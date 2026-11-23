// Render preserved real HTTP/inference output; this is not a fresh live-web run.
const fs = require('fs');
const {chromium} = require('/tmp/issue21-npm/_npx/e41f203b7505f1fb/node_modules/playwright');
(async () => {
  const live = process.argv.includes('--live');
  let liveReport, liveTrace;
  const record = JSON.parse(fs.readFileSync('/tmp/issue-50-run/api-smoke.json'))[1];
  const browser = await chromium.launch({headless:true,
    executablePath:'/tmp/issue21-browsers/chromium-1255/chrome-linux64/chrome',
    args:['--disable-gpu']});
  const page = await browser.newPage({viewport:{width:1280,height:1100}});
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  if (!live) await page.route('http://issue50.local/**', async route => {
    const path = new URL(route.request().url()).pathname;
    if (path === '/') return route.fulfill({contentType:'text/html',
      body:fs.readFileSync('src/maintainer_copilot/index.html','utf8')});
    const value = path.startsWith('/api/traces/') ? record.trace : record.report;
    return route.fulfill({contentType:'application/json',body:JSON.stringify(value)});
  });
  await page.goto(live ? 'http://127.0.0.1:8002/' : 'http://issue50.local/');
  const opening = live ? JSON.parse(fs.readFileSync('/tmp/issue-50-run/web-opening.json')) : {title:'Recorded development report rendering',body:'Render the preserved genuine bounded-agent response.'};
  await page.locator('#title').fill(opening.title);
  await page.locator('#body').fill(opening.body);
  if (live) await page.locator('#number').fill(String(opening.number));
  const responsePending = live ? page.waitForResponse(r=>r.url().endsWith('/api/agent/triage'),{timeout:90000}) : null;
  await page.locator('#agent-mode').check();
  await page.getByRole('button',{name:'Create triage report'}).click();
  if (live) {
    const response = await responsePending;
    liveReport = await response.json();
    liveTrace = await (await page.request.get('http://127.0.0.1:8002/api/traces/'+liveReport.trace_id)).json();
    record.report = liveReport; record.trace = liveTrace;
  }
  await page.locator('#report').waitFor({state:'visible'});
  await page.waitForFunction(() => document.querySelector('#trace-events').textContent.includes('triage_selection'));
  const draft = await page.locator('#draft-reply').innerText();
  const result = {scope:live ? 'Fresh browser-triggered real inference, existing bounded-agent HTTP report.' : 'Browser rendering of preserved real-inference HTTP response; no fresh browser-triggered inference.',
    assertions:{rendered_reply_matches:draft===record.report.draft_reply,
      partial_status_visible:(await page.locator('#report-status').innerText()).toLowerCase().includes('partial'),
      no_javascript_errors:errors.length===0},
    report_trace_id:record.report.trace_id, report:liveReport, trace:liveTrace, javascript_errors:errors};
  await page.locator('#report').screenshot({path:live?'docs/evaluation/issue-50/web-live.png':'docs/evaluation/issue-50/web-render.png'});
  fs.writeFileSync(live?'docs/evaluation/issue-50/web-live.json':'docs/evaluation/issue-50/web-render.json',JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result));
  await browser.close();
  if (Object.values(result.assertions).some(value=>!value)) process.exit(1);
})().catch(error=>{console.error(error);process.exit(1)});
