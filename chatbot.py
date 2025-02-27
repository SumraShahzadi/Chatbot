import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext, ttk
import pyttsx3
import os

# Set up Google Gemini API Key
genai.configure(api_key="AIzaSyDavtPM9Ys9WJVn23L3xGnKUT0eTa5Ogko")

# Text-to-Speech (TTS) Engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('voice', engine.getProperty('voices')[0].id)


# Function to get chatbot response
def chatbot_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Updated model
        response = model.generate_content(prompt)
        return response.text.strip() if response else "⚠️ No response received."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# Function to display messages
def display_message(sender, message, is_user=True):
    chat_area.configure(state="normal")
    chat_area.insert(tk.END, f"{sender}: ", "user_tag" if is_user else "bot_tag")
    chat_area.insert(tk.END, message + "\n\n")
    chat_area.configure(state="disabled")
    chat_area.yview(tk.END)


# Function to speak the bot response
def speak_response():
    bot_response = chat_area.get("end-4l", "end-1c").strip()  # Get last bot response
    if bot_response:
        engine.say(bot_response)
        engine.runAndWait()


# Function to handle user input
def send_message():
    user_input = entry_field.get().strip()
    if user_input:
        display_message(username.get(), user_input, is_user=True)
        entry_field.delete(0, tk.END)

        bot_response = chatbot_response(user_input)
        display_message("Chatbot", bot_response, is_user=False)

        # Enable Listen button
        listen_button.config(state="normal")


# Dark mode toggle
def toggle_theme():
    if root.option_get("theme", "light") == "light":
        root.tk_setPalette(background="#2E2E2E", foreground="white")
        chat_area.config(bg="#333333", fg="white", insertbackground="white")
        entry_field.config(bg="#444444", fg="white", insertbackground="white")
        send_button.config(style="Dark.TButton")
        listen_button.config(style="Dark.TButton")
        theme_button.config(text="☀️ Light Mode")
        root.option_add("*theme", "dark")
    else:
        root.tk_setPalette(background="white", foreground="black")
        chat_area.config(bg="white", fg="black", insertbackground="black")
        entry_field.config(bg="white", fg="black", insertbackground="black")
        send_button.config(style="Light.TButton")
        listen_button.config(style="Light.TButton")
        theme_button.config(text="🌙 Dark Mode")
        root.option_add("*theme", "light")


# GUI Setup
root = tk.Tk()
root.title("AI Chatbot 🤖")
root.geometry("500x600")
root.tk_setPalette(background="white", foreground="black")

# Username Input
username = tk.StringVar(value="You")
tk.Label(root, text="Enter your name:", font=("Arial", 12, "bold"), fg="#007ACC").pack()
username_entry = tk.Entry(root, textvariable=username, font=("Arial", 12))
username_entry.pack(pady=5)

# Chat Display Area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=55, height=15, font=("Arial", 12))
chat_area.pack(pady=10)
chat_area.configure(state="disabled", bg="white", fg="black")
chat_area.tag_config("user_tag", foreground="#007ACC", font=("Arial", 12, "bold"))
chat_area.tag_config("bot_tag", foreground="#008000", font=("Arial", 12, "bold"))

# Input Field & Buttons
frame = tk.Frame(root)
frame.pack()
entry_field = tk.Entry(frame, width=40, font=("Arial", 12), bg="white", fg="black")
entry_field.pack(side=tk.LEFT, padx=10)
send_button = ttk.Button(frame, text="Send 🚀", command=send_message, style="Light.TButton")
send_button.pack(side=tk.RIGHT)

# Listen Button (Initially Disabled)
listen_button = ttk.Button(root, text="🔊 Listen", command=speak_response, style="Light.TButton", state="disabled")
listen_button.pack(pady=5)

# Dark Mode Button
theme_button = ttk.Button(root, text="🌙 Dark Mode", command=toggle_theme, style="Light.TButton")
theme_button.pack(pady=10)

# Styling
style = ttk.Style()
style.configure("Light.TButton", font=("Arial", 11, "bold"), foreground="black", background="#007ACC")
style.configure("Dark.TButton", font=("Arial", 11, "bold"), foreground="white", background="#444444")

# Start the GUI
root.mainloop()
