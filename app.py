import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Rajneesh Movie Shield", layout="wide")
st.title("🚀 Rajneesh Bhaskar - Pro Movie Shield")

# Logo file path
LOGO_FILE = "1642.jpg"

uploaded_file = st.file_uploader("Movie Upload Karein", type=['mp4', 'mkv'])

if uploaded_file:
    st.sidebar.header("⚙️ Smart Settings")
    zoom_level = st.sidebar.slider("Zoom Level", 0.8, 1.0, 0.9)
    blur_intensity = st.sidebar.slider("Blur Intensity", 5, 50, 15)
    audio_pitch = st.sidebar.slider("Audio Speed", 1.0, 1.1, 1.05)
    wm_name = st.sidebar.text_input("Branding Name", "Rajneesh Bhaskar")
    
    if st.button("🚀 Process Fast"):
        input_path = "input_video.mp4"
        output_path = "cleaned_video.mp4"
        
        # File save karna
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())
        
        with st.spinner("Processing... Ismein 1-2 minute lag sakte hain."):
            # 1. Base Filter Chain
            vf_chain = f"hflip,crop=iw*{zoom_level}:ih*{zoom_level},boxblur={blur_intensity}:enable='lt(y,ih/6)'"
            # 2. Text Watermark
            vf_chain += f",drawtext=text='{wm_name}':x=(w-text_w)/2:y=h-80:fontsize=40:fontcolor=white@0.5"
            
            # Check if Logo exists on GitHub server
            if os.path.exists(LOGO_FILE):
                # Complex filter for Logo + Text + Video edits
                cmd = [
                    'ffmpeg', '-y', '-i', input_path, '-i', LOGO_FILE,
                    '-filter_complex', f"[0:v]{vf_chain}[vbase];[1:v]scale=120:-1[logo];[vbase][logo]overlay=W-w-20:20",
                    '-af', f"atempo={audio_pitch}",
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28', '-threads', '0', '-c:a', 'aac',
                    output_path
                ]
            else:
                st.warning("⚠️ Logo file server par nahi mili. Bina logo ke process ho raha hai.")
                cmd = [
                    'ffmpeg', '-y', '-i', input_path,
                    '-vf', vf_chain,
                    '-af', f"atempo={audio_pitch}",
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28', '-threads', '0', '-c:a', 'aac',
                    output_path
                ]
            
            try:
                # Process run karna aur error capture karna
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                # Agar output file ban gayi hai
                if os.path.exists(output_path):
                    st.success("✅ Video taiyar hai!")
                    with open(output_path, "rb") as f:
                        st.download_button("📥 Download Branded Video", f, "rajneesh_video.mp4")
                else:
                    st.error("❌ Processing fail ho gayi.")
                    st.code(result.stderr) # Ye dikhayega ki FFmpeg kyu ruka
                    
            except Exception as e:
                st.error(f"System Error: {e}")
            finally:
                # Purani files delete karna taaki memory saaf rahe
                if os.path.exists(input_path): os.remove(input_path)



