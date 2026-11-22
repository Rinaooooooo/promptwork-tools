
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
