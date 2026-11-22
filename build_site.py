#!/usr/bin/env python3
import os, textwrap
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)

CSS = """
:root{--bg:#0f172a;--card:#ffffff;--ink:#0f172a;--muted:#64748b;--brand:#2563eb;--brand2:#7c3aed;--line:#e2e8f0;--soft:#f1f5f9}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:var(--ink);background:#f8fafc;line-height:1.6}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
header.site{background:var(--bg);color:#fff;padding:14px 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}
header.site .logo{font-weight:800;font-size:20px;color:#fff}
nav a{color:#cbd5e1;margin-left:16px;font-size:15px}
.hero{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;padding:56px 20px;text-align:center}
.hero h1{font-size:38px;margin:0 0 12px}.hero p{font-size:18px;opacity:.92;max-width:720px;margin:0 auto 20px}
.btn{display:inline-block;background:#fff;color:var(--brand);padding:12px 22px;border-radius:10px;font-weight:700;border:0;cursor:pointer;font-size:16px}
.btn.primary{background:var(--brand);color:#fff}.btn.primary:hover{background:#1d4ed8}
.wrap{max-width:1024px;margin:0 auto;padding:28px 20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px}
.card h3{margin-top:0}.badge{display:inline-block;background:var(--soft);color:var(--brand);font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px;margin-bottom:8px}
.tool{background:#fff;border:1px solid var(--line);border-radius:14px;padding:24px;margin-bottom:24px}
label{font-weight:700;display:block;margin:14px 0 6px}
input,textarea,select{width:100%;padding:11px;border:1px solid #cbd5e1;border-radius:10px;font-size:15px;font-family:inherit}
textarea{min-height:110px}
.out{white-space:pre-wrap;background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:16px;min-height:120px;font-size:15px}
.row{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:720px){.row{grid-template-columns:1fr}.hero h1{font-size:29px}}
footer{background:var(--bg);color:#94a3b8;padding:26px 20px;text-align:center;font-size:14px;margin-top:40px}
.small{color:var(--muted);font-size:14px}.faq h3{margin-bottom:4px}
"""

