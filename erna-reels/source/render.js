const {chromium}=require('playwright');const path=process.argv[2],mode=process.argv[3];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path+'/reel.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
const fs=require('fs');
if(mode==='preview'){for(const t of [2.6,5.8,9.0,12.2,15.2,18.8]){await p.evaluate(t=>render(t),t);await p.screenshot({path:`${path}/prev_${t}.png`});}}
else{fs.mkdirSync(path+'/frames',{recursive:true});const N=19*30;for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/30);await p.screenshot({path:`${path}/frames/f${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:95});}}
await b.close();})();
