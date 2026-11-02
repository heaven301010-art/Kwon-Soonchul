const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.argv[2]+'/overlay.html',{waitUntil:'networkidle'});
await p.evaluate(()=>document.fonts.ready);
for(const id of ['s1','s2','s3','s4','s5','s6']){
 await p.evaluate(id=>{document.querySelectorAll('.scene').forEach(e=>e.style.display='none');document.getElementById(id).style.display='block';},id);
 await p.screenshot({path:`${process.argv[2]}/${id}.png`,omitBackground:id!=='s6'});
}
console.log(await p.evaluate(()=>[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family).join(',')));
await b.close();})();
