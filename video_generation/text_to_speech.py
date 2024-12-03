from dotenv import load_dotenv
from mutagen.mp3 import MP3
from pydub import AudioSegment
import io

from video_generation.completions.completions import text_to_speech

load_dotenv()


def split_text(text, max_length=4096):
    """Splits text into smaller chunks."""
    chunks = []
    while len(text) > max_length:
        split_point = text[:max_length].rfind(' ')
        if split_point == -1:  # No space found, force split
            split_point = max_length
        chunks.append(text[:split_point])
        text = text[split_point:].lstrip()
    chunks.append(text)
    return chunks


def convert_text_to_speech(path: str, name: str, text: str):
    """
    Converts text to speech using io.BytesIO for in-memory processing.

    Parameters:
    - path: str: The directory to save the final file.
    - name: str: The name of the output MP3 file.
    - text: str: The input text to be converted to speech.
    - text_to_speech: Callable: A function or API to generate TTS for a chunk of text.
    """

    def process_chunk(chunk):
        response = text_to_speech(chunk)  # Your TTS function
        if hasattr(response, "read"):  # Check if response is a stream
            return io.BytesIO(response.read())
        elif isinstance(response, bytes):  # If response is already bytes
            return io.BytesIO(response)
        else:
            raise ValueError("Unsupported response type from text_to_speech.")

    text_chunks = split_text(text)
    combined_audio = AudioSegment.empty()  # Initialize empty audio segment
    target_bitrate = None

    for chunk in text_chunks:
        audio_stream = process_chunk(chunk)

        # Load the audio into an AudioSegment
        audio = AudioSegment.from_file(audio_stream, format="mp3")

        # Determine bitrate from the first chunk
        if target_bitrate is None:
            audio_stream.seek(0)
            mp3_info = MP3(audio_stream)
            target_bitrate = f"{mp3_info.info.bitrate // 1000}k"
            print(f"Target bitrate: {target_bitrate}")

        # Append the audio chunk to the final audio
        combined_audio += audio

    # Add padding and fade effects to the final audio
    silence = AudioSegment.silent(duration=500)
    combined_audio = silence + combined_audio + silence
    combined_audio = combined_audio.fade_in(500).fade_out(500)

    # Export the combined audio to a file
    final_file_path = f"{path}/{name}.mp3"
    final_audio_buffer = io.BytesIO()

    combined_audio.export(
        final_audio_buffer,
        format="mp3",
        bitrate=target_bitrate,
        parameters=["-write_xing", "0"]
    )

    # Save to the final file
    with open(final_file_path, "wb") as f:
        final_audio_buffer.seek(0)
        f.write(final_audio_buffer.read())

    # Return the length of the final MP3 file
    final_audio_buffer.seek(0)
    mp3_file = MP3(final_file_path)
    return mp3_file.info.length
