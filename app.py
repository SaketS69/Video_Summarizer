import os
from flask import Flask, render_template, request

from Video_Summarizer.components.vid_to_txt import Config, VideoToText
from Video_Summarizer.components.vid_summarizer import summarize_text
from Video_Summarizer.components.video_downloader import VideoDownloader

app = Flask(__name__)
app.config['upload_dir'] = os.path.join('uploads/')
os.makedirs(app.config['upload_dir'], exist_ok=True)

# Default configurations for the transcription process
MODEL_NAME = 'tiny'  # Change as needed: 'tiny', 'small', 'medium', 'large'
GENERATE_SRT = True  # Set to True if subtitle files should be generated
VERBOSE_FLAG = False  # Set to True for detailed logs from the Whisper model
DEFAULT_TASK = 'transcribe'  # Default task (either 'transcribe' or 'translate')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def upload_file():
    try:
        video_file = request.files.get('video_file')  # Get the uploaded file
        transcript_generator = VideoToText(config=Config())

        if video_file:
            # Handle file upload
            filename = video_file.filename
            video_path = os.path.join(app.config['upload_dir'], filename)
            video_file.save(video_path)
            task = request.form.get('options', DEFAULT_TASK)  # Get task (default: transcribe)

            transcript = transcript_generator.initiate_stt(
                video_paths=[video_path],
                model=MODEL_NAME,
                srt=GENERATE_SRT,
                verbose=VERBOSE_FLAG,
                task=task
            )

        else:
            # Handle video link download
            video_link = request.form.get('link-input')
            if not video_link:
                return render_template('index.html', error="No video file or link provided.")

            downloader = VideoDownloader(url=video_link, save_path=app.config['upload_dir'])
            video_path = downloader.download()
            task = request.form.get('options', DEFAULT_TASK)  # Get task (default: transcribe)

            transcript = transcript_generator.initiate_stt(
                video_paths=[video_path],
                model=MODEL_NAME,
                srt=GENERATE_SRT,
                verbose=VERBOSE_FLAG,
                task=task
            )

        # Extract the transcript text
        if not transcript or 'text' not in transcript:
            return render_template('index.html', error="Transcription failed. No text found in transcript.")

        transcript_text = transcript['text']
        summary = summarize_text(transcript_text)

        # Return the results to the front-end
        return render_template('index.html', transcript=transcript_text, summary=summary)

    except Exception as e:
        # Handle any unexpected errors
        return render_template('index.html', error=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

