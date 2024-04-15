import streamlit as st
from streamlit_mic_recorder import speech_to_text
from deep_translator import GoogleTranslator

from gtts import gTTS
import base64
import pandas as pd
import os

openai_api_key = st.secrets["OPENAI_API_KEY"]
type = st.secrets["TYPE"]
id = st.secrets["ID"]

df = pd.read_excel(os.path.join('data', r'C:\Users\user\Downloads\language.xlsx'), sheet_name='wiki')
df.dropna(inplace=True)
lang = df['name'].to_list()
langlist = tuple(lang)
langcode = df['iso'].to_list()

lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}

with st.sidebar:
    st.title('Language Translator Web App')
    choice1 = st.sidebar.selectbox('__SELECT THE SPEAKERS LANGUAGE__', langlist)
    choice = st.sidebar.selectbox('__SELECT LANGUAGE TO BE TRANSLATED INTO__', langlist)
    st.info("The Translator Webapp takes input as the User's speech recording to converting it into text that can be edited for any incorrectly generated words from the audio. The Text is then translated into the user selected language along with the Audio file.")

speech_langs = {
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "la": "Latin",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Filipino",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-CN": "Chinese"
}

st.subheader("Record your audio")
st.info("Click on the **Start Recording** button and speak a phrase in the **selected language** in a clear manner. Click __Stop Recording__ and wait until __Speech-to-Text__ is generated before pressing __TRANSLATE__ button.")


state = st.session_state

if 'text_received' not in state:
    state.text_received = []

text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')

if text:
    state.text_received.append(text)

c3, c4 = st.columns(2)

with c3:
    for text in state.text_received:
        st.subheader("Speech to text")
        st.text_area("    ", value=text)
        st.write(f'{len(text)} characters.')

button = st.button("TRANSLATE")
with c4:
    if button:
        st.subheader("Translated text")
        translator = GoogleTranslator(source='auto', target=lang_array[choice])
        translate = translator.translate(text)
        st.text_area("                    ", value=translate)
        if choice in speech_langs.values():
            aud_file = gTTS(text=translate, lang=lang_array[choice], slow=False)
            aud_file.save("lang.mp3")
            audio_file_read = open('lang.mp3', 'rb')
            audio_bytes = audio_file_read.read()
            bin_str = base64.b64encode(audio_bytes).decode()
            st.write("Translated Audio")
            st.audio(audio_bytes, format='audio/mp3')
