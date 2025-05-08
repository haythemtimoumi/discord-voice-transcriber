import pyaudio
from vosk import Model, KaldiRecognizer
import json
import logging
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

class VoiceRecorder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.audio = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 2048
        self.model = self._load_model()
        self._verify_audio_device()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.logger.info("✅ VoiceRecorder initialized")

    def _load_model(self):
        model_path = Path("models/vosk-model-en-us-0.22-lgraph")
        if not model_path.exists():
            raise FileNotFoundError(f"❌ Model directory not found at {model_path}")
        return Model(str(model_path))

    def _verify_audio_device(self):
        try:
            info = self.audio.get_default_input_device_info()
            self.logger.info(f"🎤 Using audio device: {info['name']}")
        except Exception as e:
            self.logger.error(f"❌ Audio device error: {str(e)}")
            raise

    async def record_and_transcribe(self, duration=5):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self._blocking_record_and_transcribe, duration)

    def _blocking_record_and_transcribe(self, duration):
        try:
            frames = self._record_audio(duration)
            if not frames:
                return "⚠️ No audio captured"
            return self._transcribe_audio(frames)
        except Exception as e:
            self.logger.error(f"❌ Processing error: {str(e)}")
            return f"Error: {str(e)}"

    def _record_audio(self, duration):
        try:
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
        except Exception as e:
            self.logger.error(f"❌ Failed to open audio stream: {str(e)}")
            raise

        frames = []
        for _ in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        return b''.join(frames)

    def _transcribe_audio(self, frames):
        recognizer = KaldiRecognizer(self.model, self.rate)
        recognizer.AcceptWaveform(frames)
        result = json.loads(recognizer.FinalResult())
        return result.get("text", "").strip() or "⚠️ No speech detected"

    def cleanup(self):
        self.audio.terminate()
        self.logger.info("✅ Audio resources released")