JS = r"""
function copyText(id,btn){const t=document.getElementById(id).innerText;navigator.clipboard.writeText(t).then(()=>{const o=btn.innerText;btn.innerText='Copied!';setTimeout(()=>btn.innerText=o,1500)})}
function lines(id){return document.getElementById(id).value.split('\n').map(s=>s.trim()).filter(Boolean)}
function val(id){return document.getElementById(id).value.trim()}
function setOut(id,text){document.getElementById(id).innerText=text}

function genWeekly(){
 const role=val('role')||'Team member';
 const done=lines('done'),prog=lines('prog'),block=lines('block'),next=lines('next');
 let o='WEEKLY REPORT\nRole: '+role+'\n\nCOMPLETED THIS WEEK\n';
 o+= done.length?done.map(x=>'- '+x).join('\n'):'- [Add what you finished, with a result or number]';
 o+='\n\nIN PROGRESS\n'; o+= prog.length?prog.map(x=>'- '+x).join('\n'):'- [Add what is under way and how far it got]';
 o+='\n\nBLOCKERS\n'; o+= block.length?block.map(x=>'- '+x+' — next step: follow up and escalate if not resolved').join('\n'):'- None';
 o+='\n\nPLAN FOR NEXT WEEK\n'; o+= next.length?next.map(x=>'- '+x).join('\n'):'- [Add next steps that match the unfinished items above]';
 o+='\n\nTip: write every completed item as Action + Task + Result. Example: "Published 2 posts (12k views)" beats "worked on posts".';
 setOut('out',o);
 const p='Rewrite my rough weekly notes into a clear, results-focused weekly report. Do not invent facts or numbers. Keep blockers honest and pair every unfinished item with a next-week plan.\n\nMy notes:\nCompleted: '+(done.join('; ')||'-')+'\nIn progress: '+(prog.join('; ')||'-')+'\nBlockers: '+(block.join('; ')||'-')+'\nNext week: '+(next.join('; ')||'-');
 setOut('prompt',p);
}
function genMinutes(){
 const title=val('mtitle')||'Meeting', date=val('mdate'), people=val('people');
 const notes=lines('notes'); const dec=[],act=[],disc=[];
 notes.forEach(n=>{const l=n.toLowerCase(); if(/decid|agree|approv|final/.test(l))dec.push(n); else if(/will |by |@|deadline|todo|action/.test(l))act.push(n); else disc.push(n)});
 let o='MEETING MINUTES — '+title+(date?'\nDate: '+date:'')+(people?'\nAttendees: '+people:'');
 o+='\n\nDECISIONS\n'+(dec.length?dec.map(x=>'- '+x).join('\n'):'- [No clear decisions found in your notes — check lines marked as discussion]');
 o+='\n\nACTION ITEMS\n'+(act.length?act.map(x=>'- '+x+'  [owner + deadline: confirm]').join('\n'):'- [No action items found — add who does what, by when]');
 o+='\n\nDISCUSSION POINTS\n'+(disc.length?disc.map(x=>'- '+x).join('\n'):'-');
 o+='\n\nBefore sending: give every action item an owner and a deadline, or it did not really get assigned.';
 setOut('out',o);
 const p='Turn my raw meeting notes into clean minutes with three sections only: Decisions, Action Items (task + owner + deadline), and Open Questions. Do not invent owners, dates or decisions that are not in the notes — list anything unclear under Open Questions.\n\nMeeting: '+title+'\nNotes:\n'+notes.join('\n');
 setOut('prompt',p);
}
function genEmail(){
 const tone=document.getElementById('tone').value; const subj=val('subj'); let body=val('draft');
 body=body.replace(/\s+\n/g,'\n').trim();
 const greet=tone==='formal'?'Dear Sir or Madam,':(tone==='friendly'?'Hi there,':'Hello,');
 const close=tone==='formal'?'Kind regards':(tone==='friendly'?'Thanks so much':'Best regards');
 let o=(subj?'Subject: '+subj+'\n\n':'')+greet+'\n\n'+body+'\n\n'+close;
 setOut('out',o);
 const p='Polish this email in a '+tone+' tone. Keep every fact, name, date and number exactly as written. Make it shorter, clearer, and put the request in the first two lines.\n\n'+body;
 setOut('prompt',p);
}
const formulas={
 sumif:{f:"=SUMIF(A:A,\"Criteria\",B:B)",e:"Adds up column B wherever column A matches the criteria. Replace Criteria and the columns with yours."},
 countif:{f:"=COUNTIF(A:A,\"Criteria\")",e:"Counts how many cells in column A match the criteria."},
 xlookup:{f:"=XLOOKUP(D2,A:A,B:B,\"Not found\")",e:"Looks up the value in D2 inside column A and returns the matching value from column B. Excel 365 / 2021+. For older Excel use VLOOKUP."},
 vlookup:{f:"=VLOOKUP(D2,A:B,2,FALSE)",e:"Looks up D2 in the first column of A:B and returns the 2nd column. FALSE means an exact match is required."},
 if:{f:"=IF(A2>=60,\"Pass\",\"Fail\")",e:"Tests a condition: returns the first value when true, the second when false. Change 60 and the labels to fit your case."},
 textjoin:{f:"=TEXTJOIN(\" \",TRUE,A2,B2)",e:"Joins text from cells with a separator, skipping empty cells. Useful for full names and addresses."},
 datedif:{f:"=DATEDIF(A2,B2,\"D\")",e:"Number of days between two dates. Use \"M\" for whole months or \"Y\" for whole years."}
};
function genFormula(){const k=document.getElementById('ftask').value;const d=formulas[k];setOut('out',d.f+'\n\nWhat it does: '+d.e);setOut('prompt','Write an Excel formula for this task and explain it in one line. Task: '+k+'. My data layout is: [describe your columns here, e.g. A = date, B = amount, C = status].')}
function genCover(){
 const name=val('cname')||'Your Name', role=val('crole')||'the position', comp=val('ccomp')||'your company';
 const yrs=val('cyrs')||'several'; const skills=lines('cskills'); const win=val('cwin');
 let o='COVER LETTER\n\nDear Hiring Manager,\n\nI am writing to apply for '+role+' at '+comp+'. With '+yrs+' years of relevant experience'+(skills.length?', including '+skills.join(', '):'')+', I help teams deliver work that is measurable, not just busy.\n\n'+(win?('A recent example: '+win+'\n\n'):'')+'I would welcome the chance to discuss how my experience fits what '+comp+' is building. Thank you for your time and consideration.\n\nSincerely,\n'+name;
 o+='\n\nTip: a cover letter is not your resume in prose. One role, one proof point, one reason this company — that is the whole job.';
 setOut('out',o);
 const p='Write a concise cover letter (250-320 words) for '+name+' applying for '+role+' at '+comp+'. Experience: '+yrs+' years. Skills: '+(skills.join(', ')||'[add skills]')+'. Key achievement: '+(win||'[add one measurable achievement]')+'. Rules: no cliches like "team player" without proof, no repeating the resume line by line, end with a confident but polite call to action.';
 setOut('prompt',p);
}
function genSummary(){
 const role=val('srole')||'Professional', yrs=val('syrs')||'several', ind=val('sind')||'my industry';
 const skills=lines('sskills'); const wins=lines('swins');
 let o='RESUME SUMMARY\n\n'+role+' with '+yrs+' years of experience in '+ind+'. '+(skills.length?('Core strengths: '+skills.join(', ')+'. '):'')+(wins.length?('Selected results: '+wins.join('; ')+'. '):'')+'Known for turning messy, unclear work into structured plans with visible results.';
 o+='\n\nTip: put your strongest measurable result in the first two lines — recruiters skim, they do not read.';
 setOut('out',o);
 const p='Write 3 versions of a resume professional summary for a '+role+' with '+yrs+' years of experience in '+ind+'. Skills: '+(skills.join(', ')||'[add skills]')+'. Achievements: '+(wins.join('; ')||'[add measurable achievements]')+'. Version 1: safe and corporate. Version 2: results-first. Version 3: short (2 lines) for LinkedIn. No invented numbers.';
 setOut('prompt',p);
}
function genResign(){
 const name=val('rname')||'Your Name', mgr=val('rmgr')||'Manager', comp=val('rcomp')||'the company';
 const last=val('rlast')||'[your last working day]'; const reason=document.getElementById('rreason').value;
 const reasons={opportunity:'I have accepted a new opportunity that is the right next step for my career.',personal:'I am stepping away for personal reasons and need to focus on matters outside work.',relocation:'I will be relocating, which makes it necessary for me to leave my current role.',change:'I have decided to make a career change and pursue a different direction.'};
 let o='RESIGNATION LETTER\n\nDear '+mgr+',\n\nPlease accept this letter as formal notice of my resignation from my position at '+comp+'. My last working day will be '+last+'.\n\n'+reasons[reason]+'\n\nI am grateful for the opportunities, support and experience I have gained here, and I will do everything I can to hand over my work smoothly before my last day.\n\nThank you again, and I wish the team continued success.\n\nSincerely,\n'+name;
 o+='\n\nTip: keep it short, warm and final. The exit conversation is not the place to re-litigate old frustrations.';
 setOut('out',o);
 const p='Write a short, professional resignation letter for '+name+' resigning from '+comp+', addressed to '+mgr+', last working day '+last+'. Tone: grateful, clear and final, with an offer to help the handover. Do not include complaints or negotiation language. Keep it under 180 words.';
 setOut('prompt',p);
}
function genPpt(){
 const topic=val('topic')||'Your Topic',aud=val('audience')||'a general audience',n=parseInt(val('nslides'))||8;
 const flow=['Title: '+topic+' — a talk for '+aud,'Why it matters now','The problem in one picture','Key point 1','Key point 2','Key point 3','Example / case study','What most people get wrong','Step-by-step plan','Risks and how to handle them','Summary: the 3 things to remember','Call to action / next steps'];
 let chosen=flow.slice(0,Math.max(3,Math.min(n,flow.length))); if(n>flow.length){for(let i=flow.length+1;i<=n;i++)chosen.push('Extra slide '+i+': supporting data')}
 let o='PRESENTATION OUTLINE — '+topic+'\nAudience: '+aud+'\n\n'+chosen.map((s,i)=>(i+1)+'. '+s).join('\n');
 setOut('out',o);
 const p='Create a presentation outline about "'+topic+'" for '+aud+', '+n+' slides. For each slide give a headline that states the takeaway (not just a topic), plus 3 short supporting bullets. No filler slides.';
 setOut('prompt',p);
}
function genReview(){
 const role=val('rvrole')||'my role', period=val('rvperiod')||'this review period';
 const ach=lines('rvach'),grow=lines('rvgrow'),chal=lines('rvchal'),goals=lines('rvgoals');
 const rate=document.getElementById('rvrate').value;
 let o='PERFORMANCE SELF-REVIEW\nRole: '+role+'\nPeriod: '+period+'\nSelf-rating: '+rate+'\n\nSUMMARY\nThis period, working as '+role+', I focused on work that could be measured. '+(ach.length?('My biggest results: '+ach[0]+(ach.length>1?('; '+ach[1]):'')+'. '):'')+'Overall I rate my performance as: '+rate.toLowerCase()+'.\n\nKEY ACHIEVEMENTS\n';
 o+= ach.length?ach.map(x=>'- '+x).join('\n'):'- [Add achievements with numbers: what you did, and what changed because of it]';
 o+='\n\nSKILLS DEVELOPED\n'; o+= grow.length?grow.map(x=>'- '+x).join('\n'):'- [Add skills you built and where you actually used them]';
 o+='\n\nCHALLENGES AND WHAT I LEARNED\n'; o+= chal.length?chal.map(x=>'- '+x).join('\n'):'- [Name one real challenge and what you changed because of it — honesty here builds trust]';
 o+='\n\nGOALS FOR NEXT PERIOD\n'; o+= goals.length?goals.map(x=>'- '+x).join('\n'):'- [Add 2-3 goals you can actually measure]';
 o+='\n\nTip: managers calibrate on evidence. Every achievement should answer "so what changed?" with a number, a date, or a before-and-after.';
 setOut('out',o);
 const p='Write my performance self-review in first person. Role: '+role+'. Period: '+period+'. Self-rating: '+rate+'. Achievements: '+(ach.join('; ')||'[add]')+'. Skills developed: '+(grow.join('; ')||'[add]')+'. Challenges: '+(chal.join('; ')||'[add]')+'. Next goals: '+(goals.join('; ')||'[add]')+'. Rules: turn every achievement into an impact statement, admit one real challenge honestly, sound like an adult professional, and invent no numbers.';
 setOut('prompt',p);
}
function genSalary(){
 const name=val('saname')||'Your Name', mgr=val('samgr')||'Manager';
 const cur=val('sacur')||'[current salary]', tar=val('satar')||'[target salary]', yrs=val('sayrs')||'';
 const ach=lines('saach'); const mkt=val('samkt');
 let o='Subject: Request to discuss a compensation adjustment\n\nDear '+mgr+',\n\nI am writing to ask for a review of my compensation. '+(yrs?('I have been in this role for '+yrs+', and in that time '):'In my time here, ')+'the scope and results of my work have grown well beyond my current package.\n\nRecent contributions:\n';
 o+= ach.length?ach.map(x=>'- '+x).join('\n'):'- [Add 3-4 contributions, each with a measurable result]';
 o+='\n\n'+(mkt?('Market check: '+mkt+'\n\n'):'')+'Based on these results, I would like to request an adjustment from '+cur+' to '+tar+'. I am glad to discuss the reasoning in person, and to agree on any milestones you would like to attach to it.\n\nThank you for considering this — I value this role and want to keep building here.\n\nBest regards,\n'+name;
 o+='\n\nTip: send this after a visible win, not during a crisis. The ask lands when your value is freshest in the room.';
 setOut('out',o);
 const p='Write a salary negotiation email from '+name+' to '+mgr+'. Current salary: '+cur+'. Requested: '+tar+(yrs?('. Time in role: '+yrs):'')+'. Contributions: '+(ach.join('; ')||'[add measurable contributions]')+(mkt?('. Market data: '+mkt):'')+'. Tone: confident, factual and warm. Structure: one line of gratitude, evidence of impact, market context, the specific ask, and a request to discuss it in a meeting. No threats, no ultimatums, under 250 words.';
 setOut('prompt',p);
}
function genLinkedIn(){
 const name=val('liname')||'Professional', role=val('lirole')||'Professional', ind=val('liind')||'my industry', yrs=val('liyrs')||'several';
 const spec=lines('lispec'), ach=lines('liach'), focus=val('lifocus');
 let head=role+(spec.length?(' | '+spec.slice(0,3).join(' / ')):'')+(ind?(' | '+ind):'');
 let o='LINKEDIN HEADLINE\n'+head+'\n\nABOUT SECTION\nI am a '+role+' with '+yrs+' years of experience in '+ind+'. '+(spec.length?('My work focuses on '+spec.join(', ')+'. '):'')+(ach.length?('Some results I am proud of: '+ach.join('; ')+'. '):'')+(focus?('Right now I am focused on '+focus+'. '):'')+'If you work on similar problems, I am glad to connect.';
 o+='\n\nTip: your headline is searchable. Put the role title and the skills recruiters actually type — not your company slogan.';
 setOut('out',o);
 const p='Write my LinkedIn profile text for '+name+'. Headline: one line with role, top skills and industry. About section: 150-200 words, first person. Role: '+role+', '+yrs+' years in '+ind+'. Specialties: '+(spec.join(', ')||'[add]')+'. Achievements: '+(ach.join('; ')||'[add]')+'. Current focus: '+(focus||'[add]')+'. Give 2 versions: Version A professional, Version B warmer and more personal. No buzzword soup (no "guru", "ninja" or "visionary"), and invent no facts.';
 setOut('prompt',p);
}
function genJobDesc(){
 const t=val('jdtitle')||'Job Title', comp=val('jdcomp')||'Our Company', dept=val('jddept')||'', lvl=document.getElementById('jdlvl').value;
 const loc=val('jdloc')||'[location / work type]', sal=val('jdsal');
 const resp=lines('jdresp'), req=lines('jdreq'), nice=lines('jdnice');
 let o=comp+' is hiring: '+t+(dept?(' ('+dept+')'):'')+'\nLevel: '+lvl+'\nLocation: '+loc+(sal?('\nCompensation: '+sal):'')+'\n\nABOUT THE ROLE\nWe are looking for a '+lvl.toLowerCase()+' '+t+' to join '+(dept?('the '+dept+' team'):'our team')+' at '+comp+'. You will own real outcomes from day one, work with a small team, and see the direct impact of your work.\n\nWHAT YOU WILL DO\n';
 o+= resp.length?resp.map(x=>'- '+x).join('\n'):'- [Add 5-7 responsibilities, each starting with a verb]';
 o+='\n\nWHAT YOU BRING\n'; o+= req.length?req.map(x=>'- '+x).join('\n'):'- [Add genuine must-haves only — every extra requirement shrinks your applicant pool]';
 if(nice.length){o+='\n\nNICE TO HAVE\n'+nice.map(x=>'- '+x).join('\n')}
 o+='\n\nHOW TO APPLY\nSend your resume and one short paragraph on the most relevant thing you have built or delivered. We reply to every serious application.';
 o+='\n\nTip: if a requirement would not actually disqualify a great candidate, move it to Nice to have or delete it.';
 setOut('out',o);
 const p='Write a complete job description for a '+lvl+' '+t+' at '+comp+(dept?(' ('+dept+')'):'')+', '+loc+(sal?(', compensation '+sal):'')+'. Responsibilities: '+(resp.join('; ')||'[add]')+'. Must-have requirements: '+(req.join('; ')||'[add]')+'. Nice to have: '+(nice.join('; ')||'none')+'. Rules: inclusive, concrete language; keep must-haves truly essential; add a realistic day-in-the-life paragraph; end with a clear how-to-apply.';
 setOut('prompt',p);
}
function genApology(){
 const name=val('apname')||'Your Name', rec=val('aprec')||'there';
 const what=val('apwhat')||'[describe what happened]', fix=val('apfix');
 const tone=document.getElementById('aptone').value;
 const open=tone==='formal'?'I am writing to sincerely apologize':'I owe you a direct apology';
 let o='Subject: My apology — '+what.slice(0,60)+'\n\nDear '+rec+',\n\n'+open+' for what happened: '+what+'.\n\nThat was on me. I understand it caused real inconvenience and may have cost you time and trust, and I am not going to hide behind excuses.\n\n'+(fix?('What I have done about it: '+fix+'\n\n'):'')+'I value our working relationship and I will make sure this specific failure does not repeat. If there is anything else I can do to make this right, please tell me directly.\n\n'+(tone==='formal'?'Sincerely':'With apologies')+',\n'+name;
 o+='\n\nTip: never write "sorry if you were offended" — that apologizes for their feelings, not your actions. Name the failure, own it, show the fix.';
 setOut('out',o);
 const p='Write a sincere business apology email from '+name+' to '+rec+'. What happened: '+what+'. '+(fix?('Corrective action already taken: '+fix+'. '):'')+'Rules: apologize for the specific action (never "sorry if you felt"), take responsibility without excuses, state the fix and how it will be prevented, keep it under 200 words, tone: '+tone+'.';
 setOut('prompt',p);
}
function genFollowUp(){
 const name=val('funame')||'Your Name', iv=val('fuiv')||'Hiring Team', role=val('furole')||'the role', comp=val('fucomp')||'your company';
 const topic=val('futopic'); const type=document.getElementById('futype').value;
 let body='';
 if(type==='thankyou'){body='Thank you for taking the time to speak with me about '+role+' at '+comp+'. '+(topic?('I especially enjoyed our discussion about '+topic+', and it confirmed that this is exactly the kind of problem I want to work on. '):'')+'I am very enthusiastic about the role and confident I can contribute quickly. Please let me know if I can provide anything else.'}
 else if(type==='nudge'){body='I wanted to follow up on my interview for '+role+' at '+comp+'. I remain very interested in the role'+(topic?(', and our conversation about '+topic+' has stayed with me'):'')+'. I understand timelines shift — if it helps, I am happy to provide references or additional work samples. Thank you again for your consideration.'}
 else{body='As promised during our conversation about '+role+' at '+comp+', I am sending over the material we discussed'+(topic?(' regarding '+topic):'')+'. I hope it gives a clear picture of how I approach this kind of work. I would welcome any feedback, and I am glad to walk through it together.'}
 let o='Subject: '+(type==='thankyou'?('Thank you — '+role+' interview'):('Following up — '+role+' at '+comp))+'\n\nDear '+iv+',\n\n'+body+'\n\nBest regards,\n'+name;
 o+='\n\nTip: one specific callback to the actual conversation is worth more than three paragraphs of generic enthusiasm. Send thank-you notes within 24 hours.';
 setOut('out',o);
 const p='Write a short follow-up email from '+name+' to '+iv+' about '+role+' at '+comp+'. Type: '+(type==='thankyou'?'thank-you after interview':(type==='nudge'?'gentle nudge, no reply yet':'sending promised material'))+'. Specific conversation detail to reference: '+(topic||'[add one topic you actually discussed]')+'. Rules: under 150 words, specific not generic, confident without being pushy, one clear closing line.';
 setOut('prompt',p);
}
"""

