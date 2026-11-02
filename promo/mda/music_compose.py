import numpy as np, scipy.signal as sg, scipy.io.wavfile as wf, sys
SR=44100; DUR=21.68; N=int(SR*DUR)
L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def midi(m): return 440*2**((m-69)/12)
def add(sig,t0,pan=0.0,gain=1.0):
    i=int(t0*SR); j=min(N,i+len(sig)); 
    if i>=N: return
    s=sig[:j-i]*gain; L[i:j]+=s*np.sqrt((1-pan)/2); R[i:j]+=s*np.sqrt((1+pan)/2)
def env(n,a,r,sus=1.0):
    e=np.ones(n)*sus; na=max(1,int(a*SR)); nr=max(1,int(r*SR))
    e[:na]=np.linspace(0,sus,na); e[-nr:]*=np.linspace(1,0,nr); return e
def saw(f,n,det=0.0):
    t=np.arange(n)/SR; ph=(f*(1+det))*t+rng.random(); return 2*(ph%1)-1
def lp(x,fc,order=2):
    b,a=sg.butter(order,min(fc,SR/2-100)/(SR/2)); return sg.lfilter(b,a,x)
def hp(x,fc):
    b,a=sg.butter(2,fc/(SR/2),'high'); return sg.lfilter(b,a,x)
# --- harmony timeline (time, root midi, chord intervals)
CUT=[3.317,7.633,10.95,14.267,18.083]
chords=[(0,50,[0,3,7]),(3.317,46,[0,4,7]),(5.48,41,[0,4,7]),(7.633,43,[0,3,7]),(9.29,45,[0,4,7]),
        (10.95,50,[0,3,7]),(12.6,46,[0,4,7]),(14.267,41,[0,4,7]),(16.17,48,[0,4,7]),(18.083,50,[0,3,7,12])]
ends=[c[0] for c in chords[1:]]+[DUR]
# strings pad: detuned saws, voiced in two octaves
for (t0,root,iv),t1 in zip(chords,ends):
    n=int((t1-t0+0.6)*SR); 
    for k,i in enumerate(iv):
        for octv,g in [(12,0.06),(24,0.045)]:
            f=midi(root+i+octv); x=sum(saw(f,n,d) for d in (-0.004,-0.0015,0,0.0017,0.0042))/5
            x=lp(x,1800 if t0<18 else 2600)*env(n,0.35,0.55)
            add(x,t0,pan=(k-1)*0.5,gain=g*(1.0 if t0>3 else 0.7))
# low drone / bass
for (t0,root,iv),t1 in zip(chords,ends):
    n=int((t1-t0+0.3)*SR); t=np.arange(n)/SR; f=midi(root-24)
    x=(0.6*np.sin(2*np.pi*f*t)+0.25*lp(saw(f,n),400))*env(n,0.08,0.3)
    add(x,t0,gain=0.33)
# brass stabs/swells at cuts and chord changes after intro
for (t0,root,iv),t1 in zip(chords,ends):
    if t0<3: continue
    n=int(min(t1-t0,1.9)*SR); t=np.arange(n)/SR
    x=np.zeros(n)
    for i in iv[:3]:
        for o in (0,12):
            f=midi(root+i+o); x+=sum(saw(f,n,d) for d in (-0.003,0,0.003))/3
    fenv=600+2600*np.exp(-t*2.5)*np.clip(t/0.08,0,1)
    # time-varying lowpass approx: blend two filters
    a=lp(x,700); b=lp(x,3200); m=(fenv-600)/2600
    y=(a*(1-m)+b*m)*env(n,0.04,0.6)
    add(y,t0,gain=0.07 if t0<18 else 0.1)
# taiko-like drums
def taiko(g=1.0,f0=130,f1=48):
    n=int(1.1*SR); t=np.arange(n)/SR
    f=f1+(f0-f1)*np.exp(-t*30); ph=2*np.pi*np.cumsum(f)/SR
    body=np.sin(ph)*np.exp(-t*5.5)
    nz=lp(rng.standard_normal(n),1800)*np.exp(-t*28)*0.35
    return (body+nz)*g
beat=60/92
t=1.2
pattern=[1,0,0.5,0,0.8,0,0.5,0.4]   # 8ths
while t<18.0:
    step=int(round((t-1.2)/(beat/2)))
    inten=0.35 if t<3.3 else (0.6 if t<10.95 else 0.85)
    v=pattern[step%8]
    if t>14.3 and step%2==1: v=max(v,0.45)   # build: fill 8ths
    if v>0: add(taiko(inten*v,140 if v<0.6 else 120,52),t,pan=(0.25 if step%2 else -0.25),gain=0.55)
    t+=beat/2
# string ostinato (spiccato 16ths) from scene 2, follows chord root
t=3.317; sixteenth=beat/4
while t<18.0:
    c=[c for c in chords if c[0]<=t+1e-6][-1]; root=c[1]
    k=int(round((t-3.317)/sixteenth)); notes=[0,0,12,0, 7,0,12,7]
    f=midi(root+12+notes[k%8]); n=int(0.16*SR); tt=np.arange(n)/SR
    x=lp(sum(saw(f,n,d) for d in (-0.003,0.003))/2,2400)*np.exp(-tt*22)
    add(x,t,pan=0.35,gain=0.05 if t<10.95 else 0.07)
    t+=sixteenth
# risers into each cut + boom hits
for c in CUT:
    rl=1.4 if c!=18.083 else 2.6; n=int(rl*SR); tt=np.arange(n)/SR
    nz=rng.standard_normal(n); x=np.zeros(n)
    # sweep: progressively brighter bandpass via blend
    x=lp(nz,600)*(1-tt/rl)+hp(lp(nz,7000),1500)*(tt/rl)
    x*= (tt/rl)**2
    add(x,c-rl,gain=0.12 if c!=18.083 else 0.2)
    n=int(3.0*SR); tt=np.arange(n)/SR
    f=38+70*np.exp(-tt*9); boom=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*1.6)
    crash=lp(hp(rng.standard_normal(n),2500),9000)*np.exp(-tt*3.2)*0.13
    add(boom+crash,c,gain=0.55 if c!=18.083 else 0.8)
# final chord choir-ish sustain swell already in pad; add timpani roll before end hit
t=16.6
while t<18.06:
    add(taiko(0.25+0.4*(t-16.6)/1.5,110,60),t,gain=0.4); t+=0.07
# reverb
irn=int(2.6*SR); tt=np.arange(irn)/SR
irL=rng.standard_normal(irn)*np.exp(-tt*2.4); irR=rng.standard_normal(irn)*np.exp(-tt*2.4)
irL=lp(irL,5000); irR=lp(irR,5000); irL/=np.sqrt((irL**2).sum()); irR/=np.sqrt((irR**2).sum())
wetL=sg.fftconvolve(L,irL)[:N]; wetR=sg.fftconvolve(R,irR)[:N]
outL=L*0.8+wetL*0.45; outR=R*0.8+wetR*0.45
# fade in/out
fi=int(0.4*SR); fo=int(1.6*SR)
for o in (outL,outR): o[:fi]*=np.linspace(0,1,fi); o[-fo:]*=np.linspace(1,0,fo)**1.5
st=np.stack([outL,outR],1); st/=np.abs(st).max()*1.05
wf.write(sys.argv[1],SR,(st*32767).astype(np.int16)); print('ok')
