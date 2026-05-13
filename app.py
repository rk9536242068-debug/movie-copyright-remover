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
    blur_area = st.sidebar.slider("Upper Blur Area", 0.1, 0.3, 0.15)
    
    if st.button("🚀 Process Perfect Video"):
        input_p = "input.mp4"
        output_p = "output.mp4"
        
        with open(input_p, "wb") as f:
            f.write(uploaded_file.read())
        
        with st.spinner("Logo ko Gol kiya ja raha hai aur patti set ho rahi hai..."):
            # 1. Video Flip, Zoom, Blur patti aur Black Box
            vf_chain = f"hflip,crop=iw*{zoom_val}:ih*{zoom_val},split[main][blur];[blur]boxblur=25,crop=iw:ih*{blur_area}:0:0[blurred];[main][blurred]overlay=0:0,drawbox=y=ih-140:color=black@1:width=iw:height=140:t=fill"
            
            # 2. Aapka naam patti ke upar
            my_name = "drawtext=text='Rajneesh Bhaskar':x=(w-text_w)/2:y=h-95:fontsize=55:fontcolor=yellow:shadowcolor=black:shadowx=2:shadowy=2"
            
            if os.path.exists(LOGO_FILE):
                # LOGO KO GOL KARNE KA MAGIC:
                # scale=100:-1 se logo chhota hoga (100px width)
                # geq filter se circle mask banega
                logo_filter = (
                    "scale=100:100,format=rgba,geq=r='r(X,Y)':a='if(gt(hypot(X-W/2,Y-H/2),W/2),0,255)'"
                )
                
                cmd = [
                    'ffmpeg', '-y', '-i', input_p, '-i', LOGO_FILE,
                    '-filter_complex', f"[0:v]{vf_chain},{my_name}[v1];[1:v]{logo_filter}[logo];[v1][logo]overlay=W-w-25:25",
                    '-af', "atempo=1.05",
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '22', '-c:a', 'aac',
                    output_p
                ]
            else:
                st.warning("Logo file nahi mili!")
                cmd = ['ffmpeg', '-y', '-i', input_p, '-vf', f"{vf_chain},{my_name}", '-af', "atempo=1.05", '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '22', output_p]
            
            res = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(output_p):
                st.success("✅ Gol Logo aur Patti dono set hain!")
                with open(output_p, "rb") as f:
                    st.download_button("📥 Download Final Video", f, "rajneesh_final_pro.mp4")
            else:
                st.error("Error aaya!")
                st.code(res.stderr)
        
        if os.path.exists(input_p): os.remove(input_p)



