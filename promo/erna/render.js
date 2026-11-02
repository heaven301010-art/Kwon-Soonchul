const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [dir,mode]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+dir+'/reel.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
if(mode==='stills'){for(const t of [2.2,4.0,6.5,11,14.8,19.5]){await p.evaluate(t=>render(t),t);await p.screenshot({path:`${dir}/still_${t}.jpg`,type:'jpeg',quality:85});}}
else{fs.mkdirSync(dir+'/frames',{recursive:true});const FPS=30,N=Math.round(20*FPS);
 for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/FPS);await p.screenshot({path:`${dir}/frames/f${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:93});}}
await b.close();})();
