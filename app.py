import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Rajneesh Pro Shield", layout="wide")
st.title("🚀 Rajneesh Bhaskar - Professional Movie Shield")

LOGO_FILE = "1642.jpg"

uploaded_file = st.file_uploader("Movie Upload Karein", type=['mp4', 'mkv'])

if uploaded_file:
    st.sidebar.header("⚙️ Settings")
    zoom_val = st.sidebar.slider("Zoom Level", 0.8, 1.0, 0.9)
    # 0.15 matlab sirf upar ka 15% hissa blur hoga
    blur_area = st.sidebar.slider("Upper Blur Area", 0.1, 0.3, 0.15)
    
    if st.button("🚀 Process Perfect Video"):
        input_p = "input.mp4"
        output_p = "output.mp4"
        
        with open(input_p, "wb") as f:
            f.write(uploaded_file.read())
        
        with st.spinner("Video saaf aur branded ban rahi hai..."):
            # Sabse aasaan aur pakka tarika:
            # 1. Video ko flip aur crop karo
            # 2. Crop ke baad sirf upar ke hisse par blur lagao
            # Is baar hum math calculation ko simple string mein bhej rahe hain
            
            vf_chain = f"hflip,crop=iw*{zoom_val}:ih*{zoom_val},split[main][blur];[blur]boxblur=25,crop=iw:ih*{blur_area}:0:0[blurred];[main][blurred]overlay=0:0"
            my_name = "drawtext=text='Rajneesh Bhaskar':x=(w-text_w)/2:y=h-100:fontsize=45:fontcolor=yellow:shadowcolor=black:shadowx=2:shadowy=2"
            
            if os.path.exists(LOGO_FILE):
                # Filter complex for Logo + Selective Blur + Text
                cmd = [
                    'ffmpeg', '-y', '-i', input_p, '-i', LOGO_FILE,
                    '-filter_complex', f"[0:v]{vf_chain},{my_name}[v1];[1:v]scale=130:-1[logo];[v1][logo]overlay=W-w-20:20",
                    '-af', "atempo=1.05",
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '22', '-c:a', 'aac',
                    output_p
                ]
            else:
                cmd = ['ffmpeg', '-y', '-i', input_p, '-vf', f"{vf_chain},{my_name}", '-af', "atempo=1.05", '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '22', output_p]
            
            res = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(output_p):
                st.success("✅ Video Taiyar Hai!")
                with open(output_p, "rb") as f:
                    st.download_button("📥 Download Clean Video", f, "rajneesh_perfect.mp4")
            else:
                st.error("Kuch gadbad hui!")
                st.code(res.stderr)
        
        if os.path.exists(input_p): os.remove(input_p)


