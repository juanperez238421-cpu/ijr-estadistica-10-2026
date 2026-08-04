#!/usr/bin/env bash
set -euo pipefail
V=delivery/Statistics10_IQR_Graph_Construction_Problems_Professional_pqh.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,profile,width,height,r_frame_rate,avg_frame_rate,pix_fmt,nb_frames -show_entries format=duration,size -of default=noprint_wrappers=1 "$V" | tee delivery/FFPROBE.txt
grep -qx 'codec_name=h264' delivery/FFPROBE.txt
grep -qx 'width=1920' delivery/FFPROBE.txt
grep -qx 'height=1080' delivery/FFPROBE.txt
grep -qx 'r_frame_rate=30/1' delivery/FFPROBE.txt
grep -qx 'pix_fmt=yuv420p' delivery/FFPROBE.txt
python - "$V" <<'PY'
import subprocess,sys
v=sys.argv[1]; w,h=320,180; size=w*h
border=[y*w+x for y in range(h) for x in range(w) if x<2 or x>=w-2 or y<2 or y>=h-2]
p=subprocess.Popen(['ffmpeg','-v','error','-i',v,'-vf',f'scale={w}:{h},format=gray','-f','rawvideo','-pix_fmt','gray','-'],stdout=subprocess.PIPE)
frames=maximum=0; bad=[]
while True:
 d=p.stdout.read(size)
 if not d: break
 assert len(d)==size; frames+=1
 dark=sum(d[i]<96 for i in border); maximum=max(maximum,dark)
 if dark>28 and len(bad)<20: bad.append((frames,dark))
p.stdout.close(); assert p.wait()==0; assert not bad,bad
open('delivery/ALL_FRAME_BORDER_SCAN.txt','w').write(f'frames_scanned={frames}\nmax_dark_border_pixels={maximum}\nviolations=[]\nresult=PASS\n')
PY
mkdir -p delivery/qa_frames
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
python - "$D" <<'PY'
import subprocess,sys
d=float(sys.argv[1])
for i in range(1,41):
 t=min(d-.2,d*(i-.5)/40)
 subprocess.run(['ffmpeg','-y','-v','error','-ss',f'{t:.3f}','-i','delivery/Statistics10_IQR_Graph_Construction_Problems_Professional_pqh.mp4','-frames:v','1',f'delivery/qa_frames/frame_{i:02d}.png'],check=True)
PY
ffmpeg -y -v error -pattern_type glob -i 'delivery/qa_frames/frame_*.png' -vf 'scale=360:-1,tile=5x8:padding=7:margin=7:color=white' -frames:v 1 delivery/QA_CONTACT_SHEET.png
sha256sum delivery/Statistics10_IQR_Graph_Construction_Problems_Professional_pqh.mp4 delivery/Statistics10_IQR_Graph_Construction_Problems_pql.mp4 delivery/statistics10_iqr_graph_construction_problems.py delivery/QA_CONTACT_SHEET.png > delivery/SHA256SUMS.txt
cat delivery/FFPROBE.txt delivery/ALL_FRAME_BORDER_SCAN.txt delivery/SHA256SUMS.txt > delivery/TECHNICAL_VERIFICATION.txt
