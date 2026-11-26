"""Durable pre-dispatch accounting for a serial paired model evaluation."""

import fcntl
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path


class PairedBudget:
    def __init__(
        self,
        ledger: Path,
        allowed: dict[tuple[str, str], str],
        *,
        per_model: int,
        total: int,
    ) -> None:
        self.ledger = ledger
        self.allowed = dict(allowed)
        self.per_model = per_model
        self.total = total

    def reserve(self, alias: str, case: str, body: bytes) -> None:
        digest = hashlib.sha256(body).hexdigest()
        if self.allowed.get((alias, case)) != digest:
            raise ValueError("Request differs from the frozen arm/case payload")
        with self.ledger.open("a+") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            handle.seek(0)
            previous = [json.loads(line) for line in handle]
            if (
                len(previous) >= self.total
                or sum(r["alias"] == alias for r in previous) >= self.per_model
                or any((r["alias"], r["case"]) == (alias, case) for r in previous)
            ):
                raise ValueError("Duplicate dispatch or exhausted paired budget")
            record = {
                "sequence": len(previous) + 1,
                "alias": alias,
                "case": case,
                "body_sha256": digest,
                "reserved_at": datetime.now(UTC).isoformat(),
            }
            handle.write(json.dumps(record) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
