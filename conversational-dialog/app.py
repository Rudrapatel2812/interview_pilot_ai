import streamlit as st
import os
import tempfile
import json
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
from audioToText import AudioRecorder, transcribe_audio

# Load environment variables
load_dotenv()

# Initialize API clients
client_openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
client_claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Initialize global components
recorder = AudioRecorder()

def text_to_speech(text: str, audio_path="interviewer-speech.mp3"):
    try:
        speech = client_openai.audio.speech.create(
            model='tts-1', voice='alloy', input=text)
        with open(audio_path, "wb") as f:
            f.write(speech.content)
        return audio_path
    except Exception as e:
        st.error(f"Error generating speech: {e}")
        return None

def text_to_text(input_text: str, history, persona):
    try:
        history.append({'role': 'user', 'content': input_text})
        response = client_claude.messages.create(
            model='claude-3-5-sonnet-20240620',
            max_tokens=1000,
            temperature=0,
            system=persona,
            messages=history
        )
        response_text = response.content[0].text
        history.append({'role': 'assistant', 'content': response_text})
        return response_text, history
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "I'm sorry, I didn't catch that.", history

def is_done(message):
    try:
        response = client_claude.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Given this response, {message}, does it seem like the person wants to end the conversation immediately? only give a 'yes' or a 'no' in that exact format"
                        }
                    ]
                }
            ]
        )
        return response.content[0].text.lower().strip() == "yes"
    except Exception as e:
        st.error(f"Error determining end of conversation: {e}")
        return False

def run_interview(persona):
    st.session_state['history'] = []
    stop = False

    while not stop:
        st.write("🎙️ Click the button to record your answer.")
        if st.button("Record Now"):
            frames = recorder.record_until_silence()
            wav_filename = recorder.save_recording(frames)

            try:
                user_input = transcribe_audio(wav_filename)
                st.success(f"🗣 You said: {user_input}")
            except Exception as e:
                st.error(f"Error transcribing: {e}")
                user_input = ""
            finally:
                os.remove(wav_filename)

            if user_input.strip().lower() == "i am done." or is_done(user_input):
                stop = True
                break

            response_text, st.session_state['history'] = text_to_text(user_input, st.session_state['history'], persona)
            st.markdown(f"🤖 *Interviewer*: {response_text}")

            if is_done(response_text):
                stop = True
                break

            audio_path = text_to_speech(response_text)
            if audio_path:
                st.audio(audio_path)

    st.write("📝 Interview ended. Here's the transcript:")
    st.json(st.session_state['history'])

    with open('interview_history.json', 'w') as f:
        json.dump(st.session_state['history'], f, indent=4)

# --- Streamlit UI ---
# --- Streamlit UI ---
import time

st.set_page_config(page_title="Conversational Interviewer", layout="centered")
st.title("🧠 AI Interviewer")
st.markdown("This app simulates an AI-driven interview experience.")

if 'step' not in st.session_state:
    st.session_state['step'] = 'start'  # can be 'start', 'record', 'respond', 'end'
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'persona' not in st.session_state:
    st.session_state['persona'] = ''
if 'stop' not in st.session_state:
    st.session_state['stop'] = False

difficulty = st.selectbox("Select interview difficulty level:", ["easy", "medium", "hard"])

if st.session_state['step'] == 'start':
    if st.button("Start Interview"):
        persona_file = os.path.join(os.path.dirname(__file__), "ethan-the-strategic-planner-product-manager-watershed-response-guidelines.txt")
        with open(persona_file, 'r') as f:
            persona = f.read()
        persona += f" Begin the interview. You are the interviewer and I am the interviewee. Please be very concise as the interviewer in your answers but do not skip the formalities. Use this opportunity to pick up on interviewee social cues. keep in mind time is limited and make this interview {difficulty}."
        st.session_state['persona'] = persona
        st.session_state['step'] = 'record'
        st.rerun()

elif st.session_state['step'] == 'record':
    st.write("🎙️ Please record your answer.")
    if st.button("Record Now", key="record_now"):
        frames = recorder.record_until_silence()
        wav_filename = recorder.save_recording(frames)
        try:
            user_input = transcribe_audio(wav_filename)
            st.success(f"🗣 You said: {user_input}")
        except Exception as e:
            st.error(f"Error transcribing: {e}")
            user_input = ""
        finally:
            os.remove(wav_filename)
        st.session_state['user_input'] = user_input
        st.session_state['step'] = 'respond'
        st.rerun()

elif st.session_state['step'] == 'respond':
    user_input = st.session_state.get('user_input', '')
    if user_input.strip().lower() == "i am done." or is_done(user_input):
        st.session_state['stop'] = True
        st.session_state['step'] = 'end'
        st.rerun()
    else:
        response_text, st.session_state['history'] = text_to_text(
            user_input, st.session_state['history'], st.session_state['persona'])
        st.session_state['last_response'] = response_text
        audio_path = text_to_speech(response_text)
        st.session_state['last_audio'] = audio_path
        st.session_state['step'] = 'playback'
        st.rerun()

elif st.session_state['step'] == 'playback':
    response_text = st.session_state.get('last_response', '')
    audio_path = st.session_state.get('last_audio', None)
    st.markdown(f"🤖 *Interviewer*: {response_text}")
    if audio_path:
        st.audio(audio_path, format='audio/mp3')
    if is_done(response_text):
        st.session_state['stop'] = True
        st.session_state['step'] = 'end'
    else:
        if st.button("Next", key="next_after_playback"):
            st.session_state['step'] = 'record'
            st.rerun()

elif st.session_state['step'] == 'end':
    st.write("📝 Interview ended. Here's the transcript:")
    st.json(st.session_state['history'])
    with open('interview_history.json', 'w') as f:
        json.dump(st.session_state['history'], f, indent=4)