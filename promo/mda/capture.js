const {chromium}=require('playwright');
const fs=require('fs');
const OUT=process.argv[2];
const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
const lerp=(a,b,t)=>a+(b-a)*t;
// crop: {cx,cy,h} portrait 9:16 in CSS px
const scenes=[
 {name:'s1', n:110, setup:null, from:{x:340,y:78,h:995}, to:{x:590,y:78,h:995}},
 {name:'s2', n:140, setup:'서해', from:{x:230,y:78,h:995}, to:{x:330,y:150,h:760}},
 {name:'s3', n:110, setup:'한반도 해역', from:{x:1500,y:78,h:760}, to:{x:1505,y:150,h:700}},
 {name:'s4', n:110, setup:'북극항로', from:{x:337,y:120,h:900}, to:{x:380,y:220,h:740}},
 {name:'s5', n:125, setup:'원해 SLOC', from:{x:70,y:300,h:700}, to:{x:1080,y:260,h:700}},
];
(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:2});
await p.clock.install({time:new Date('2026-11-02T05:00:00Z')});
await p.goto('http://localhost:8765/mda/',{waitUntil:'load'});
await p.clock.runFor(2000);
await p.getByRole('button',{name:'×600',exact:true}).click();
await p.clock.runFor(4000);
for(const s of scenes){
  const dir=`${OUT}/${s.name}`; fs.mkdirSync(dir,{recursive:true});
  if(s.setup){ if(s.setup==='한반도 해역'){await p.getByRole('button',{name:'한반도 해역',exact:true}).click(); await p.clock.runFor(300); await p.getByRole('button',{name:'전체',exact:true}).first().click();}
    else await p.getByRole('button',{name:s.setup,exact:true}).click();
    await p.clock.runFor(1200);}
  for(let i=0;i<s.n;i++){
    const t=ease(i/(s.n-1));
    const h=lerp(s.from.h,s.to.h,t), w=h*9/16;
    const clip={x:lerp(s.from.x,s.to.x,t), y:lerp(s.from.y,s.to.y,t), width:w, height:h};
    await p.clock.runFor(33);
    await p.screenshot({path:`${dir}/f${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92,clip});
  }
  console.log('done',s.name,new Date().toISOString());
}
await b.close();})();
