from flask import Flask, request, jsonify, send_from_directory
import random
import pyjokes
import wikipedia
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
            print("HarryAi: Sure! can you please please tell me whether you want a domestic or international flight?")
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
            print("It was pleasent talking, Have a nice day!!")

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
            session_state["step"] = "await_domestic_destination"
            return "Great! Where would you like to fly within the country? Please tell me your departure city and destination city."
        elif "inter" in query or "international" in query:
            session_state["step"] = "await_passport"
            return "Do you have a passport? Please answer yes or no:"
        else:
            session_state.pop("step", None)
            return "Sorry, I didn't understand. Please say 'domestic' or 'international'."

    elif state == "await_domestic_destination":
        session_state["step"] = "await_domestic_date"
        return f"Nice! I'll look for flights for that route. What date would you like to travel? (e.g. 25 July)"

    elif state == "await_domestic_date":
        session_state["step"] = "await_domestic_class"
        return "Got it! Which class would you prefer? Economy, Business, or First Class?"

    elif state == "await_domestic_class":
        session_state.pop("step", None)
        if "business" in query:
            return "Great choice! Business class flights usually cost between ₹8,000 - ₹25,000. Would you like me to help with anything else?"
        elif "first" in query:
            return "Luxury travel! First class flights usually cost between ₹20,000 - ₹60,000. Would you like me to help with anything else?"
        else:
            return "Economy it is! Flights usually cost between ₹2,500 - ₹8,000. Would you like me to help with anything else?"

    elif state == "await_passport":
        session_state.pop("step", None)
        if "yes" in query:
            session_state["step"] = "await_international_destination"
            return "Awesome! Which country would you like to fly to?"
        else:
            return "You'll need a passport for international travel. You can apply at your nearest Passport Seva Kendra. Want help with anything else?"

    elif state == "await_international_destination":
        session_state["step"] = "await_international_date"
        return f"Great destination! What date would you like to travel? (e.g. 25 July)"

    elif state == "await_international_date":
        session_state.pop("step", None)
        return "Perfect! International flights are typically available 3-6 months in advance. I recommend checking airlines like IndiGo, Air India, or Emirates for the best deals. Want help with anything else?"
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
    elif "cancel" in query and "flight" in query:
        return "To cancel a flight, visit the airline's website or call their customer care. Most airlines allow free cancellation within 24 hours of booking!"
    elif "baggage" in query or "luggage" in query:
        return "Most domestic flights allow 15kg check-in baggage and 7kg cabin baggage. International flights usually allow 23kg check-in. Always check with your airline for exact limits!"
    elif "check in" in query or "checkin" in query:
        return "Online check-in usually opens 48 hours before departure. You can check in via the airline's app or website. Airport check-in counters open 3 hours before international and 2 hours before domestic flights!"
    elif "visa" in query:
        return "Visa requirements depend on your destination country. You can check visa requirements at the official embassy website or use services like VFS Global. Need help with a specific country?"
    elif "flight status" in query or "flight delay" in query:
        return "You can check real-time flight status on the airline's website or app. For Indian flights, you can also check on the DGCA website!"
    elif "cheapest flight" in query or "cheap flight" in query or "best deal" in query:
        return "For the best flight deals, try booking 6-8 weeks in advance, travel on weekdays, and use apps like Google Flights, MakeMyTrip, or Skyscanner to compare prices!"
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
    return send_from_directory('.', 'index.html')

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"response": "I didn't receive a message."})
    response = harryAi_web(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)