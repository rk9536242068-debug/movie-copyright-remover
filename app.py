import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Movie Copyright Shield", layout="centered")

st.title("🎬 Movie Copyright Shield")
st.info("Mirror + Zoom + Logo Blur Active")

uploaded_file = st.file_uploader("Apni Movie Select Karein", type=['mp4', 'mkv', 'avi'])

if uploaded_file is not None:
    input_path = "input_video.mp4"
    output_path = "cleaned_video.mp4"
    
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())
    
    if st.button("Start Processing"):
        with st.spinner("Processing... Ismein thoda samay lagega."):
            # Code fix: Simplified filters to avoid status 8 error
            filters = (
                "hflip,"
                "crop=iw*0.8:ih*0.8,"
                "boxblur=10:5:enable='between(t,0,1000)'" # Sabse safe blur method
            )
            
            cmd = [
                'ffmpeg', '-y', '-i', input_path,
                '-vf', "hflip,crop=iw*0.9:ih*0.9,boxblur=20:enable='y<ih/6'", # Sirf top area blur karega
                '-af', "atempo=1.05",
                '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28', '-c:a', 'aac',
                output_path
            ]
            
            try:
                # Running with shell=False for better error handling
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    st.error(f"FFmpeg Error: {result.stderr}")
                else:
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="Download Cleaned Movie",
                            data=f,
                            file_name="cleaned_movie.mp4",
                            mime="video/mp4"
                        )
                    st.success("Kaam ho gaya! Video download ke liye taiyar hai.")
                
            except Exception as e:
                st.error(f"System Error: {e}")
            finally:
                if os.path.exists(input_path): os.remove(input_path)
                if os.path.exists(output_path): os.remove(output_path)

