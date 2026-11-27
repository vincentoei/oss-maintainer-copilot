const fs = require('node:fs');
const { chromium } = require(process.argv[2]);

(async () => {
  const input = JSON.parse(fs.readFileSync(0, 'utf8'));
  const browser = await chromium.launch({ headless: true, executablePath: process.argv[4] });
  try {
    const page = await browser.newPage();
    await page.goto(process.argv[3]);
    await page.locator('#title').fill(input.title);
    await page.locator('#body').fill(input.body);
    const [response] = await Promise.all([
      page.waitForResponse(r => r.url().endsWith('/api/triage') && r.request().method() === 'POST'),
      page.locator('#issue-form button[type=submit]').click(),
    ]);
    if (!response.ok()) throw new Error(`Application status ${response.status()}`);
    const report = await response.json();
    await page.locator('#report').waitFor({ state: 'visible' });
    if (await page.locator('#issue-type').textContent() !== (report.issue_type ?? 'Unknown')) {
      throw new Error('Rendered type differs from API report');
    }
    for (const [selector, value] of [
      ['#issue-type-quote', report.issue_type_quote ?? ''],
      ['#draft-reply', report.draft_reply],
      ['#trace-id', report.trace_id],
      ['#report-status', report.status],
    ]) {
      if (await page.locator(selector).textContent() !== value) {
        throw new Error(`Rendered ${selector} differs from API report`);
      }
    }
    process.stdout.write(JSON.stringify(report));
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