def page(title, desc, body, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | PromptWork Tools</title><meta name="description" content="{desc}">{extra_head}
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta property="og:title" content="{title} | PromptWork Tools"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:image" content="https://promptwork-tools.pages.dev/og-image.png"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/style.css"></head><body>
<header class="site"><a class="logo" href="/">PromptWork Tools</a><nav><a href="/">All Tools</a><a href="/weekly-report-generator.html">Weekly Report</a><a href="/meeting-minutes-generator.html">Meeting Minutes</a><a href="/excel-formula-generator.html">Excel Formula</a></nav></header>
{body}
<footer>PromptWork Tools — free office tools that run 100% in your browser. Nothing you type is uploaded or stored.<br><a href="/privacy-policy.html" style="color:#cbd5e1">Privacy Policy</a> &middot; <a href="/about.html" style="color:#cbd5e1">About &amp; Contact</a><br>&copy; 2026 PromptWork Tools</footer>
<script src="/assets/app.js"></script></body></html>"""

def tool_shell(h1, intro, form, faq):
    return f"""<div class="wrap"><h1>{h1}</h1><p class="small">{intro}</p>
<div class="tool">{form}
<h3>Your result</h3><div class="out" id="out">Fill in the fields above and click Generate.</div><p><button class="btn" onclick="copyText('out',this)">Copy result</button></p>
<h3>Want a smarter version? Use this AI prompt</h3><div class="out" id="prompt">Your copy-ready prompt for ChatGPT / Claude will appear here.</div><p><button class="btn" onclick="copyText('prompt',this)">Copy AI prompt</button></p></div>
<div class="faq"><h2>FAQ</h2>{faq}</div></div>"""

home_body = """<section class="hero"><h1>Free AI Office Tools That Save You an Hour a Week</h1>
<p>Weekly reports, meeting minutes, emails, Excel formulas and presentation outlines — structured in seconds, right in your browser. No sign-up, no upload, free.</p>
<a class="btn" href="/weekly-report-generator.html">Start with the Weekly Report Generator</a></section>
<div class="wrap"><h2>All tools</h2><div class="grid">
<div class="card"><span class="badge">MOST POPULAR</span><h3>Weekly Report Generator</h3><p>Turn rough notes into a results-focused weekly report your manager will actually read.</p><a href="/weekly-report-generator.html">Open tool &rarr;</a></div>
<div class="card"><h3>Meeting Minutes Generator</h3><p>Paste raw notes and get decisions, action items and discussion points, sorted for you.</p><a href="/meeting-minutes-generator.html">Open tool &rarr;</a></div>
<div class="card"><h3>Email Polisher</h3><p>Pick a tone and get a clean, ready-to-send structure for any work email.</p><a href="/email-polisher.html">Open tool &rarr;</a></div>
<div class="card"><h3>Excel Formula Generator</h3><p>Choose the job, get the exact formula plus a plain-English explanation.</p><a href="/excel-formula-generator.html">Open tool &rarr;</a></div>
<div class="card"><h3>PPT Outline Generator</h3><p>Topic in, slide-by-slide outline out — with headlines that state the takeaway.</p><a href="/ppt-outline-generator.html">Open tool &rarr;</a></div>
<div class="card"><span class="badge">NEW</span><h3>Cover Letter Generator</h3><p>One role, one proof point, one reason this company — a cover letter that is not your resume in prose.</p><a href="/cover-letter-generator.html">Open tool &rarr;</a></div>
<div class="card"><span class="badge">NEW</span><h3>Resume Summary Generator</h3><p>A tight professional summary that leads with your strongest measurable result.</p><a href="/resume-summary-generator.html">Open tool &rarr;</a></div>
<div class="card"><span class="badge">NEW</span><h3>Resignation Letter Generator</h3><p>Short, warm and final — resign gracefully and keep every door open.</p><a href="/resignation-letter-generator.html">Open tool &rarr;</a></div>
<div class="card"><span class="badge">NEW</span><h3>Performance Review Generator</h3><p>A self-review built on evidence: achievements with numbers, one honest challenge, measurable goals.</p><a href="/performance-review-generator.html">Open tool &rarr;</a></div>
<div class="card"><span class="badge">NEW</span><h3>Salary Negotiation Email Generator</h3><p>Ask for a raise the way managers can approve: proof of impact, market context, one specific number.</p><a href="/salary-negotiation-email-generator.html">Open tool &rarr;</a></div>
<div class="card"><span class="badge">NEW</span><h3>LinkedIn Summary Generator</h3><p>A headline recruiters can find, plus an About section that sounds like a person, not a slogan.</p><a href="/linkedin-summary-generator.html">Open tool &rarr;</a></div>
<div class="card"><span class="badge">NEW</span><h3>Job Description Generator</h3><p>Complete, realistic job posts — honest must-haves, clear responsibilities, no laundry lists.</p><a href="/job-description-generator.html">Open tool &rarr;</a></div>
<div class="card"><span class="badge">NEW</span><h3>Apology Email Generator</h3><p>A business apology that actually works: name it, own it, show the fix.</p><a href="/apology-email-generator.html">Open tool &rarr;</a></div>
<div class="card"><span class="badge">NEW</span><h3>Follow-Up Email Generator</h3><p>Interview thank-yous and gentle nudges built around one specific detail from your conversation.</p><a href="/follow-up-email-generator.html">Open tool &rarr;</a></div>
</div>
<h2>How it works</h2><p>1. Pick a tool and type or paste your rough material. 2. Click Generate — the tool structures it instantly, in your browser. 3. Copy the result, or copy the bonus AI prompt and paste it into ChatGPT or Claude for an even smarter rewrite. Your text never leaves your device.</p>
<h2>Why free?</h2><p>These tools run entirely on your device, so they cost almost nothing to offer. If they save you time, bookmark the page and share it with a coworker — that is all we ask.</p></div>"""

weekly_form = """<label>Your role</label><input id="role" placeholder="e.g. Marketing specialist">
<label>Completed this week (one per line, add results or numbers)</label><textarea id="done" placeholder="Published 2 posts (12k views)&#10;Sorted 18 customer feedback items"></textarea>
<label>In progress (one per line)</label><textarea id="prog" placeholder="Product guide: chapter 3 of 5 done"></textarea>
<label>Blockers (one per line)</label><textarea id="block" placeholder="Waiting on supplier quote, no reply yet"></textarea>
<label>Plan for next week (one per line)</label><textarea id="next" placeholder="Finish guide chapters 4-5&#10;Follow up on supplier quote on Monday"></textarea>
<p><button class="btn primary" onclick="genWeekly()">Generate my report</button></p>"""
weekly_faq = """<h3>How do I write a weekly report that is not just a list?</h3><p>Write every item as Action + Task + Result. "Published 2 posts (12k views)" tells your manager what happened; "worked on posts" does not.</p>
<h3>Should I include blockers?</h3><p>Yes — a blocker with your next step ("waiting on a quote, following up Monday") shows progress management, not excuses.</p>
<h3>Is my text uploaded anywhere?</h3><p>No. This tool runs 100% in your browser.</p>"""

minutes_form = """<label>Meeting title</label><input id="mtitle" placeholder="e.g. Product guide review">
<div class="row"><div><label>Date</label><input id="mdate" placeholder="e.g. Nov 10, 2026"></div><div><label>Attendees</label><input id="people" placeholder="e.g. Lee, Wang, Chen"></div></div>
<label>Raw notes (one point per line — lines with "decided / agreed" go to Decisions, lines with "will / by" go to Action Items)</label><textarea id="notes" placeholder="Decided to launch the guide on Friday&#10;Wang will send the supplier a reminder by Tuesday&#10;Discussed the 18 feedback items"></textarea>
<p><button class="btn primary" onclick="genMinutes()">Generate minutes</button></p>"""
minutes_faq = """<h3>What makes meeting minutes useful?</h3><p>Three things only: what was decided, who owns each next step, and by when. Everything else is background.</p>
<h3>How does the sorting work?</h3><p>Simple keyword rules run in your browser. Always review the result — and give every action item an owner and a deadline before sending.</p>"""

email_form = """<label>Subject (optional)</label><input id="subj" placeholder="e.g. Follow-up on the supplier quote">
<label>Tone</label><select id="tone"><option value="professional">Professional</option><option value="formal">Formal</option><option value="friendly">Friendly</option></select>
<label>Your draft</label><textarea id="draft" placeholder="Paste your rough email here..."></textarea>
<p><button class="btn primary" onclick="genEmail()">Polish structure</button></p>"""
email_faq = """<h3>Does this rewrite my email with AI?</h3><p>The instant result restructures your draft with a greeting, clean body and sign-off for the tone you picked. For a full AI rewrite, copy the generated prompt into ChatGPT or Claude together with your draft.</p>"""

excel_form = """<label>What do you need to do?</label><select id="ftask"><option value="sumif">Add up values that match a condition (SUMIF)</option><option value="countif">Count cells that match a condition (COUNTIF)</option><option value="xlookup">Look up a value — modern Excel (XLOOKUP)</option><option value="vlookup">Look up a value — older Excel (VLOOKUP)</option><option value="if">Return one value or another based on a test (IF)</option><option value="textjoin">Join text from several cells (TEXTJOIN)</option><option value="datedif">Days / months / years between two dates (DATEDIF)</option></select>
<p><button class="btn primary" onclick="genFormula()">Get the formula</button></p>"""
excel_faq = """<h3>XLOOKUP or VLOOKUP — which should I use?</h3><p>XLOOKUP if you have Excel 365 or 2021 or newer: it is simpler and safer. VLOOKUP still works everywhere, but the column index breaks when you insert columns.</p>"""

ppt_form = """<label>Presentation topic</label><input id="topic" placeholder="e.g. Q3 marketing results and Q4 plan">
<label>Audience</label><input id="audience" placeholder="e.g. department managers">
<label>Number of slides</label><input id="nslides" type="number" value="8" min="3" max="12">
<p><button class="btn primary" onclick="genPpt()">Generate outline</button></p>"""
ppt_faq = """<h3>What makes a good slide headline?</h3><p>A headline should state the takeaway ("Sales grew 18% in Q3"), not just the topic ("Sales"). The generated AI prompt enforces that rule.</p>"""

cover_form = """<label>Your name</label><input id="cname" placeholder="e.g. Alex Morgan">
<div class="row"><div><label>Job title you are applying for</label><input id="crole" placeholder="e.g. Product Marketing Manager"></div><div><label>Company</label><input id="ccomp" placeholder="e.g. Notion"></div></div>
<label>Years of relevant experience</label><input id="cyrs" placeholder="e.g. 5">
<label>Top skills (one per line)</label><textarea id="cskills" placeholder="Campaign planning&#10;Data analysis&#10;Cross-team coordination"></textarea>
<label>One measurable achievement</label><input id="cwin" placeholder="e.g. grew signup conversion by 23% in one quarter">
<p><button class="btn primary" onclick="genCover()">Generate cover letter</button></p>"""
cover_faq = """<h3>How long should a cover letter be?</h3><p>250-350 words. Hiring managers skim: one role fit, one proof point, one genuine reason for this company.</p>
<h3>Should I just repeat my resume?</h3><p>No. The letter explains why you fit this specific role; the resume lists what you have done. The generated AI prompt enforces that split.</p>"""

summary_form = """<div class="row"><div><label>Your role / target role</label><input id="srole" placeholder="e.g. Operations Manager"></div><div><label>Years of experience</label><input id="syrs" placeholder="e.g. 7"></div></div>
<label>Industry</label><input id="sind" placeholder="e.g. e-commerce logistics">
<label>Core skills (one per line)</label><textarea id="sskills" placeholder="Process optimization&#10;Team leadership&#10;Budget control"></textarea>
<label>Measurable achievements (one per line)</label><textarea id="swins" placeholder="Cut delivery delays by 31%&#10;Saved $120k in annual vendor costs"></textarea>
<p><button class="btn primary" onclick="genSummary()">Generate summary</button></p>"""
summary_faq = """<h3>What belongs in a resume summary?</h3><p>Role, years, industry, 3-4 core strengths and your single strongest measurable result. Nothing else — it is a headline, not a biography.</p>
<h3>Summary or objective statement?</h3><p>Summary. Objective statements ("seeking a challenging role") describe what you want; summaries describe what the employer gets.</p>"""

resign_form = """<div class="row"><div><label>Your name</label><input id="rname" placeholder="e.g. Alex Morgan"></div><div><label>Manager's name</label><input id="rmgr" placeholder="e.g. Ms. Chen"></div></div>
<div class="row"><div><label>Company</label><input id="rcomp" placeholder="e.g. Acme Ltd."></div><div><label>Last working day</label><input id="rlast" placeholder="e.g. December 5, 2026"></div></div>
<label>Reason</label><select id="rreason"><option value="opportunity">Accepted a new opportunity</option><option value="personal">Personal reasons</option><option value="relocation">Relocating</option><option value="change">Career change</option></select>
<p><button class="btn primary" onclick="genResign()">Generate resignation letter</button></p>"""
resign_faq = """<h3>How much notice should I give?</h3><p>Follow your contract and local norms — two to four weeks is typical. State one clear last working day and stick to it.</p>
<h3>Should I explain my real reasons in detail?</h3><p>No. One neutral line is enough. Gratitude plus a clean handover offer protects your reputation far better than a full explanation.</p>"""

review_form = """<div class="row"><div><label>Your role</label><input id="rvrole" placeholder="e.g. Customer Support Lead"></div><div><label>Review period</label><input id="rvperiod" placeholder="e.g. 2026, second half"></div></div>
<label>Self-rating</label><select id="rvrate"><option>Exceeded expectations</option><option>Met expectations</option><option>Approaching expectations</option></select>
<label>Key achievements (one per line, add numbers)</label><textarea id="rvach" placeholder="Reduced average ticket resolution time from 9h to 5h&#10;Trained 4 new team members to full productivity"></textarea>
<label>Skills you developed (one per line)</label><textarea id="rvgrow" placeholder="Root-cause analysis&#10;Running weekly team reviews"></textarea>
<label>Challenges and what you learned (one per line)</label><textarea id="rvchal" placeholder="Q3 backlog spike: learned to escalate capacity problems two weeks earlier"></textarea>
<label>Goals for next period (one per line)</label><textarea id="rvgoals" placeholder="Bring resolution time under 4h&#10;Document the top 20 recurring issues"></textarea>
<p><button class="btn primary" onclick="genReview()">Generate my self-review</button></p>"""
review_faq = """<h3>What do managers actually look for in a self-review?</h3><p>Evidence. Every claim should carry a number, a date or a before-and-after. "Improved the process" is forgettable; "cut resolution time from 9h to 5h" is a calibration anchor.</p>
<h3>Should I hide my weak areas?</h3><p>No — name one real challenge and what you changed because of it. A review with no weakness reads as either unaware or dishonest, and managers discount the whole document.</p>"""

salary_form = """<div class="row"><div><label>Your name</label><input id="saname" placeholder="e.g. Alex Morgan"></div><div><label>Manager's name</label><input id="samgr" placeholder="e.g. Mr. Lee"></div></div>
<div class="row"><div><label>Current salary</label><input id="sacur" placeholder="e.g. $72,000"></div><div><label>Target salary</label><input id="satar" placeholder="e.g. $82,000"></div></div>
<label>Time in this role</label><input id="sayrs" placeholder="e.g. 2 years">
<label>Your contributions (one per line, measurable)</label><textarea id="saach" placeholder="Took over vendor reporting, saving the team 6 hours a week&#10;Closed the two largest renewals of the year ($410k combined)"></textarea>
<label>Market data (optional)</label><input id="samkt" placeholder="e.g. similar roles in this city are posted at $80k-$88k">
<p><button class="btn primary" onclick="genSalary()">Generate negotiation email</button></p>"""
salary_faq = """<h3>When is the best moment to send this?</h3><p>Right after a visible win — a shipped project, a closed deal, a glowing review — and never in the middle of a crisis or a conflict. Timing is half the negotiation.</p>
<h3>Should the first ask happen by email or in person?</h3><p>Email first, meeting second. A written ask gives your manager something concrete to take to their own boss; the meeting is where you discuss it, not where they first hear it.</p>"""

linkedin_form = """<div class="row"><div><label>Your name</label><input id="liname" placeholder="e.g. Alex Morgan"></div><div><label>Current or target role</label><input id="lirole" placeholder="e.g. Operations Manager"></div></div>
<div class="row"><div><label>Industry</label><input id="liind" placeholder="e.g. e-commerce logistics"></div><div><label>Years of experience</label><input id="liyrs" placeholder="e.g. 8"></div></div>
<label>Specialties (one per line — these become headline keywords)</label><textarea id="lispec" placeholder="Supply chain planning&#10;Warehouse automation&#10;Vendor negotiation"></textarea>
<label>Achievements (one per line)</label><textarea id="liach" placeholder="Cut fulfilment costs 18% across 3 warehouses&#10;Built the planning process the team still uses"></textarea>
<label>Current focus (what you want to be known for / open to)</label><input id="lifocus" placeholder="e.g. helping mid-size retailers fix delivery promises">
<p><button class="btn primary" onclick="genLinkedIn()">Generate headline + about</button></p>"""
linkedin_faq = """<h3>What makes a LinkedIn headline work?</h3><p>Searchability. Recruiters type role titles and skills, not slogans. "Operations Manager | Supply Chain Planning | E-commerce Logistics" gets found; "Passionate problem-solver" does not.</p>
<h3>First person or third person for the About section?</h3><p>First person. It reads as a human talking, and it is the voice people expect when they reach out to connect.</p>"""

jobdesc_form = """<div class="row"><div><label>Job title</label><input id="jdtitle" placeholder="e.g. Content Writer"></div><div><label>Company</label><input id="jdcomp" placeholder="e.g. Acme Ltd."></div></div>
<div class="row"><div><label>Department (optional)</label><input id="jddept" placeholder="e.g. Marketing"></div><div><label>Seniority</label><select id="jdlvl"><option>Entry-level</option><option>Mid-level</option><option>Senior</option><option>Lead / Manager</option></select></div></div>
<div class="row"><div><label>Location / work type</label><input id="jdloc" placeholder="e.g. Remote (EU time zones)"></div><div><label>Compensation (optional)</label><input id="jdsal" placeholder="e.g. $55k-$70k + benefits"></div></div>
<label>Responsibilities (one per line)</label><textarea id="jdresp" placeholder="Write 2 product explainers per week&#10;Interview customers and turn calls into case studies&#10;Keep the help centre up to date"></textarea>
<label>Must-have requirements (one per line — be strict with yourself)</label><textarea id="jdreq" placeholder="2+ years writing for software products&#10;Portfolio of published long-form pieces"></textarea>
<label>Nice to have (one per line)</label><textarea id="jdnice" placeholder="Basic HTML&#10;Experience with SEO tools"></textarea>
<p><button class="btn primary" onclick="genJobDesc()">Generate job description</button></p>"""
jobdesc_faq = """<h3>Why do long requirement lists hurt hiring?</h3><p>Every "must-have" filters out candidates who would have been great. Research on job ads consistently shows qualified people self-select out when they meet only part of an inflated list. Keep must-haves to what would truly disqualify.</p>
<h3>Should I include the salary range?</h3><p>Yes, if you can. Postings with a range get more and better-matched applicants, and in a growing number of places it is legally required.</p>"""

apology_form = """<div class="row"><div><label>Your name</label><input id="apname" placeholder="e.g. Alex Morgan"></div><div><label>Recipient</label><input id="aprec" placeholder="e.g. Ms. Patel"></div></div>
<label>What happened (be concrete — vague apologies do not work)</label><textarea id="apwhat" placeholder="e.g. I missed the Friday delivery deadline for the Q3 report and did not warn you until Monday morning"></textarea>
<label>What you have done to fix it (optional but powerful)</label><textarea id="apfix" placeholder="e.g. the report is now delivered, and I have set a Thursday checkpoint so a slip is flagged a day early"></textarea>
<label>Tone</label><select id="aptone"><option value="formal">Formal</option><option value="warm">Warm professional</option></select>
<p><button class="btn primary" onclick="genApology()">Generate apology email</button></p>"""
apology_faq = """<h3>What are the parts of an apology that actually works?</h3><p>Four: name the specific failure, take responsibility without excuses, state what you fixed, and say how it will not repeat. Skip any one of them and the apology feels hollow.</p>
<h3>Is "sorry if you were offended" ever acceptable?</h3><p>No. It apologizes for the other person's feelings instead of your actions, and everyone reads it that way. If you are not ready to own the action, wait until you are.</p>"""

followup_form = """<div class="row"><div><label>Your name</label><input id="funame" placeholder="e.g. Alex Morgan"></div><div><label>Interviewer / recipient</label><input id="fuiv" placeholder="e.g. Mr. Thompson"></div></div>
<div class="row"><div><label>Role</label><input id="furole" placeholder="e.g. Product Designer"></div><div><label>Company</label><input id="fucomp" placeholder="e.g. Figma"></div></div>
<label>One specific topic from your conversation (this is what makes it work)</label><input id="futopic" placeholder="e.g. your plan to rebuild onboarding in Q1">
<label>Email type</label><select id="futype"><option value="thankyou">Thank-you after an interview</option><option value="nudge">Gentle nudge — no reply yet</option><option value="material">Sending promised material</option></select>
<p><button class="btn primary" onclick="genFollowUp()">Generate follow-up email</button></p>"""
followup_faq = """<h3>How fast should a thank-you email go out?</h3><p>Within 24 hours, while the conversation is still fresh for both sides. Same day is best; after two days it starts to read as an afterthought.</p>
<h3>How many nudges are too many?</h3><p>Two, spaced about a week apart. After that, silence is the answer — a third nudge only spends goodwill.</p>"""

privacy_body = """<div class="wrap"><h1>Privacy Policy</h1><p class="small">Last updated: November 2026</p>
<h2>The short version</h2><p>PromptWork Tools runs entirely in your browser. The text you type into any tool on this site is processed on your own device and is never uploaded to, or stored on, a server by us. We have no user accounts, no sign-up, and no database of visitor content.</p>
<h2>What we collect</h2><p><strong>Tool inputs: nothing.</strong> Everything you enter into a generator stays in the page on your device. When you close the tab, it is gone.</p>
<p><strong>Basic hosting logs.</strong> This site is hosted on Cloudflare Pages. Like any web host, Cloudflare may process standard technical information (such as IP address, browser type and pages requested) to deliver the site and protect it from abuse. That processing is governed by Cloudflare's own privacy policy.</p>
<h2>Cookies</h2><p>We do not set advertising or tracking cookies. If this changes in the future — for example, if we add advertising — this policy will be updated before the change takes effect, and any consent requirements that apply will be honoured.</p>
<h2>Third parties</h2><p>Some tools offer a copy-ready prompt that you may choose to paste into a third-party AI service such as ChatGPT or Claude. That action is entirely yours: nothing is sent anywhere until you paste it yourself, and whatever you share there is covered by that service's privacy policy, not this one.</p>
<h2>Children</h2><p>This site provides general office productivity tools and is not directed at children under 13.</p>
<h2>Changes</h2><p>If this policy changes, the updated version will be posted on this page with a new date.</p>
<h2>Contact</h2><p>Questions about this policy: see the <a href="/about.html">About &amp; Contact</a> page.</p></div>"""

about_body = """<div class="wrap"><h1>About PromptWork Tools</h1>
<p>PromptWork Tools is a small, independent collection of free office tools: weekly reports, meeting minutes, emails, Excel formulas, presentation outlines and the paperwork of working life — cover letters, resignation letters, performance reviews and more.</p>
<h2>How the tools work</h2><p>Every tool works the same way: you fill in a short form, and the tool structures your material instantly, using rules that run 100% in your browser. Nothing you type is uploaded or stored. Each tool also gives you a copy-ready AI prompt, so if you want a smarter rewrite you can paste it into ChatGPT or Claude yourself — your choice, your data.</p>
<h2>Why free?</h2><p>Because the tools run on your device, they cost almost nothing to offer. There are no accounts and no paywalls. If a tool saves you time, the best thank-you is to bookmark it and share it with a coworker.</p>
<h2>Who runs this?</h2><p>An independent creator building practical tools for office workers, one small tool at a time. New tools are added based on what people actually search for and ask about.</p>
<h2>Contact</h2><p>Feedback, corrections and tool requests are very welcome:<br><strong>stolarzstuttgen@gmail.com</strong></p>
<p class="small">We read everything; replies may take a few days. Please do not send resumes or personal documents — the tools on this site are the right place for those, and they never leave your browser.</p></div>"""

pages = {
 "index.html": page("Free AI Office Tools", "Free browser-based office tools: weekly report generator, meeting minutes generator, email polisher, Excel formula generator and PPT outline generator. No sign-up.", home_body),
 "weekly-report-generator.html": page("Weekly Report Generator — Free, No Sign-Up", "Turn rough notes into a results-focused weekly report in seconds. Free, runs in your browser, plus a copy-ready AI prompt.", tool_shell("Weekly Report Generator", "Built on one rule: Action + Task + Result. Paste your rough notes and get a report your manager will actually read.", weekly_form, weekly_faq)),
 "meeting-minutes-generator.html": page("Meeting Minutes Generator — Decisions & Action Items, Sorted", "Paste raw meeting notes and get minutes sorted into decisions, action items and discussion points. Free and private.", tool_shell("Meeting Minutes Generator", "Good minutes answer three questions: what was decided, who does what, and by when. This tool sorts your notes into exactly that.", minutes_form, minutes_faq)),
 "email-polisher.html": page("Email Polisher — Clean, Ready-to-Send Work Emails", "Restructure any work email in a professional, formal or friendly tone, plus a copy-ready AI prompt for a full rewrite.", tool_shell("Email Polisher", "Pick a tone, paste your draft, and get a clean structure instantly — then use the AI prompt if you want a deeper rewrite.", email_form, email_faq)),
 "excel-formula-generator.html": page("Excel Formula Generator — Formula + Plain-English Explanation", "Pick the job and get the exact Excel formula — SUMIF, COUNTIF, XLOOKUP, VLOOKUP, IF and more — explained in plain English.", tool_shell("Excel Formula Generator", "No more Googling syntax. Choose what you are trying to do and copy the formula, with an explanation of how it works.", excel_form, excel_faq)),
 "ppt-outline-generator.html": page("PPT Outline Generator — Slide-by-Slide Outlines That Make Sense", "Enter a topic and audience and get a logical slide-by-slide presentation outline, plus an AI prompt for takeaway headlines.", tool_shell("PPT Outline Generator", "A good deck is an argument, not a pile of slides. This outline follows a proven flow: why it matters, the problem, the evidence, the plan.", ppt_form, ppt_faq)),
 "cover-letter-generator.html": page("Cover Letter Generator — One Role, One Proof Point", "Generate a focused cover letter from your role, company and best achievement, plus a copy-ready AI prompt. Free, no sign-up.", tool_shell("Cover Letter Generator", "One rule separates good cover letters from resume re-runs: one role fit, one proof point, one real reason for this company.", cover_form, cover_faq)),
 "resume-summary-generator.html": page("Resume Summary Generator — Lead With Your Best Result", "Build a tight resume professional summary from your role, skills and measurable achievements, plus an AI prompt for 3 versions.", tool_shell("Resume Summary Generator", "Recruiters skim for about six seconds. This summary puts your role, strengths and strongest number where their eyes land first.", summary_form, summary_faq)),
 "resignation-letter-generator.html": page("Resignation Letter Generator — Short, Warm and Final", "Generate a professional resignation letter with notice date and a graceful handover offer, plus a copy-ready AI prompt.", tool_shell("Resignation Letter Generator", "A good resignation letter is short, warm and final: clear last day, one neutral reason, real gratitude, and a handover offer.", resign_form, resign_faq)),
 "performance-review-generator.html": page("Performance Review Generator — A Self-Review Built on Evidence", "Turn your achievements, skills and challenges into a structured performance self-review, plus a copy-ready AI prompt. Free, no sign-up.", tool_shell("Performance Review Generator", "Self-reviews are won on evidence, not adjectives. Put in what you delivered — with numbers — and get a review your manager can calibrate on.", review_form, review_faq)),
 "salary-negotiation-email-generator.html": page("Salary Negotiation Email Generator — Ask With Evidence, Not Nerves", "Generate a calm, evidence-based salary negotiation email: contributions, market context and a specific ask, plus an AI prompt.", tool_shell("Salary Negotiation Email Generator", "A raise is an argument, not a favour. This tool builds it in the right order: gratitude, proof of impact, market context, one specific number.", salary_form, salary_faq)),
 "linkedin-summary-generator.html": page("LinkedIn Summary Generator — Headline + About That Get Found", "Generate a searchable LinkedIn headline and a first-person About section from your role, specialties and results, plus an AI prompt.", tool_shell("LinkedIn Summary Generator", "Recruiters search for role titles and skills. This tool builds a headline that matches those searches and an About section that sounds like a person.", linkedin_form, linkedin_faq)),
 "job-description-generator.html": page("Job Description Generator — Clear JDs Without the Laundry List", "Generate a complete, realistic job description from responsibilities and genuine must-haves, plus a copy-ready AI prompt.", tool_shell("Job Description Generator", "Most job ads fail by asking for everything. This tool keeps must-haves honest and structures the rest so the right people actually apply.", jobdesc_form, jobdesc_faq)),
 "apology-email-generator.html": page("Apology Email Generator — Sincere, Specific, No Excuses", "Generate a business apology email that names the failure, owns it and shows the fix, plus a copy-ready AI prompt.", tool_shell("Apology Email Generator", "A working apology has four parts: the specific failure, responsibility without excuses, the fix, and prevention. This tool writes all four.", apology_form, apology_faq)),
 "follow-up-email-generator.html": page("Follow-Up Email Generator — Thank-You Notes and Gentle Nudges", "Generate an interview thank-you, a gentle no-reply nudge or a sending-materials follow-up with one specific callback, plus an AI prompt.", tool_shell("Follow-Up Email Generator", "Follow-ups fail when they are generic. One specific detail from the actual conversation does the work — this tool is built around it.", followup_form, followup_faq)),
 "privacy-policy.html": page("Privacy Policy", "How PromptWork Tools handles your data: tools run 100% in your browser, nothing you type is uploaded or stored.", privacy_body),
 "about.html": page("About & Contact", "About PromptWork Tools: free browser-based office tools, how they work, and how to get in touch.", about_body),
}
for name, html in pages.items():
    with open(os.path.join(SITE, name), "w", encoding="utf-8") as f: f.write(html)
with open(os.path.join(SITE, "assets", "style.css"), "w", encoding="utf-8") as f: f.write(CSS)
with open(os.path.join(SITE, "assets", "app.js"), "w", encoding="utf-8") as f: f.write(JS)
FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2563eb"/><stop offset="1" stop-color="#7c3aed"/></linearGradient></defs><rect width="64" height="64" rx="14" fill="url(#g)"/><text x="32" y="45" font-family="Arial,sans-serif" font-size="36" font-weight="bold" fill="#ffffff" text-anchor="middle">P</text></svg>'
with open(os.path.join(SITE, "favicon.svg"), "w", encoding="utf-8") as f: f.write(FAVICON)
_og = os.path.join(ROOT, "og-image.png")
if os.path.exists(_og):
    with open(_og, "rb") as src, open(os.path.join(SITE, "og-image.png"), "wb") as dst: dst.write(src.read())
with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8") as f: f.write("User-agent: *\nAllow: /\n\nSitemap: https://promptwork-tools.pages.dev/sitemap.xml\n")
BASE = "https://promptwork-tools.pages.dev"
URLS = ["/", "/weekly-report-generator", "/meeting-minutes-generator", "/email-polisher", "/excel-formula-generator", "/ppt-outline-generator", "/cover-letter-generator", "/resume-summary-generator", "/resignation-letter-generator", "/performance-review-generator", "/salary-negotiation-email-generator", "/linkedin-summary-generator", "/job-description-generator", "/apology-email-generator", "/follow-up-email-generator", "/privacy-policy", "/about"]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in URLS:
    pr = "1.0" if u == "/" else "0.9"
    sm += f"  <url><loc>{BASE}{u}</loc><changefreq>weekly</changefreq><priority>{pr}</priority></url>\n"
sm += "</urlset>\n"
with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f: f.write(sm)
# Google Search Console ownership verification file — must stay in site root, never delete
with open(os.path.join(SITE, "google96fc746a1d2f731e.html"), "w", encoding="utf-8") as f: f.write("google-site-verification: google96fc746a1d2f731e.html")
print("built", sorted(os.listdir(SITE)))
