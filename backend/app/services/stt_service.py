# backend/app/services/stt_service.py
import asyncio
import random

class STTService:
    """
    A mock Speech-to-Text (STT) service that simulates the behavior of a
    Whisper-based transcription model. It's designed to be asynchronous.
    """
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """
        Simulates the transcription of an audio byte stream.
        In this mock, the audio_data is not actually processed.
        """
        print("Mock STT Service: Simulating transcription...")
        # Simulate I/O bound or CPU bound delay of a real transcription model
        await asyncio.sleep(random.uniform(1.0, 2.5))
        
        mock_transcriptions = [
            "পঞ্চাশ কেজি আলু বিক্রি করতে চাই প্রতি কেজি পঁচিশ টাকা",
            "আমার কাছে ১০০ কেজি ধান আছে, প্রতি কেজি ৩০ টাকা করে বিক্রি করব",
            "আমি ২০ কেজি পেঁয়াজ বিক্রি করব, কেজি ৪০ টাকা",
            "আলুর দামের পূর্বাভাস দেখাও", # For future NLP intent
        ]
        selected_transcription = random.choice(mock_transcriptions)
        print(f"Mock STT Service: Transcription complete. Result: '{selected_transcription}'")
        return selected_transcription

stt_service = STTService()
