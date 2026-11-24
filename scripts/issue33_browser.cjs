// Existing browser flow; real localhost HTTP and selected-model inference.
const fs = require('fs');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE);
const directory = process.argv[2];
const phase = process.argv[3];
(async () => {
  const browser = await chromium.launch({headless:true, executablePath:process.env.CHROMIUM_PATH,
    args:['--disable-gpu']});
  const page = await browser.newPage({viewport:{width:1280,height:1100}});
  const errors=[]; page.on('pageerror', e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8033');
  await page.waitForFunction(()=>document.querySelector('#repository-select').options.length>1);
  if (phase === 'register') {
    await page.locator('#repository-input').fill('https://github.com/astral-sh/ruff');
    const pending = page.waitForResponse(r=>r.url().endsWith('/api/repositories')&&r.request().method()==='POST', {timeout:90000});
    await page.locator('#repository-add button').click();
    const response=await pending; const registration=await response.json();
    if(response.status()!==200) throw new Error(JSON.stringify(registration));
    await page.waitForFunction(()=>document.querySelector('#repository-status').textContent.startsWith('astral-sh/ruff:'));
    const beforeRestart=await (await page.request.get('http://127.0.0.1:8033/api/repositories')).json();
    fs.writeFileSync(`${directory}/browser-registration.json`,JSON.stringify({browser:await browser.version(),registration,
      before_restart:beforeRestart, active:await page.locator('#repository-status').innerText(), errors},null,2)+'\n');
    await page.screenshot({path:`${directory}/browser-registration.png`,fullPage:true});
  } else if (phase === 'reports') {
    const entries=await (await page.request.get('http://127.0.0.1:8033/api/repositories')).json();
    const before=JSON.parse(fs.readFileSync(`${directory}/browser-registration.json`)).before_restart;
    if(JSON.stringify(entries)!==JSON.stringify(before)) throw new Error('Restart changed registrations');
    const results=[];
    for(const repository of ['pytest-dev/pytest','astral-sh/ruff']) {
      const entry=entries.find(e=>e.context.repository===repository);
      await page.locator('#repository-select').selectOption(entry.id);
      await page.locator('#title').fill(repository==='pytest-dev/pytest'?'Bug: collection fails in a local project':'Ruff command reports a bug in a local project');
      await page.locator('#body').fill(repository==='pytest-dev/pytest'
        ?'Synthetic smoke opening: collection fails in a local project when running a test file.'
        :'### Summary\nSynthetic smoke opening: ruff check example.py reports a failure.\n### Version\n0.17.6');
      const pending=page.waitForResponse(r=>r.url().endsWith('/api/triage')&&r.request().method()==='POST',{timeout:60000});
      await page.locator('#issue-form button[type="submit"]').click();
      const response=await pending; const report=await response.json();
      if(response.status()!==200) throw new Error(JSON.stringify(report));
      await page.locator('#report').waitFor({state:'visible'});
      await page.waitForFunction(()=>document.querySelector('#trace-events').textContent.includes('triage_selection'));
      const trace=await (await page.request.get(`http://127.0.0.1:8033/api/traces/${report.trace_id}`)).json();
      const rendered=await page.locator('#report-repository').innerText();
      const checks={identity:report.context.repository===repository, rendered:rendered.includes(repository)&&rendered.includes(report.context.revision),
        trace:trace.context.repository===repository, citations:report.citations.every(c=>c.source_url.includes(repository)||repository==='pytest-dev/pytest'&&c.source_url.startsWith('https://docs.pytest.org/')),
        reply:await page.locator('#draft-reply').innerText()===report.draft_reply,
        model_calls:trace.events.filter(e=>e.kind==='model').length===1, errors:errors.length===0};
      results.push({repository,checks,report,trace,rendered});
      await page.locator('#report').screenshot({path:`${directory}/browser-${repository.split('/')[1]}.png`});
      if(Object.values(checks).some(x=>!x)) throw new Error(JSON.stringify(checks));
    }
    fs.writeFileSync(`${directory}/browser-reports.json`,JSON.stringify({browser:await browser.version(),restart_persistence:true,results,errors},null,2)+'\n');
  } else throw new Error('Expected register or reports');
  await browser.close(); console.log(JSON.stringify({phase,errors}));
})().catch(e=>{console.error(e);process.exitCode=1;});
