
import pyttsx3
import speech_recognition as sr
import requests
API_KEY = "139ff8e5644894750d3293adb1372433"
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results: {e}")
        return ""
def get_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"  # You can change units to "imperial" for Fahrenheit
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"The weather in {city_name} is {weather_description} with a temperature of {temperature} degrees Celsius."
    else:
        return "Sorry, I couldn't fetch the weather data."
def main():
    speak("Initializing voice assistant...")
    
    while True:
        query = listen()

        if query:
            if "weather" in query:
                city_name = query.split("weather in")[0].strip()
                weather_info = get_weather(city_name)
                speak(weather_info)
            elif "exit" in query:
                speak("Goodbye!")
                break
            else:
                speak("I'm sorry, I don't understand that command.")

if __name__ == "__main__":
    main()
