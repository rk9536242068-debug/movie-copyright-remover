import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Rajneesh Movie Shield", layout="wide")

st.title("🚀 Rajneesh Bhaskar - Pro Movie Shield")

# Logo file check
LOGO_FILE = "1642.jpg"

uploaded_file = st.file_uploader("Movie Upload Karein", type=['mp4', 'mkv'])

if uploaded_file:
    # --- Sidebar Controls ---
    st.sidebar.header("⚙️ Smart Settings")
    zoom_level = st.sidebar.slider("Zoom Level", 0.7, 1.0, 0.9)
    blur_intensity = st.sidebar.slider("Blur Intensity", 5, 50, 20)
    audio_pitch = st.sidebar.slider("Audio Speed", 1.0, 1.2, 1.05)
    
    # Text input for your name
    wm_name = st.sidebar.text_input("Branding Name", "Rajneesh Bhaskar")
    
    if st.button("🚀 Process with Logo & Watermark"):
        input_path = "input.mp4"
        output_path = "output.mp4"
        with open(input_path, "wb") as f: f.write(uploaded_file.read())
        
        with st.spinner("Logo aur Branding add ho rahi hai..."):
            
            # Base filters: Flip, Crop, Top Blur
            vf_chain = f"hflip,crop=iw*{zoom_level}:ih*{zoom_level},boxblur={blur_intensity}:enable='lt(y,ih/6)'"
            
            # Adding Watermark Text (Rajneesh Bhaskar)
            vf_chain += f",drawtext=text='{wm_name}':x=(w-text_w)/2:y=h-80:fontsize=45:fontcolor=white@0.6"
            
            # Adding Image Logo (1642.jpg) if exists
            if os.path.exists(LOGO_FILE):
                # Logo ko chota karke (150 width) top right mein lagayega
                cmd = [
                    'ffmpeg', '-y', '-i', input_path, '-i', LOGO_FILE,
                    '-filter_complex', 
                    f"[0:v]{vf_chain}[vbase];[1:v]scale=150:-1[logo];[vbase][logo]overlay=main_w-overlay_w-20:20",
                    '-af', f"atempo={audio_pitch}",
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', 
                    output_path
                ]
            else:
                st.warning("Logo file (1642.jpg) nahi mili, sirf text watermark lagega.")
                cmd = ['ffmpeg', '-y', '-i', input_path, '-vf', vf_chain, '-af', f"atempo={audio_pitch}", output_path]
            
            subprocess.run(cmd)
            
            with open(output_path, "rb") as f:
                st.download_button("✅ Download Branding Video", f, "rajneesh_branded.mp4")
            
            os.remove(input_path)


