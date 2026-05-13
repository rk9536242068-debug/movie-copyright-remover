import streamlit as st
import subprocess
import os
import tempfile

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Rajneesh Logo Shield Pro",
    page_icon="🛡️",
    layout="wide",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    body { background: #0d0d0d; }
    .main { background: #0d0d0d; }
    h1 { color: #f5c518 !important; letter-spacing: 1px; }
    .stButton > button {
        background: linear-gradient(135deg, #f5c518, #e0a800);
        color: #000;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.4rem;
        font-size: 1rem;
        transition: 0.2s;
    }
    .stButton > button:hover { opacity: 0.88; transform: scale(1.02); }
    .info-box {
        background: #1a1a2e;
        border-left: 4px solid #f5c518;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 10px;
        color: #ccc;
        font-size: 0.9rem;
    }
    .stDownloadButton > button {
        background: #22c55e;
        color: #fff;
        font-weight: 700;
        border-radius: 8px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TITLE
# ─────────────────────────────────────────────
st.title("🛡️ Rajneesh Bhaskar — Professional Logo Shield")
st.caption("Purana copyright / watermark hataiye, apna brand lagaiye — ek click mein.")

st.divider()

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
LOGO_FILE = "1642.jpg"

def find_font():
    """Return a valid font path or empty string."""
    candidates = [
        FONT_PATH,
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return ""

def build_ffmpeg_cmd(
    input_p: str,
    output_p: str,
    crop_top: int,
    crop_bottom: int,
    flip: bool,
    line1: str,
    line2: str,
    footer: str,
    speed: float,
    font_path: str,
    logo_path: str | None,
) -> list[str]:
    """Build the ffmpeg command based on user settings."""

    total_crop = crop_top + crop_bottom
    # Crop: remove top & bottom bands that carry watermarks
    # scale back to 720 wide, pad to 1280 tall (portrait)
    crop_filter = (
        f"crop=iw:ih-{total_crop}:0:{crop_top},"
        f"scale=720:-2,"
        f"pad=720:1280:(ow-iw)/2:(oh-ih)/2:black"
    )

    flip_filter = "hflip," if flip else ""

    # Text overlays (only if text provided)
    text_filters = []
    if line1 and font_path:
        safe1 = line1.replace("'", "\\'")
        text_filters.append(
            f"drawtext=text='{safe1}':fontfile={font_path}:"
            f"fontcolor=yellow:fontsize=45:x=(w-text_w)/2:y=145:"
            f"shadowcolor=black:shadowx=2:shadowy=2"
        )
    if line2 and font_path:
        safe2 = line2.replace("'", "\\'")
        text_filters.append(
            f"drawtext=text='{safe2}':fontfile={font_path}:"
            f"fontcolor=white:fontsize=42:x=(w-text_w)/2:y=205:"
            f"shadowcolor=black:shadowx=2:shadowy=2"
        )
    if footer and font_path:
        safeF = footer.replace("'", "\\'")
        text_filters.append(
            f"drawtext=text='{safeF}':fontfile={font_path}:"
            f"fontcolor=white@0.45:fontsize=28:x=(w-text_w)/2:y=h-130:"
            f"shadowcolor=black:shadowx=1:shadowy=1"
        )

    text_chain = (",".join(text_filters) + ",") if text_filters else ""

    main_filter = f"{flip_filter}{crop_filter},{text_chain.rstrip(',')}"

    audio_filter = f"atempo={speed:.2f}" if speed != 1.0 else ""

    if logo_path and os.path.exists(logo_path):
        logo_proc = (
            "scale=85:85,format=rgba,"
            "geq=r='r(X,Y)':a='if(gt(hypot(X-W/2,Y-H/2),W/2),0,255)'"
        )
        fc = (
            f"[0:v]{main_filter}[v1];"
            f"[1:v]{logo_proc}[logo];"
            f"[v1][logo]overlay=W-w-35:35"
        )
        cmd = [
            "ffmpeg", "-y",
            "-i", input_p, "-i", logo_path,
            "-filter_complex", fc,
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-i", input_p,
            "-vf", main_filter,
        ]

    if audio_filter:
        cmd += ["-af", audio_filter]

    cmd += [
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        output_p,
    ]
    return cmd

# ─────────────────────────────────────────────
#  LAYOUT  (col1 = upload + settings | col2 = info)
# ─────────────────────────────────────────────
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("📁 Video Upload")
    uploaded_file = st.file_uploader(
        "MP4 ya MKV video chuniye",
        type=["mp4", "mkv", "avi", "mov"],
        label_visibility="collapsed",
    )

with col2:
    st.markdown("""
    <div class='info-box'>
    <b>Yeh tool kya karta hai?</b><br>
    ✂️ Video ke upar/niche se watermark crop karta hai<br>
    🔄 Optional mirror flip<br>
    ✍️ Aapka custom text daalta hai<br>
    🖼️ Aapka logo (1642.jpg) round shape mein laata hai<br>
    ⚡ Speed adjust karta hai
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────
#  SETTINGS  (only show if file uploaded)
# ─────────────────────────────────────────────
if uploaded_file:
    st.subheader("⚙️ Settings")

    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown("**✂️ Crop (pixels)**")
        crop_top    = st.slider("Upar se kato (top crop)", 0, 300, 120, 10)
        crop_bottom = st.slider("Niche se kato (bottom crop)", 0, 300, 120, 10)

    with s2:
        st.markdown("**✍️ Text Overlay**")
        line1  = st.text_input("Top line (Yellow)",  "Pehli Line Likhein")
        line2  = st.text_input("Middle line (White)", "Doosri Line Likhein")
        footer = st.text_input("Footer (Watermark)",  "Rajneesh Bhaskar")

    with s3:
        st.markdown("**🎬 Video Options**")
        flip  = st.checkbox("🔄 Mirror Flip (hflip)", value=True)
        speed = st.slider("⚡ Audio Speed", 0.80, 1.50, 1.06, 0.01)
        st.caption("1.0 = normal speed")

    st.divider()

    # ─────────────────────────────────────────
    #  PROCESS BUTTON
    # ─────────────────────────────────────────
    if st.button("🚀 Logo Hatao & Video Process Karo", use_container_width=True):

        font_path = find_font()
        if not font_path:
            st.warning("⚠️ Font file nahi mili. Text overlay skip hoga.")

        input_p  = os.path.join(tempfile.gettempdir(), "rj_input.mp4")
        output_p = os.path.join(tempfile.gettempdir(), "rj_output.mp4")

        # Save uploaded file
        with open(input_p, "wb") as f:
            f.write(uploaded_file.read())

        logo_path = LOGO_FILE if os.path.exists(LOGO_FILE) else None

        cmd = build_ffmpeg_cmd(
            input_p=input_p,
            output_p=output_p,
            crop_top=crop_top,
            crop_bottom=crop_bottom,
            flip=flip,
            line1=line1,
            line2=line2,
            footer=footer,
            speed=speed,
            font_path=font_path,
            logo_path=logo_path,
        )

        # Show command (debug)
        with st.expander("🔧 FFmpeg command (debug ke liye)"):
            st.code(" ".join(cmd), language="bash")

        with st.spinner("⏳ Processing ho raha hai... thoda wait karein"):
            res = subprocess.run(cmd, capture_output=True, text=True)

        if os.path.exists(output_p) and os.path.getsize(output_p) > 1000:
            st.success("✅ Sab ho gaya! Purana logo/watermark 100% remove!")

            # Show file size
            size_mb = os.path.getsize(output_p) / (1024 * 1024)
            st.info(f"📦 Output size: **{size_mb:.1f} MB**")

            with open(output_p, "rb") as f:
                st.download_button(
                    label="📥 Clean Video Download Karein",
                    data=f,
                    file_name="rajneesh_final.mp4",
                    mime="video/mp4",
                    use_container_width=True,
                )
        else:
            st.error("❌ Processing fail hua. Niche error dekho:")
            st.code(res.stderr[-3000:], language="bash")  # last 3000 chars

        # Cleanup temp files
        for p in [input_p, output_p]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

else:
    st.info("👆 Upar video upload karein, phir settings aayengi.")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.divider()
st.caption("🛡️ Rajneesh Bhaskar — Professional
