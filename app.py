import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Rajneesh Movie Pro", layout="wide")
st.title("🎬 Rajneesh Bhaskar - Professional Shorts Creator")

# Logo file check
LOGO_FILE = "1642.jpg"

uploaded_file = st.file_uploader("Movie Upload Karein", type=['mp4', 'mkv'])

if uploaded_file:
    st.sidebar.header("✍️ Customize Your Hook")
    # Yahan aap apni pasand ki lines likh sakte hain
    line1 = st.sidebar.text_input("Top Line (Yellow Text)", "Yahan Pehli Line Likhein")
    line2 = st.sidebar.text_input("Bottom Line (White Text)", "Yahan Doosri Line Likhein")
    
    # Ultra HD Quality Settings
    st.sidebar.subheader("💎 Quality Settings")
    crf_val = st.sidebar.select_slider("Select Video Quality", options=["Standard", "High", "Ultra Pro"], value="High")
    crf_map = {"Standard": "22", "High": "18", "Ultra Pro": "16"}

    if st.button("🚀 Generate High-Quality Short"):
        input_p = "input_temp.mp4"
        output_p = "rajneesh_final_short.mp4"
        
        with open(input_p, "wb") as f:
            f.write(uploaded_file.read())
        
        with st.spinner("Professional layout taiyar ho raha hai..."):
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            
            # Professional 9:16 Layout Filter
            # 1. Video mirror (Hflip)
            # 2. HD Scaling (720 width)
            # 3. Padding (Black Bars Top & Bottom)
            # 4. Two-line Text (Yellow & White) with clean shadows
            vf_filters = (
                f"hflip,scale=720:-1,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black,"
                f"drawtext=text='{line1}':fontfile={font_path}:fontcolor=yellow:fontsize=42:x=(w-text_w)/2:y=130:shadowcolor=black:shadowx=2:shadowy=2,"
                f"drawtext=text='{line2}':fontfile={font_path}:fontcolor=white:fontsize=42:x=(w-text_w)/2:y=195:shadowcolor=black:shadowx=2:shadowy=2"
            )
            
            # Bottom Branding (Optional)
            footer = f"drawtext=text='Rajneesh Bhaskar':fontfile={font_path}:fontcolor=white@0.4:fontsize=26:x=(w-text_w)/2:y=h-120"

            if os.path.exists(LOGO_FILE):
                # Circular professional logo
                logo_f = "scale=80:80,format=rgba,geq=r='r(X,Y)':a='if(gt(hypot(X-W/2,Y-H/2),W/2),0,255)'"
                cmd = [
                    'ffmpeg', '-y', '-i', input_p, '-i', LOGO_FILE,
                    '-filter_complex', f"[0:v]{vf_filters},{footer}[v1];[1:v]{logo_f}[logo];[v1][logo]overlay=W-w-40:40",
                    '-af', "atempo=1.05",
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', crf_map[crf_val], 
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                    output_p
                ]
            else:
                cmd = ['ffmpeg', '-y', '-i', input_p, '-vf', f"{vf_filters},{footer}", '-af', "atempo=1.05", '-c:v', 'libx264', '-preset', 'slow', '-crf', crf_map[crf_val], output_p]
            
            res = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(output_p):
                st.success("✅ Professional Short Successfully Generated!")
                with open(output_p, "rb") as f:
                    st.download_button("📥 Download HQ Video", f, "rajneesh_pro_short.mp4")
            else:
                st.error("Error in processing!")
                st.code(res.stderr)
        
        if os.path.exists(input_p): os.remove(input_p)

