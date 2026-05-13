import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Rajneesh Pro Shield", layout="wide")
st.title("🚀 Rajneesh Bhaskar - Ultimate Movie Shield")

LOGO_FILE = "1642.jpg"

uploaded_file = st.file_uploader("Movie Upload Karein", type=['mp4', 'mkv'])

if uploaded_file:
    st.sidebar.header("⚙️ Adjustment Settings")
    # Purane logo ko dhakne ke liye blur height badhao
    blur_height = st.sidebar.slider("Purana Logo Blur Area (Height)", 0.1, 0.3, 0.18)
    zoom_val = st.sidebar.slider("Zoom/Crop", 0.8, 1.0, 0.9)
    
    if st.button("🚀 Process & Add My Branding"):
        input_p = "input.mp4"
        output_p = "output.mp4"
        
        with open(input_p, "wb") as f:
            f.write(uploaded_file.read())
        
        with st.spinner("Processing... Logo aur Naam add ho raha hai."):
            # 1. Sabse pehle Mirror aur Crop (Zoom)
            # 2. Phir Purana logo hatane ke liye bada Blur area
            # 3. Phir aapka text 'Rajneesh Bhaskar'
            base_vf = f"hflip,crop=iw*{zoom_val}:ih*{zoom_val},boxblur=25:enable='lt(y,ih*{blur_height})'"
            my_name = "drawtext=text='Rajneesh Bhaskar':x=(w-text_w)/2:y=h-100:fontsize=50:fontcolor=yellow:shadowcolor=black:shadowx=2:shadowy=2"
            
            if os.path.exists(LOGO_FILE):
                # AGAR LOGO HAI: Filter Complex use karenge
                # [0:v] video, [1:v] aapka logo
                cmd = [
                    'ffmpeg', '-y', '-i', input_p, '-i', LOGO_FILE,
                    '-filter_complex', 
                    f"[0:v]{base_vf},{my_name}[v1];[1:v]scale=150:-1[logo];[v1][logo]overlay=W-w-30:30",
                    '-af', "atempo=1.05",
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '24', '-c:a', 'aac',
                    output_p
                ]
            else:
                st.warning("Logo file (1642.jpg) nahi mili! Sirf naam likha jayega.")
                cmd = [
                    'ffmpeg', '-y', '-i', input_p,
                    '-vf', f"{base_vf},{my_name}",
                    '-af', "atempo=1.05",
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '24', '-c:a', 'aac',
                    output_p
                ]
            
            res = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(output_p):
                st.success("Branding Successful!")
                with open(output_p, "rb") as f:
                    st.download_button("📥 Download Branded Video", f, "rajneesh_final.mp4")
            else:
                st.error("Error: Video process nahi hui.")
                st.code(res.stderr)
        
        if os.path.exists(input_p): os.remove(input_p)



