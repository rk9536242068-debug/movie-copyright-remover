import streamlit as st
import yt_dlp
import os
import subprocess

# Page setup
st.set_page_config(page_title="Copyright Shield Pro", layout="centered")
st.title("🎬 Movie Copyright Remover")
st.info("Ye tool video ki metadata aur speed change karke use unique banata hai.")

# Input URL
video_url = st.text_input("Video URL (YouTube/FB/Insta) yahan paste karein:", placeholder="https://...")

# Processing Options
col1, col2 = st.columns(2)
with col1:
    speed = st.slider("Video Speed (1.05x recommended)", 1.0, 1.2, 1.05)
with col2:
    flip = st.checkbox("Mirror/Flip Video (Best for Copyright)")

if st.button("Start Processing 🚀"):
    if video_url:
        try:
            # Temporary files
            input_file = "raw_video.mp4"
            output_file = "processed_video.mp4"
            
            # Clean old files
            if os.path.exists(input_file): os.remove(input_file)
            if os.path.exists(output_file): os.remove(output_file)

            with st.spinner("Downloading video..."):
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': input_file,
                    'noplaylist': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])

            with st.spinner("Applying Copyright Shield (FFmpeg)..."):
                # Building FFmpeg command
                # 1.05x speed and changing audio pitch to match
                vf_filters = f"setpts={1/speed}*PTS"
                if flip:
                    vf_filters += ",hflip"
                
                af_filters = f"atempo={speed}"
                
                # Command to re-encode and strip metadata
                command = [
                    "ffmpeg", "-y", "-i", input_file,
                    "-vf", vf_filters,
                    "-af", af_filters,
                    "-map_metadata", "-1",  # Metadata remove karne ke liye
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
                    "-c:a", "aac", "-b:a", "128k",
                    output_file
                ]
                
                result = subprocess.run(command, capture_output=True, text=True)
                
                if result.returncode != 0:
                    st.error(f"FFmpeg Error: {result.stderr}")
                else:
                    if os.path.exists(output_file):
                        file_size = os.path.getsize(output_file) / (1024 * 1024)
                        st.success(f"✅ Ready! Size: {file_size:.2f} MB")
                        
                        with open(output_file, "rb") as f:
                            st.download_button(
                                label="Download Processed Video",
                                data=f,
                                file_name="copyright_free_video.mp4",
                                mime="video/mp4"
                            )
        except Exception as e:
            st.error(f"Kuch galat hua: {e}")
    else:
        st.warning("Please enter a valid URL.")
