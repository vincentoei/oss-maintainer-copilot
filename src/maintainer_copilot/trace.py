"""Bounded, process-local records of work that produced triage reports."""

from collections import OrderedDict
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from threading import Lock
from time import perf_counter
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

MAX_TRACES = 100


class TraceEvent(BaseModel):
    kind: Literal["retrieval", "tool", "model"]
    name: str
    status: Literal["ok", "partial", "error"] = "ok"
    started_ms: float = Field(ge=0)
    duration_ms: float = Field(ge=0)
    target: str | None = None
    result_count: int | None = Field(default=None, ge=0)
    references: list[str] = Field(default_factory=list, max_length=10)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    error: str | None = None


class TraceRecord(BaseModel):
    trace_id: UUID
    created_at: datetime
    status: Literal["complete", "partial"]
    duration_ms: float = Field(ge=0)
    events: list[TraceEvent]


_records: OrderedDict[UUID, TraceRecord] = OrderedDict()
_lock = Lock()


class TraceRecorder:
    def __init__(self) -> None:
        self.trace_id = uuid4()
        self.created_at = datetime.now(UTC)
        self.started = perf_counter()
        self.events: list[TraceEvent] = []

    @property
    def status(self) -> Literal["complete", "partial"]:
        return (
            "partial"
            if any(event.status != "ok" for event in self.events)
            else "complete"
        )

    @contextmanager
    def call(
        self,
        kind: Literal["retrieval", "tool", "model"],
        name: str,
        target: str | None = None,
    ) -> Iterator[TraceEvent]:
        started = perf_counter()
        event = TraceEvent(
            kind=kind,
            name=name,
            target=target,
            started_ms=round((started - self.started) * 1000, 3),
            duration_ms=0,
        )
        try:
            yield event
        except Exception:
            event.status = "error"
            event.error = "Call failed."
            raise
        finally:
            event.duration_ms = round((perf_counter() - started) * 1000, 3)
            self.events.append(event)

    def save(self) -> None:
        record = TraceRecord(
            trace_id=self.trace_id,
            created_at=self.created_at,
            status=self.status,
            duration_ms=round((perf_counter() - self.started) * 1000, 3),
            events=self.events,
        )
        with _lock:
            _records[self.trace_id] = record
            while len(_records) > MAX_TRACES:
                _records.popitem(last=False)


def get_trace(trace_id: UUID) -> TraceRecord | None:
    with _lock:
        record = _records.get(trace_id)
        return TraceRecord.model_validate(record.model_dump()) if record else None
