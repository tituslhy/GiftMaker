ffmpeg -i Gabriel.mp4 -i Licheng.mp4 -i Shauna.mp4 -filter_complex \
"[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:-1:-1,setsar=1,fps=30,format=yuv420p[v0];
 [1:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:-1:-1,setsar=1,fps=30,format=yuv420p[v1];
 [2:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:-1:-1,setsar=1,fps=30,format=yuv420p[v2];
 [v0][0:a][v1][1:a][v2][2:a]concat=n=3:v=1:a=1[v][a]" \
-map "[v]" -map "[a]" -c:v libx264 -c:a aac -movflags +faststart happybirthday.mp4