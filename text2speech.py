import streamlit as st
from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')


def split_into_chunks(text, chunk_size=5):
  import re
  sentences = re.split(r'(?<=[.!?]) +', text)
  chunks = [' '.join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]
  return chunks


def text_to_speech(text, client, voice="alloy"):
  response = client.audio.speech.create(
    model="tts-1",
    voice=voice,
    input=text
  )
  return response


def compile_audio(parts, output_path):
  combined = AudioSegment.empty()
  for part in parts:
    combined += AudioSegment.from_file(part)
  combined.export(output_path, format="mp3")


# def main():
#   input_text = input_txt
#   chunks = split_into_chunks(input_text, chunk_size=3)
#
#   audio_files = []
#   client = OpenAI(api_key=api_key)
#
#   for i, chunk in enumerate(chunks):
#     # Generate the audio for each chunk
#     speech_file_path = Path(f"speech_part_{i}.mp3")
#     response = text_to_speech(chunk, client)
#     response.stream_to_file(speech_file_path)
#     audio_files.append(speech_file_path)
#
#   # Combine all parts into one file
#   compile_audio(audio_files, Path("reviewer2s.mp3"))
#
#   # Clean up individual parts
#   for file_path in audio_files:
#     file_path.unlink()



# Streamlit application
def streamlit_app():
    st.title("Text to Speech Converter")
    st.write("Enter your text below, and the application will generate an MP3 file.")

    # Text input from the user
    input_text = st.text_area("Enter the text to convert to speech:", height=200)

    if st.button("Convert to Speech"):
        if input_text:
            st.write("Processing...")

            # Split the text into chunks
            chunks = split_into_chunks(input_text, chunk_size=3)

            audio_files = []
            client = OpenAI(api_key=api_key)

            # Generate the audio for each chunk
            for i, chunk in enumerate(chunks):
                speech_file_path = Path(f"speech_part_{i}.mp3")
                response = text_to_speech(chunk, client)
                response.stream_to_file(speech_file_path)
                audio_files.append(speech_file_path)

            # Combine all parts into one file
            output_path = Path("output_speech.mp3")
            compile_audio(audio_files, output_path)

            # Clean up individual parts
            for file_path in audio_files:
                file_path.unlink()

            # Provide a download link for the generated MP3 file
            with open(output_path, "rb") as audio_file:
                st.download_button(
                    label="Download MP3",
                    data=audio_file,
                    file_name="output_speech.mp3",
                    mime="audio/mp3"
                )

# Run the Streamlit app
if __name__ == "__main__":
    streamlit_app()
