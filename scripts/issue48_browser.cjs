// Focused real-inference check of the existing web report; no model mock.
const fs = require('fs');
const crypto = require('crypto');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE);

(async () => {
  const prefix = process.argv[3];
  if (!prefix || fs.existsSync(prefix + '.json') || fs.existsSync(prefix + '.png')) {
    throw new Error('Supply a new output prefix after the temporary openings path');
  }
  const issue = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'))['12219'];
  const ledgerPath = process.env.MODEL_CALLS_PATH;
  const first = fs.existsSync(ledgerPath) ? JSON.parse(fs.readFileSync(ledgerPath)).length : 0;
  const browser = await chromium.launch({headless:true,
    executablePath:process.env.CHROMIUM_PATH, args:['--disable-gpu']});
  const page = await browser.newPage({viewport:{width:1280,height:1100}});
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8001');
  await page.locator('#number').fill('12219');
  await page.locator('#title').fill(issue.title);
  await page.locator('#body').fill(issue.body);
  await page.locator('#agent-mode').check();
  const pending = page.waitForResponse(r => r.url().endsWith('/api/agent/triage') &&
    r.request().method() === 'POST', {timeout:60000});
  await page.getByRole('button', {name:'Create triage report'}).click();
  const response = await pending;
  const report = await response.json();
  await page.locator('#report').waitFor({state:'visible'});
  await page.waitForFunction(() => document.querySelector('#trace-events').textContent.includes('triage_selection'));
  const traceResponse = await page.request.get('http://127.0.0.1:8001/api/traces/' + report.trace_id);
  const trace = await traceResponse.json();
  const rendered = {
    status:await page.locator('#report-status').innerText(),
    draft_reply:await page.locator('#draft-reply').innerText(),
    missing_details:await page.locator('#missing-details').innerText(),
  };
  const assertions = {
    http_ok:response.status() === 200,
    targeted_follow_up:rendered.draft_reply.includes('minimized failing example'),
    rendered_reply_matches:rendered.draft_reply === report.draft_reply,
    matching_trace:trace.trace_id === report.trace_id,
    real_usage:trace.events.some(e => e.kind === 'model' && e.status === 'ok' && e.input_tokens > 0),
    model_calls_bounded:trace.events.filter(e => e.kind === 'model').length <= 4,
    no_javascript_errors:errors.length === 0,
  };
  await page.locator('#report').screenshot({path:prefix + '.png'});
  fs.writeFileSync(prefix + '.json', JSON.stringify({
    recorded_at:new Date().toISOString(), browser:await browser.version(),
    scope:'Existing web bounded-agent report, real Ollama; verified frozen issue candidates, ordinary live documentation, separate from historical field scoring',
    input_content_sha256:crypto.createHash('sha256').update(issue.title + '\0' + issue.body).digest('hex'),
    assertions, rendered, report, trace, javascript_errors:errors,
    model_calls:JSON.parse(fs.readFileSync(ledgerPath)).slice(first),
  }, null, 2) + '\n');
  console.log(JSON.stringify(assertions));
  await browser.close();
  if (Object.values(assertions).some(x => !x)) process.exit(1);
})().catch(e => {console.error(e); process.exit(1);});
