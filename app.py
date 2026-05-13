import streamlit as st
import subprocess
import os

# =========================================
# PAGE SETTINGS
# =========================================

st.set_page_config(
    page_title="Rajneesh Bhaskar Shorts Creator",
    layout="wide"
)

st.title("🎬 Rajneesh Bhaskar - Professional Shorts Creator")

# =========================================
# LOGO FILE
# =========================================

LOGO_FILE = "1642.jpg"

# =========================================
# VIDEO UPLOAD
# =========================================

uploaded_file = st.file_uploader(
    "📤 Upload Movie / Video",
    type=["mp4", "mkv", "mov", "avi"]
)

# =========================================
# MAIN APP
# =========================================

if uploaded_file:

    st.sidebar.header("✍️ Hook Text Settings")

    line1 = st.sidebar.text_input(
        "Yellow Hook Line",
        "Yahan Pehli Line Likhein"
    )

    line2 = st.sidebar.text_input(
        "White Hook Line",
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

    speed_boost = st.sidebar.checkbox(
        "⚡ Slight Speed Boost",
        value=True
    )

    # =========================================
    # GENERATE BUTTON
    # =========================================

    if st.button("🚀 Generate Professional Short"):

        input_video = "input_temp.mp4"
        output_video = "rajneesh_final_short.mp4"

        # Save uploaded video
        with open(input_video, "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("🎞️ Professional Short Ban Raha Hai..."):

            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

            # =========================================
            # VIDEO FILTERS
            # =========================================

            vf_filters = (

                # Full vertical crop
                f"scale=720:1280:force_original_aspect_ratio=increase,"
                f"crop=720:1280,"

                # =========================================
                # TOP BLACK BOX
                # =========================================

                f"drawbox=x=0:y=0:w=720:h=240:color=black:t=fill,"

                # =========================================
                # BOTTOM BLACK BOX
                # =========================================

                f"drawbox=x=0:y=1080:w=720:h=200:color=black:t=fill,"

                # =========================================
                # YELLOW TOP TEXT
                # =========================================

                f"drawtext=text='{line1}':"
                f"fontfile={font_path}:"
                f"fontcolor=#ffcc00:"
                f"fontsize=46:"
                f"x=(w-text_w)/2:"
                f"y=60:"
                f"borderw=4:"
                f"bordercolor=black,"

                # =========================================
                # WHITE SECOND TEXT
                # =========================================

                f"drawtext=text='{line2}':"
                f"fontfile={font_path}:"
                f"fontcolor=white:"
                f"fontsize=42:"
                f"x=(w-text_w)/2:"
                f"y=130:"
                f"borderw=4:"
                f"bordercolor=black,"

                # =========================================
                # REMOVE OLD CHANNEL NAME AREA
                # =========================================

                f"drawbox=x=0:y=930:w=720:h=150:color=black:t=fill,"

                # =========================================
                # YOUR CHANNEL NAME
                # =========================================

                f"drawtext=text='Rajneesh Bhaskar':"
                f"fontfile={font_path}:"
                f"fontcolor=white:"
                f"fontsize=58:"
                f"x=(w-text_w)/2:"
                f"y=960:"
                f"borderw=5:"
                f"bordercolor=black,"

                # =========================================
                # FOOTER WATERMARK
                # =========================================

                f"drawtext=text='@rajneesh_pro_shorts':"
                f"fontfile={font_path}:"
                f"fontcolor=white@0.35:"
                f"fontsize=24:"
                f"x=(w-text_w)/2:"
                f"y=h-45"
            )

            # =========================================
            # AUDIO SPEED
            # =========================================

            audio_filter = "atempo=1.05" if speed_boost else "atempo=1.0"

            # =========================================
            # LOGO FILTER
            # =========================================

            if os.path.exists(LOGO_FILE):

                logo_filter = (
                    "scale=85:85,"
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
                    f"[v1][logo]overlay=W-w-20:20",

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

            # =========================================
            # RUN FFMPEG
            # =========================================

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            # =========================================
            # SUCCESS OUTPUT
            # =========================================

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

                st.error("❌ Video Processing Error")

                st.code(result.stderr)

        # =========================================
        # CLEAN TEMP FILE
        # =========================================

        if os.path.exists(input_video):
            os.remove(input_video)

