import requests
import os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

def ask_qna(query, api_key):
    """Sends a query to the Gemini Pro API and returns the clear answer.

    Args:
        query: The question to ask.
        api_key: Your Google Cloud API key.

    Returns:
        The clear answer from the Gemini Pro API.
    """

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": query
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data, params={'key': api_key})
    response_json = response.json()

    try:
        answer = response_json['candidates'][0]['content']['parts'][0]['text']
        return answer
    except (KeyError, IndexError):
        return "Sorry, I couldn't understand your question. Please try again."

def speak(text):
    tts = gTTS(text=text, lang='en-IN')
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")

def start_listening():
    global listening
    listening = True
    print("Shiva is now listening...")

def stop_listening():
    global listening
    listening = False
    print("Shiva stopped listening...")

if __name__ == "__main__":
    api_key = "your api key here"  # Replace with your actual API key
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    listening = False

    while True:
        if not listening:
            with microphone as source:
                print("Waiting for 'hello Shiva' command...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            print("Recognizing...")
            try:
                command = recognizer.recognize_google(audio)
                print("You said:", command)
                if command.lower() == "hello shiva":
                    start_listening()
                elif command.lower() == "stop shiva":
                    stop_listening()
            except sr.UnknownValueError:
                print("Sorry, I could not understand what you said. Please try again.")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        else:
            with microphone as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            print("Recognizing...")
            try:
                query = recognizer.recognize_google(audio)
                print("You said:", query)
                if query.lower() == "exit":
                    break
                answer = ask_qna(query, api_key)
                print("Response:", answer)
                speak(answer)
            except sr.UnknownValueError:
                print("Sorry, I could not understand what you said. Please try again.")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
