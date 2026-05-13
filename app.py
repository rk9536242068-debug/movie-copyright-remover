import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Movie Copyright Shield", layout="centered")

st.title("🎬 Movie Copyright Shield")
st.info("Ismein Flip + Crop + Logo Blur sab ek saath hoga.")

uploaded_file = st.file_uploader("Apni Movie Select Karein", type=['mp4', 'mkv', 'avi'])

if uploaded_file is not None:
    input_path = "input_video.mp4"
    output_path = "cleaned_video.mp4"
    
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())
    
    if st.button("Start Processing"):
        with st.spinner("Processing... Ismein thoda samay lagega."):
            # Command explain: 
            # hflip = Mirror
            # crop = Zoom/Crop
            # delogo = Logo area ko blur karna (x, y, w, h settings)
            filters = (
                "hflip,"
                "crop=iw*0.9:ih*0.9,"
                "delogo=x=0:y=0:w=iw/4:h=ih/8:band=1," # Left Top Blur
                "delogo=x=iw-iw/4:y=0:w=iw/4:h=ih/8:band=1" # Right Top Blur
            )
            
            cmd = [
                'ffmpeg', '-y', '-i', input_path,
                '-vf', filters,
                '-af', "atempo=1.05",
                '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28', '-c:a', 'aac',
                output_path
            ]
            
            try:
                subprocess.run(cmd, check=True)
                
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="Download Cleaned Movie",
                        data=f,
                        file_name="cleaned_movie.mp4",
                        mime="video/mp4"
                    )
                st.success("Kaam ho gaya! Dono corners blur ho gaye hain.")
                
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(input_path): os.remove(input_path)
                if os.path.exists(output_path): os.remove(output_path)
