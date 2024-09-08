import pyttsx3
import pywhatkit
import wikipedia
import datetime
import pyjokes
import time

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

def speak(text):
    """This function will speak the given text."""
    engine.say(text)
    engine.runAndWait()

def get_current_time():
    """Returns the current time in a readable format."""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

def tell_joke():
    """Returns a random joke."""
    return pyjokes.get_joke()

def set_reminder(reminder_time, reminder_message):
    """Sets a reminder and notifies the user when the time is reached."""
    reminder_time = datetime.datetime.strptime(reminder_time, "%I:%M %p")
    current_time = datetime.datetime.now()

    time_difference = (reminder_time - current_time).total_seconds()
    if time_difference > 0:
        print(f"Reminder set for {reminder_time.strftime('%I:%M %p')}.")
        speak(f"Reminder set for {reminder_time.strftime('%I:%M %p')}.")

        time.sleep(time_difference)
        speak(f"Reminder: {reminder_message}")
        print(f"Reminder: {reminder_message}")
    else:
        print("The time you set has already passed. Please set a future time.")
        speak("The time you set has already passed. Please set a future time.")

def chatbot_response(user_input):
    # Convert user input to lowercase to make the chatbot case-insensitive
    user_input = user_input.lower()

    # Define responses based on simple rules
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you today?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"
    elif "your name" in user_input:
        return "I'm a simple chatbot created by you."
    elif "play" in user_input and "youtube" in user_input:
        # Extract the search query
        search_query = user_input.replace("play", "").replace("on youtube", "").strip()
        pywhatkit.playonyt(search_query)
        return f"Opening YouTube and playing {search_query}."
    elif "search wikipedia for" in user_input:
        # Extract the search query
        search_query = user_input.replace("search wikipedia for", "").strip()
        summary = wikipedia.summary(search_query, sentences=2)
        return f"According to Wikipedia: {summary}"
    elif "time" in user_input:
        current_time = get_current_time()
        return f"The current time is {current_time}."
    elif "tell me a joke" in user_input or "make me laugh" in user_input:
        joke = tell_joke()
        return joke
    elif "set a reminder for" in user_input:
        # Extract the time and message from the user input
        reminder_time = user_input.split("for")[1].strip().split(" ", 1)[0].strip()
        reminder_message = user_input.split("for")[1].strip().split(" ", 1)[1].strip()
        set_reminder(reminder_time, reminder_message)
        return f"Setting a reminder for {reminder_time} to {reminder_message}."
    elif "bye" in user_input:
        return "Goodbye! Have a great day!"
    else:
        return "I'm sorry, I don't understand that. Can you please ask something else?"

# Chatbot loop to keep the conversation going
def chat():
    print("Hello! Type 'bye' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            response = "Goodbye! Have a great day!" 
            print(f"Chatbot: {response}")
            speak(response)
            break
        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")
        speak(response)

# Start the chat
chat()
