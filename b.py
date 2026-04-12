from flask import Flask, request, jsonify, send_from_directory
import random
import pyjokes
from langchain_core.language_models.llms import BaseLLM
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
app = Flask(__name__, static_folder='.', static_url_path='')

def harryAi():
    print("HarryAi: hi! I am your friend Harry.")
    while True:
        query = input("You: ").lower()
        if query == "bye":
            print("harryAi: goodbye! have a nice day.")
            break
        elif "hi" in query or "yo" in query or "hey" in query or "hello" in query:
            print("HarryAi: Hello! How can I help you?")
        elif "help" in query:
            print("ronaldo agya bol kya dikkat")
        elif "your name" in query:
            print("cristiano ronaldo, suuuuiiiii")
        elif "flight booking" in query or "book a flight" in query or "book" in query:
            print("Dora: Sure! can you please please tell me whether you want a domestic or international flight?")
            query2 = input().lower()
            if "domestic" in query2 or "dome" in query2:
                print("Sorry, flight search is not available in terminal mode.")
            elif "inter" in query2 or "international" in query2:
                condition = input("Do you have passport? Please Answer yes or no: ").lower()
                if condition == "yes":
                    print("Sorry I cant help you with international flight booking")
                else:
                    print("First you have to apply for passport then You can fly abroad")
        else:
            print("Ronaldo is the greatest of all time")

session_state = {}

jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my suitcase there will be no vacation this year. Now I'm dealing with emotional baggage.",
    "Why did the airport break up with the airplane? Because it had too many terminal issues!",
    "I asked the flight attendant for a window seat. She said 'Sir, this is a bus.'",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "Why can't you give Elsa a balloon? Because she'll let it go!",
    "I told my doctor I broke my arm in two places. He told me to stop going to those places.",
    "Faizan yaar kitne bunk marega, ghar pe Sota rehta hoga",
    "What do you call a fake noodle? An impasta!",
    "Why did the bicycle fall over? Because it was two-tired!",
    "I used to hate facial hair but then it grew on me.",
    "Why don't eggs tell jokes? They'd crack each other up!",
    "What do you call cheese that isn't yours? Nacho cheese!",
    "I would tell you a joke about construction, but I'm still working on it."
]

def harryAi_web(message):
    query = message.lower().strip()
    state = session_state.get("step", None)

    if state == "await_flight_type":
        if "domestic" in query or "dome" in query:
            session_state.pop("step", None)
            return "Sorry, flight search is not available right now. Please contact us directly for bookings!"
        elif "inter" in query or "international" in query:
            session_state["step"] = "await_passport"
            return "Do you have a passport? Please answer yes or no:"
        else:
            session_state.pop("step", None)
            return "Sorry, I didn't understand. Please say 'domestic' or 'international'."

    elif state == "await_passport":
        session_state.pop("step", None)
        if "yes" in query:
            return "Sorry, I can't help with international flights right now."
        else:
            return "First apply for a passport, then you can fly abroad!"
    if query == "bye":
        return "Goodbye! Have a nice day."
    elif "hi" in query or "yo" in query or "hey" in query or "hello" in query:
        return "Hello! How can I help you?"
    elif "help" in query:
        return "ronaldo agya bol kya dikkat"
    elif "tiwari joke" in query or "crazy" in query:
        return pyjokes.get_joke()
    elif "your name" in query:
        return "cristiano ronaldo, suuuuiiiii"
    elif "flight booking" in query or "book a flight" in query or "book" in query:
        session_state["step"] = "await_flight_type"
        return "Sure! Do you want a domestic or international flight?"
    elif "joke" in query or "funny" in query or "make me laugh" in query or "jokes" in query:
        return random.choice(jokes)
    elif "roast me" in query or "roast" in query:
        return "You're so slow, even Spirit Airlines would leave without you!"
    elif "tell me something" in query or "say something" in query:
        return random.choice(jokes)
    elif "bored" in query or "boring" in query:
        return "Here's a joke to cheer you up: " + random.choice(jokes)
    elif "haha" in query or "lol" in query or "hehe" in query:
        return "Glad I made you laugh! Want another joke? Just say 'joke'!"
    elif "sad" in query or "upset" in query or "depressed" in query:
        return "Aw, cheer up! Here's something funny: " + random.choice(jokes)
    else:
        return "Ronaldo is the greatest of all time"


@app.route("/")
def home():
    return send_from_directory('.', 'a.html')

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"response": "I didn't receive a message."})
    response = harryAi_web(user_message)
    return jsonify({"response": response})

llm = ChatGroq(
    groq_api_key="This is api key",
    model_name="llama-3.3-70b-versatile"
)

prompt = PromptTemplate(
    input_variables=["text"],
    template="Suggest the next word after: {text}"
)

def suggest_next_word(text):
    chain = prompt | llm
    response = chain.invoke({"text": text})
    return response.content


@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.json
    text = data.get("message")
    response = suggest_next_word(text)
    return jsonify({"response": response})

if __name__ == "__main__":
    print("Chatbot is running! Visit http://127.0.0.1:5000 in your browser")
    app.run(debug=True)