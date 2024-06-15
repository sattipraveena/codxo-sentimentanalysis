import speech_recognition as sr
import pyttsx3
import requests

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to listen and recognize speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        speak("Could not request results; check your network connection.")
        return None
    return command.lower()

# Function to perform tasks based on commands
def perform_task(command):
    if "hello" in command:
        speak("Hello! How can I help you today?")
    elif "your name" in command:
        speak("I am your custom voice assistant.")
    elif "weather" in command:
        get_weather()
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I can't help with that yet.")

# Function to get weather information
def get_weather():
    api_key = "your_openweathermap_api_key"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("Which city?")
    city_name = listen()
    if city_name:
        complete_url = base_url + "q=" + city_name + "&appid=" + api_key
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] != "404":
            main = data["main"]
            temperature = main["temp"]
            weather_desc = data["weather"][0]["description"]
            weather_response = f"The temperature in {city_name} is {temperature - 273.15:.2f}°C with {weather_desc}."
            speak(weather_response)
        else:
            speak("City not found. Please try again.")

# Main function to run the assistant
def run_assistant():
    speak("How can I assist you?")
    while True:
        command = listen()
        if command:
            perform_task(command)

if __name__ == "__main__":
    run_assistant()
