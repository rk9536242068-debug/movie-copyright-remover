
import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Rajneesh Logo Remover", layout="wide")
st.title("🛡️ Rajneesh Bhaskar - Professional Logo Shield")

LOGO_FILE = "1642.jpg"

uploaded_file = st.file_uploader("Video Upload Karein", type=['mp4', 'mkv'])

if uploaded_file:
    st.sidebar.header("✍️ Text Settings")
    line1 = st.sidebar.text_input("Top Line (Yellow)", "Pehli Line Likhein")
    line2 = st.sidebar.text_input("Bottom Line (White)", "Doosri Line Likhein")
    
    if st.button("🚀 Remove Old Logo & Process"):
        input_p = "input_video.mp4"
        output_p = "rajneesh_cleaned.mp4"
        
        with open(input_p, "wb") as f:
            f.write(uploaded_file.read())
        
        with st.spinner("Purana logo kaat kar naya layout banaya ja raha hai..."):
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            
            # LOGIC: 
            # 1. crop=iw:ih-240:0:120 -> Isse video ke upar aur niche se 120-120 pixels kaat diye jayenge (Jahan purana logo hota hai).
            # 2. scale=720:-1 -> Video quality ko HD standard par set karega.
            # 3. pad=720:1280... -> Nayi fresh black patti lagayega jisme koi purana nishaan nahi hoga.
            
            clean_filter = (
                f"hflip,crop=iw:ih-240:0:120,scale=720:-1,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black,"
                f"drawtext=text='{line1}':fontfile={font_path}:fontcolor=yellow:fontsize=45:x=(w-text_w)/2:y=140:shadowcolor=black:shadowx=2:shadowy=2,"
                f"drawtext=text='{line2}':fontfile={font_path}:fontcolor=white:fontsize=45:x=(w-text_w)/2:y=200:shadowcolor=black:shadowx=2:shadowy=2"
            )
            
            footer_text = f"drawtext=text='Rajneesh Bhaskar':fontfile={font_path}:fontcolor=white@0.4:fontsize=28:x=(w-text_w)/2:y=h-130"

            if os.path.exists(LOGO_FILE):
                # Aapka gol logo
                logo_proc = "scale=85:85,format=rgba,geq=r='r(X,Y)':a='if(gt(hypot(X-W/2,Y-H/2),W/2),0,255)'"
                
                cmd = [
                    'ffmpeg', '-y', '-i', input_p, '-i', LOGO_FILE,
                    '-filter_complex', f"[0:v]{clean_filter},{footer_text}[v1];[1:v]{logo_proc}[logo];[v1][logo]overlay=W-w-35:35",
                    '-af', "atempo=1.06",
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '18', '-pix_fmt', 'yuv420p',
                    output_p
                ]
            else:
                cmd = ['ffmpeg', '-y', '-i', input_p, '-vf', f"{clean_filter},{footer_text}", '-af', "atempo=1.06", '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '18', output_p]
            
            res = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(output_p):
                st.success("✅ Purana logo 100% remove ho gaya hai!")
                with open(output_p, "rb") as f:
                    st.download_button("📥 Download Clean Video", f, "rajneesh_final.mp4")
            else:
                st.error("Processing mein error aaya.")
                st.code(res.stderr)
        
        if os.path.exists(input_p): os.remove(input_p)
