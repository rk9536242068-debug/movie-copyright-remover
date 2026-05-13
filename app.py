import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Movie Copyright Fixer", layout="wide")
st.title("🎬 Full Movie Copyright Remover")
st.info("Ye cloud par process hoga, isliye mobile crash nahi hoga.")

uploaded_file = st.file_uploader("Apni Movie Select Karein", type=['mp4', 'mkv', 'avi'])

if uploaded_file:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())
    st.success("Upload Complete! Ab niche button dabayein.")

    if st.button("Start Processing (Full Movie)"):
        with st.spinner("Processing... Movie badi hai toh 15-20 min lag sakte hain."):
            output = "final_movie.mp4"
            # Command for Full Movies
            cmd = f'ffmpeg -y -i input.mp4 -vf "hflip,scale=1.1*iw:-1,crop=iw/1.1:ih/1.1" -af "asetrate=44100*1.05,atempo=1/1.05" -c:v libx264 -preset ultrafast -crf 28 {output}'
            
            os.system(cmd)
            
            if os.path.exists(output):
                with open(output, "rb") as file:
                    st.download_button("⬇️ Download Full Movie", file, file_name="copyright_free.mp4")
            else:
                st.error("Processing fail ho gayi. File size check karein.")
