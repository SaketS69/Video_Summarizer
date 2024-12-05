import whisper
import ffmpeg
import tempfile
import os
import warnings
from dataclasses import dataclass
from Video_Summarizer.logger import logger
from Video_Summarizer.exception import CustomException
import subprocess
import sys

@dataclass
class Config:
    acodec: str = "pcm_s16le"
    audio_channel: int = 1
    audio_rate: str = '16k'
    output_dir_name: str = 'transcript_text'


class VideoToText:
    def __init__(self, config: Config):
        try:
            self.acodec = config.acodec
            self.ac = config.audio_channel
            self.ar = config.audio_rate
            self.output_dir = config.output_dir_name
        except Exception as e:
            raise CustomException(e, sys)

    def get_audio(self, paths) -> dict:
        """
        Extracts audio from video files and returns a dictionary of video paths to extracted audio paths.
        """
        try:
            temp_dir = tempfile.gettempdir()
            audio_paths = {}

            for path in paths:
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Video file not found: {path}")

                filename = os.path.basename(path).split('.')[0]
                logger.info(f"Extracting audio from {os.path.basename(path)}...")
                output_path = os.path.join(temp_dir, f"{filename}.wav")

                try:
                    # Use ffmpeg-python to extract audio
                    (
                        ffmpeg
                        .input(path)
                        .output(output_path, acodec=self.acodec, ac=self.ac, ar=self.ar)
                        .run(quiet=True, overwrite_output=True)
                    )
                except AttributeError as e:
                    logger.error(f"ffmpeg-python error: {e}. Falling back to system-level FFmpeg.")
                    # Fallback: Use system-level ffmpeg as a subprocess
                    command = [
                        "ffmpeg", "-i", path,
                        "-acodec", self.acodec, "-ac", str(self.ac), "-ar", self.ar,
                        output_path
                    ]
                    subprocess.run(command, check=True)

                audio_paths[path] = output_path

            return audio_paths

        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise CustomException(e, sys)
        except subprocess.CalledProcessError as e:
            logger.error(f"System FFmpeg command failed: {e}")
            raise CustomException(e, sys)
        except Exception as e:
            logger.error(f"Unexpected error in get_audio: {e}")
            raise CustomException(e, sys)

    def write_transcript(self, audio_path, text_path, transcribe: callable):
        """
        Generates a transcript for a given audio file and writes it to the specified text path.
        """
        try:
            logger.info(f"Generating transcript for {os.path.basename(audio_path)} audio... This might take a while.")
            
            warnings.filterwarnings("ignore")
            result = transcribe(audio_path)
            warnings.filterwarnings("default")
            
            logger.info(f"Writing transcript for the video.")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
            
            return result

        except Exception as e:
            logger.error(f"Error in write_transcript: {e}")
            raise CustomException(e, sys)

    def get_transcript(self, audio_paths: dict, output_text: bool, output_dir: str, transcribe: callable):
        """
        Processes extracted audio files and generates transcripts.
        """
        try:
            text_dir = output_dir if output_text else tempfile.gettempdir()
            results = {}

            for path, audio_path in audio_paths.items():
                filename = os.path.basename(path).split('.')[0]
                text_path = os.path.join(text_dir, f"{filename}.txt")
                result = self.write_transcript(audio_path, text_path, transcribe)
                results[path] = result

            return results

        except Exception as e:
            logger.error(f"Error in get_transcript: {e}")
            raise CustomException(e, sys)

    def initiate_stt(self, video_paths: list, model: str, srt: bool, verbose: bool, task: str):
        """
        Entry point to process video files, extract audio, and generate transcripts.
        """
        try:
            os.makedirs(self.output_dir, exist_ok=True)

            # Load Whisper model
            if model.endswith(".en"):
                logger.info(f"{model} is an English-only model.")
            model = whisper.load_model(model)

            # Extract audio from videos
            audio = self.get_audio(video_paths)

            # Generate transcripts
            subtitles = self.get_transcript(
                audio, srt, self.output_dir,
                lambda audio_path: model.transcribe(audio_path, verbose=verbose, task=task)
            )
            return subtitles

        except Exception as e:
            logger.error(f"Error in initiate_stt: {e}")
            raise CustomException(e, sys)
