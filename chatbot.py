from tkinter import *
from tkinter import scrolledtext
import threading
import datetime
import random

# =====================================
# WINDOW
# =====================================

window = Tk()
window.title("🤖 Smart Meta AI")
window.geometry("750x700")
window.config(bg="#0b141a")

# =====================================
# CHAT MEMORY
# =====================================

chat_memory = []

# =====================================
# RANDOM RESPONSES
# =====================================

greetings = [
    "Hello Vanshika 👋",
    "Hey there 😊",
    "Hi! How can I help you today?"
]

jokes = [
    "Why do programmers love Python? 🐍 Because it’s easy to learn!",
    "Debugging is like detective work 🕵️",
    "AI is cool until it starts correcting humans 😄"
]

motivation = [
    "You can become an amazing AI Engineer 🚀",
    "Consistency beats talent 💪",
    "Keep learning daily and success will follow 📚"
]

# =====================================
# HEADER
# =====================================

header = Frame(window, bg="#202c33", height=60)
header.pack(fill=X)

title = Label(
    header,
    text="🤖 Smart Meta AI",
    bg="#202c33",
    fg="white",
    font=("Arial", 18, "bold")
)

title.pack(pady=10)

# =====================================
# CHAT AREA
# =====================================

chat_area = scrolledtext.ScrolledText(
    window,
    wrap=WORD,
    font=("Arial", 12),
    bg="#111b21",
    fg="white"
)

chat_area.pack(
    padx=10,
    pady=10,
    fill=BOTH,
    expand=True
)

chat_area.insert(
    END,
    "🤖 Offline Smart Meta AI Ready\n\nType your message below 👇\n\n"
)

# =====================================
# AI RESPONSE FUNCTION
# =====================================

def get_ai_response(message):

    msg = message.lower()

    if "hello" in msg or "hi" in msg:
        return random.choice(greetings)

    elif "how are you" in msg:
        return "I am doing great 😊"

    elif "your name" in msg:
        return "I am Smart Meta AI 🤖"

    elif "who created you" in msg:
        return "I was created by Vanshika Kaushik 👩‍💻"

    elif "what is ai" in msg:
        return "AI stands for Artificial Intelligence 🧠"

    elif "python" in msg:
        return "Python is one of the best languages for AI and automation 🐍"

    elif "joke" in msg:
        return random.choice(jokes)

    elif "motivate" in msg:
        return random.choice(motivation)

    elif "time" in msg:
        current = datetime.datetime.now().strftime("%I:%M %p")
        return f"Current time is {current} ⏰"

    elif "date" in msg:
        today = datetime.date.today()
        return f"Today's date is {today} 📅"

    elif "+" in msg or "-" in msg or "*" in msg or "/" in msg:

        try:
            answer = eval(msg)
            return f"The answer is {answer} 🧮"

        except:
            return "Invalid math expression ❌"

    elif "bye" in msg:
        return "Goodbye Vanshika 👋"

    else:
        smart_replies = [
            "Interesting 🤔",
            "Tell me more 😊",
            "That sounds cool 🚀",
            "I am still learning 🧠",
            "Can you explain differently?"
        ]

        return random.choice(smart_replies)

# =====================================
# PROCESS MESSAGE
# =====================================

def process_message(user_input):

    current_time = datetime.datetime.now().strftime("%I:%M %p")

    # Typing effect
    chat_area.insert(END, "\nAI is typing...\n")
    chat_area.see(END)

    # AI reply
    ai_reply = get_ai_response(user_input)

    # Remove typing text
    chat_area.delete("end-2l", "end-1l")

    # Show AI reply
    chat_area.insert(
        END,
        f"\nAI ({current_time}):\n{ai_reply}\n"
    )

    chat_area.see(END)

# =====================================
# SEND MESSAGE
# =====================================

def send_message():

    user_input = entry_box.get()

    if user_input.strip() == "":
        return

    current_time = datetime.datetime.now().strftime("%I:%M %p")

    # Show user message
    chat_area.insert(
        END,
        f"\nYou ({current_time}):\n{user_input}\n"
    )

    chat_area.see(END)

    # Clear input
    entry_box.delete(0, END)

    # Background thread
    threading.Thread(
        target=process_message,
        args=(user_input,),
        daemon=True
    ).start()

# =====================================
# ENTER KEY
# =====================================

def enter_key(event):
    send_message()

# =====================================
# CLEAR CHAT
# =====================================

def clear_chat():
    chat_area.delete("1.0", END)

# =====================================
# BOTTOM FRAME
# =====================================

bottom_frame = Frame(window, bg="#202c33")
bottom_frame.pack(fill=X)

# =====================================
# INPUT BOX
# =====================================

entry_box = Entry(
    bottom_frame,
    font=("Arial", 14),
    bg="white",
    fg="black",
    width=40
)

entry_box.pack(
    side=LEFT,
    padx=10,
    pady=10,
    ipady=8
)

entry_box.bind("<Return>", enter_key)

# =====================================
# SEND BUTTON
# =====================================

send_button = Button(
    bottom_frame,
    text="Send",
    command=send_message,
    bg="#00a884",
    fg="white",
    font=("Arial", 12, "bold"),
    width=10
)

send_button.pack(side=LEFT, padx=5)

# =====================================
# CLEAR BUTTON
# =====================================

clear_button = Button(
    bottom_frame,
    text="Clear",
    command=clear_chat,
    bg="red",
    fg="white",
    font=("Arial", 12, "bold"),
    width=10
)

clear_button.pack(side=LEFT, padx=5)

# =====================================
# RUN APP
# =====================================

window.mainloop()