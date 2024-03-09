import pyttsx3

def text_to_speech(text, lang='en', voice='english'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # You can adjust the speaking rate (words per minute)
    engine.setProperty('voice', voice)
    engine.say(text)
    engine.runAndWait()

# Example usage
text = "Butter Chicken"
text_to_speech(text, voice='english-in')  # Specify the desired voice here
engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    print("Voice:")
    print(" - ID:", voice.id)
    print(" - Name:", voice.name)
    print(" - Languages:", voice.languages)
    print(" - Gender:", voice.gender)
    print(" - Age:", voice.age)
    print()
