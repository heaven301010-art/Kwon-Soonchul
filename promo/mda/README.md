# MDA 공통작전상황도 인스타그램 릴스

- `mda_reel.mp4`: 1080×1920, 21.7초, 30fps (무음, 배경음악은 인스타그램에서 선택)
- `mda_reel_cover.jpg`: 커버용 장면

장면: 한반도 전체 → 서해 확대(센서 융합) → 정보 공유·지휘결심 → 북극항로 → 원해 SLOC → 접속 주소

## 다시 만들기
1. 저장소 루트에서 `python3 -m http.server 8765`
2. `node capture.js <출력폴더>`: Playwright 가짜 시계로 상황도를 한 프레임씩 캡처(장면별 s1~s5 폴더)
3. `node render.js <이 폴더 절대경로>`: `overlay.html`의 문구를 장면별 투명 PNG(s1~s6)로 저장 (`overlay/`에 결과 포함)
4. 장면마다 ffmpeg로 프레임 위에 PNG를 겹쳐 클립을 만들고, `xfade`(0.35초)로 이어 붙임
