# 에르나 쇼핑몰 인스타그램 릴스

- `erna_reel.mp4`: 1080×1920, 20초, 30fps (무음, 배경음악은 인스타그램에서 선택)
- `erna_reel_cover.jpg`: 커버용 장면
- `reel.html`: 영상 원본 (시간 t에 따라 `render(t)`로 장면을 그림)
- `render.js`: Playwright로 프레임을 캡처 (`node render.js <이 폴더 절대경로> frames`) 후 ffmpeg로 인코딩

```
ffmpeg -framerate 30 -i frames/f%04d.jpg -f lavfi -t 20 -i anullsrc=r=44100:cl=stereo \
  -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -shortest -movflags +faststart erna_reel.mp4
```
