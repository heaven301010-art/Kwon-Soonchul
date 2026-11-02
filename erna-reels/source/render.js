const {chromium}=require('playwright');const path=process.argv[2],mode=process.argv[3];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path+'/'+(process.argv[4]||'reel.html')+'');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
const fs=require('fs');
if(mode==='preview'){for(const t of [1.9,4.6,7.2,9.7,12.1,14.8]){await p.evaluate(t=>render(t),t);await p.screenshot({path:`${path}/prev15_${t}.png`});}}
else{fs.mkdirSync(path+'/frames',{recursive:true});const N=(+process.argv[5]||19)*30;for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/30);await p.screenshot({path:`${path}/frames/f${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:95});}}
await b.close();})();
