import streamlit as st
import subprocess
import os

# =========================
# PAGE SETTINGS
# =========================
st.set_page_config(page_title="Rajneesh Movie Pro", layout="wide")

st.title("🎬 Rajneesh Bhaskar - Professional Shorts Creator")
st.write("Upload movie/video and create cinematic YouTube Shorts automatically.")

# =========================
# FILES
# =========================
LOGO_FILE = "1642.jpg"

uploaded_file = st.file_uploader(
    "📤 Movie Upload Karein",
    type=["mp4", "mkv", "mov", "avi"]
)

# =========================
# SIDEBAR SETTINGS
# =========================
if uploaded_file:

    st.sidebar.header("✍️ Customize Your Hook")

    line1 = st.sidebar.text_input(
        "Top Line (Yellow Text)",
        "Yahan Pehli Line Likhein"
    )

    line2 = st.sidebar.text_input(
        "Bottom Line (White Text)",
        "Yahan Doosri Line Likhein"
    )

    st.sidebar.subheader("💎 Video Quality")

    quality = st.sidebar.select_slider(
        "Select Quality",
        options=["Standard", "High", "Ultra Pro"],
        value="High"
    )

    crf_map = {
        "Standard": "24",
        "High": "20",
        "Ultra Pro": "16"
    }

    add_speed = st.sidebar.checkbox(
        "⚡ Slight Speed Boost",
        value=True
    )

    # =========================
    # GENERATE BUTTON
    # =========================
    if st.button("🚀 Generate Professional Short"):

        input_video = "input_temp.mp4"
        output_video = "rajneesh_final_short.mp4"

        # Save uploaded video
        with open(input_video, "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("🎞️ Professional Short Taiyar Ho Raha Hai..."):

            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

            # =========================
            # VIDEO FILTERS
            # =========================

            vf_filters = (
                f"scale=720:1280:force_original_aspect_ratio=increase,"
                f"crop=720:1280,"

                # Top cinematic black box
                f"drawbox=x=0:y=0:w=720:h=250:color=black:t=fill,"

                # Yellow text
                f"drawtext=text='{line1}':"
                f"fontfile={font_path}:"
                f"fontcolor=#ffcc00:"
                f"fontsize=48:"
                f"x=(w-text_w)/2:"
                f"y=65:"
                f"borderw=4:"
                f"bordercolor=black,"

                # White text
                f"drawtext=text='{line2}':"
                f"fontfile={font_path}:"
                f"fontcolor=white:"
                f"fontsize=44:"
                f"x=(w-text_w)/2:"
                f"y=140:"
                f"borderw=4:"
                f"bordercolor=black,"

                # Bottom branding
                f"drawtext=text='Rajneesh Bhaskar':"
                f"fontfile={font_path}:"
                f"fontcolor=white@0.40:"
                f"fontsize=26:"
                f"x=(w-text_w)/2:"
                f"y=h-80"
            )

            # =========================
            # AUDIO SPEED
            # =========================

            audio_filter = "atempo=1.05" if add_speed else "atempo=1.0"

            # =========================
            # LOGO EFFECT
            # =========================

            if os.path.exists(LOGO_FILE):

                logo_filter = (
                    "scale=90:90,"
                    "format=rgba,"
                    "geq=r='r(X,Y)':"
                    "a='if(gt(hypot(X-W/2,Y-H/2),W/2),0,255)'"
                )

                cmd = [
                    "ffmpeg",
                    "-y",
                    "-i", input_video,
                    "-i", LOGO_FILE,

                    "-filter_complex",
                    f"[0:v]{vf_filters}[v1];"
                    f"[1:v]{logo_filter}[logo];"
                    f"[v1][logo]overlay=W-w-30:30",

                    "-af", audio_filter,

                    "-c:v", "libx264",
                    "-preset", "slow",
                    "-crf", crf_map[quality],

                    "-pix_fmt", "yuv420p",

                    "-c:a", "aac",
                    "-b:a", "192k",

                    output_video
                ]

            else:

                cmd = [
                    "ffmpeg",
                    "-y",
                    "-i", input_video,

                    "-vf", vf_filters,

                    "-af", audio_filter,

                    "-c:v", "libx264",
                    "-preset", "slow",
                    "-crf", crf_map[quality],

                    "-pix_fmt", "yuv420p",

                    "-c:a", "aac",
                    "-b:a", "192k",

                    output_video
                ]

            # =========================
            # RUN FFMPEG
            # =========================

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            # =========================
            # OUTPUT
            # =========================

            if os.path.exists(output_video):

                st.success("✅ Professional Short Successfully Generated!")

                st.video(output_video)

                with open(output_video, "rb") as f:

                    st.download_button(
                        "📥 Download HQ Video",
                        f,
                        file_name="rajneesh_pro_short.mp4"
                    )

            else:

                st.error("❌ Error in Video Processing")

                st.code(result.stderr)

        # =========================
        # CLEANUP
        # =========================

        if os.path.exists(input_video):
            os.remove(input_video)

