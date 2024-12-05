# Video Summarizer

The **Video Summarizer** is a Flask-based web application that extracts the transcript of a video and generates a concise summary. It supports both locally uploaded videos and video URLs and leverages the pre-trained **BART-Large-CNN** model for text summarization. The application uses inference without fine-tuning the summarization model.

---

## Features
- **Upload Video Files**: Users can upload local video files for transcription and summarization.
- **Video URL Support**: Download and process videos from online platforms using their links.
- **Transcript Generation**: Converts video audio into text using OpenAI's Whisper model.
- **Text Summarization**: Summarizes the generated transcript using the BART-Large-CNN model.
- **Multiple Tasks**: Supports both transcription and translation tasks.

---

## Tech Stack
- **Backend**:
  - Flask
  - OpenAI Whisper (for transcription)
  - Hugging Face Transformers (BART-Large-CNN model for summarization)
  - FFmpeg (for audio extraction)
- **Frontend**:
  - HTML and CSS (for a simple web interface)
- **Deployment**:
  - Python (3.8+)

---

## Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg installed on your system
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/<your_username>/video-summarizer.git
   cd video-summarizer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure FFmpeg is installed and added to your system's PATH.

5. Run the Flask app:
   ```bash
   python app.py
   ```

6. Open the app in your browser:
   Navigate to `http://127.0.0.1:5000` in your web browser.

---

## Usage
1. **Upload a Video File**:
   - Select a video file to upload from your local system.
   - Choose either "Transcribe" (default) or "Translate" from the task options.
   - Click the "Submit" button to generate a transcript and summary.

2. **Provide a Video URL**:
   - Enter the URL of a video in the provided input field.
   - Choose the task option ("Transcribe" or "Translate").
   - Click "Submit" to process the video.

3. **View Results**:
   - The transcript and its summary will be displayed on the web page after processing.

---

## Folder Structure
```
video-summarizer/
│
├── Video_Summarizer/
│   ├── components/
│   │   ├── vid_to_txt.py      # Handles video-to-text conversion
│   │   ├── vid_summarizer.py  # Summarization logic using BART
│   │   ├── video_downloader.py # Handles video downloading via URL
│   ├── logger.py              # Logging utilities
│   ├── exception.py           # Custom exception handling
│
├── templates/
│   ├── index.html             # Frontend template
│
├── uploads/                   # Directory to store uploaded videos
├── app.py                     # Main Flask application
├── requirements.txt           # List of dependencies
├── README.md                  # Project documentation
```

---

## Models Used
1. **Whisper**:
   - For speech-to-text transcription.
   - Supports multilingual transcription and translation tasks.

2. **BART-Large-CNN**:
   - Pre-trained summarization model from Hugging Face.
   - Generates concise and coherent summaries from transcripts.

---

## Future Enhancements
- Add support for fine-tuning the BART model for specific video domains.
- Enhance the UI with more advanced features like progress tracking.
- Add support for longer videos with dynamic chunking and processing.

---

## Contributing
Contributions are welcome! If you'd like to contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes and push to your branch.
4. Open a Pull Request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- [Hugging Face Transformers](https://huggingface.co/)
- [OpenAI Whisper](https://openai.com/)
- Flask Framework

Feel free to explore, contribute, or provide feedback! 🎉
