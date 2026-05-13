import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Rajneesh Movie Pro", layout="wide")
st.title("🎬 Rajneesh Bhaskar - Professional Shorts Creator")

LOGO_FILE = "1642.jpg"

uploaded_file = st.file_uploader("Movie Select Karein", type=['mp4', 'mkv'])

if uploaded_file:
    st.sidebar.header("✍️ Customize Text")
    line1 = st.sidebar.text_input("Top Line (Yellow)", "Pehli Line Likhein")
    line2 = st.sidebar.text_input("Bottom Line (White)", "Doosri Line Likhein")
    
    if st.button("🚀 Fix & Generate Video"):
        input_p = "raw_input.mp4"
        output_p = "clean_output.mp4"
        
        with open(input_p, "wb") as f:
            f.write(uploaded_file.read())
        
        with st.spinner("Sari gandagi saaf karke branded video ban rahi hai..."):
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            
            # STEP-BY-STEP CLEANING:
            # 1. crop=iw:ih-300:0:150 -> Isse upar aur niche ka 150-150px hissa (purane logo) kat jayega.
            # 2. scale=720:-1 -> Video ki width 720px karega.
            # 3. pad=720:1280... -> Nayi saaf black bars lagayega.
            clean_vf = (
                f"hflip,crop=iw:ih-300:0:150,scale=720:-1,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black,"
                f"drawtext=text='{line1}':fontfile={font_path}:fontcolor=yellow:fontsize=44:x=(w-text_w)/2:y=150,"
                f"drawtext=text='{line2}':fontfile={font_path}:fontcolor=white:fontsize=44:x=(w-text_w)/2:y=215"
            )
            
            footer = f"drawtext=text='Rajneesh Bhaskar':fontfile={font_path}:fontcolor=white@0.5:fontsize=30:x=(w-text_w)/2:y=h-150"

            if os.path.exists(LOGO_FILE):
                logo_f = "scale=90:90,format=rgba,geq=r='r(X,Y)':a='if(gt(hypot(X-W/2,Y-H/2),W/2),0,255)'"
                cmd = [
                    'ffmpeg', '-y', '-i', input_p, '-i', LOGO_FILE,
                    '-filter_complex', f"[0:v]{clean_vf},{footer}[v1];[1:v]{logo_f}[logo];[v1][logo]overlay=W-w-40:40",
                    '-af', "atempo=1.06",
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '18', '-pix_fmt', 'yuv420p',
                    output_p
                ]
            else:
                cmd = ['ffmpeg', '-y', '-i', input_p, '-vf', f"{clean_vf},{footer}", '-af', "atempo=1.06", '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '18', output_p]
            
            res = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(output_p):
                st.success("✅ Saaf aur Professional Video Taiyar!")
                with open(output_p, "rb") as f:
                    st.download_button("📥 Download Final Short", f, "rajneesh_pro_short.mp4")
            else:
                st.error("Kuch gadbad hai!")
                st.code(res.stderr)
        
        if os.path.exists(input_p): os.remove(input_p)
