"""Live Chromium network/CORS contract test of IQ AI Tutor STAGING v032.
This is not the full original UI. No production access, no admin keys.
Testing creates one device and one submitted/one pending run. Cleanup is
performed separately against the specific tagged synthetic test device.
"""
import json
from playwright.sync_api import sync_playwright

URL = 'https://isceyxbemyraoeixjhgp.supabase.co/functions/v1/quiz-engine-v032'
APP_VERSION = 'qa-live-browser-v033-20260920'

JS = r'''async ({url, appVersion}) => {
  const log=[];
  let device=null;
  const check=(name,pass,detail='')=>log.push({name,pass:pass===true,detail});
  async function api(action,payload={}){
    const res=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({action,...payload}),signal:AbortSignal.timeout(18000)});
    const result=await res.json();
    return {http:res.status,ok:result.ok===true,data:result.data,error:result.error,
      cors:res.headers.get('access-control-allow-origin')};
  }
  try {
    const boot=await api('bootstrap',{app_version:appVersion});
    device=boot.data?.device;
    check('B01_live_browser_bootstrap',boot.http===200&&boot.ok&&!!device?.device_id&&!!device?.device_secret);
    if (!device?.device_id||!device?.device_secret) throw Error('BOOTSTRAP_FAILED');
    const auth={device_id:device.device_id,device_secret:device.device_secret};
    const issued=await api('study_issue',{...auth,skill_code:'ch3_rr_solution_workflow'});
    const run=issued.data?.run_id;
    check('B02_live_issue',issued.http===200&&issued.ok&&!!run&&issued.data?.item?.options?.length===4);
    check('B03_no_answer_key',!(/"is_correct"|"trap_code"|"solution"|"answer_key"/).test(JSON.stringify(issued.data)));
    if(!run)throw Error('ISSUE_FAILED');
    const h=await api('study_help',{...auth,run_id:run});
    check('B04_live_help',h.http===200&&h.ok&&h.data?.assistance_recorded===true&&h.data?.run_id===run);
    const resumed=await api('study_issue',{...auth,skill_code:'ch3_rr_solution_workflow'});
    check('B05_server_help_restored',resumed.ok&&resumed.data?.run_id===run&&resumed.data?.assistance_recorded===true);
    const sent=await api('study_submit',{...auth,run_id:run,response_kind:'dont_know'});
    check('B06_live_submit',sent.ok&&sent.data?.attempt?.evidence_eligible===false&&sent.data?.assistance_used===true);
    const gate=await api('gate',{...auth,skill_code:'ch3_rr_solution_workflow',study_correct_forms:9999,study_difficulty_levels:9999});
    check('B07_no_fake_readiness',gate.ok&&gate.data?.verified_study_items===0&&gate.data?.ready_to_continue===false);
    const next=await api('study_issue',{...auth,skill_code:'ch3_rr_solution_workflow'});
    check('B08_live_next_question',next.ok&&next.data?.run_id!==run);
    // Note: no credentials, student secret, device ID or run ID are emitted to public CI logs.
  } catch(e) {
    check('B99_unhandled_exception',false,String(e?.message??e).slice(0,220));
  }
  return log;
}'''

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':390,'height':844})
    page.goto('about:blank')
    results=page.evaluate(JS,{'url':URL,'appVersion':APP_VERSION})
    browser.close()

for record in results:
    print(('PASS ' if record['pass'] else 'FAIL ')+record['name'] +
          (' '+str(record['detail']) if record['detail'] else ''))
passed=sum(r['pass'] for r in results)
print('SUMMARY '+json.dumps({'passed':passed,'total':len(results)},ensure_ascii=False))
if passed!=len(results) or len(results)!=8:
    raise SystemExit(1)
