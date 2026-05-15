import os
from flask import Flask, request, render_template, send_file
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html lang="en">
    <head><title>Instant Copyright Shield</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 50px;">
        <h2>Instant Video Shield & Unique Modifier</h2>
        <form action="/process" method="post" enctype="multipart/form-data">
            <input type="file" name="video" required><br><br>
            <button type="submit" style="padding: 10px 20px;">Process Video Instantly</button>
        </form>
    </body>
    </html>
    '''

@app.route('/process', method=['POST'])
def process_video():
    if 'video' not in request.files:
        return "No video file found", 400
    
    file = request.files['video']
    if file.filename == '':
        return "No selected file", 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, "shielded_" + file.filename)
    file.save(input_path)

    # FFmpeg Powerful Command to alter metadata, pitch, scale, and speed instantly
    # vf: video filter (halka speed, scale aur contrast changes)
    # af: audio filter (pitch aur tempo adjust)
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vf', 'setpts=0.99*PTS,scale=iw*1.02:ih*1.02,crop=iw/1.02:ih/1.02,eq=contrast=1.03:brightness=0.01',
        '-af', 'asetrate=44100*1.01,aresample=44100,atempo=0.98',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23',
        '-c:a', 'aac', output_path
    ]

    try:
        # Executing the core modifier algorithm
        subprocess.run(ffmpeg_cmd, check=True)
        return send_file(output_path, as_attachment=True)
    except subprocess.CalledProcessError as e:
        return f"Processing Error: {str(e)}", 500
    finally:
        # Cleaning up space
        if os.path.exists(input_path):
            os.remove(input_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
