import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Rajneesh Pro Shield", layout="wide")
st.title("🚀 Rajneesh Bhaskar - Ultimate Movie Shield")

# Logo file check
LOGO_FILE = "1642.jpg"

uploaded_file = st.file_uploader("Movie Upload Karein", type=['mp4', 'mkv'])

if uploaded_file:
    st.sidebar.header("⚙️ Adjustment Settings")
    zoom_val = st.sidebar.slider("Zoom/Crop", 0.8, 1.0, 0.9)
    
    if st.button("🚀 Process & Add My Branding"):
        input_p = "input.mp4"
        output_p = "output.mp4"
        
        with open(input_p, "wb") as f:
            f.write(uploaded_file.read())
        
        with st.spinner("Processing... Is baar fix ho gaya hai!"):
            # Simple Filter Chain: Hflip + Crop + Blur + Your Name
            # Boxblur=10 pure video par halka blur daalega jo copyright ke liye zaruri hai
            vf_chain = f"hflip,crop=iw*{zoom_val}:ih*{zoom_val},boxblur=10"
            my_name = "drawtext=text='Rajneesh Bhaskar':x=(w-text_w)/2:y=h-100:fontsize=45:fontcolor=yellow:shadowcolor=black:shadowx=2:shadowy=2"
            
            if os.path.exists(LOGO_FILE):
                # Filter complex with logo overlay
                cmd = [
                    'ffmpeg', '-y', '-i', input_p, '-i', LOGO_FILE,
                    '-filter_complex', f"[0:v]{vf_chain},{my_name}[v1];[1:v]scale=150:-1[logo];[v1][logo]overlay=W-w-30:30",
                    '-af', "atempo=1.05",
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '26', '-c:a', 'aac',
                    output_p
                ]
            else:
                st.warning("⚠️ Logo file (1642.jpg) nahi mili, sirf naam likha jayega.")
                cmd = [
                    'ffmpeg', '-y', '-i', input_p,
                    '-vf', f"{vf_chain},{my_name}",
                    '-af', "atempo=1.05",
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '26', '-c:a', 'aac',
                    output_p
                ]
            
            res = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(output_p):
                st.success("✅ Branding Successful!")
                with open(output_p, "rb") as f:
                    st.download_button("📥 Download Branded Video", f, "rajneesh_final.mp4")
            else:
                st.error("Error: Video process nahi hui.")
                st.code(res.stderr)
        
        if os.path.exists(input_p): os.remove(input_p)

