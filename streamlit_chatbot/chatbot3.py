
import streamlit as st
import random
import time
import os
import pandas as pd
import google.generativeai as genai

# -------------------------------
# CONFIGURE GEMINI API
# -------------------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# -------------------------------
# CATEGORIES & WORDS
# -------------------------------
categories = {
    "Animals": ["elephant", "giraffe", "kangaroo", "penguin", "dolphin"],
    "Countries": ["malaysia", "brazil", "finland", "australia", "nigeria"],
    "Movies": ["inception", "avatar", "aladdin", "frozen", "titanic"],
    "Food": ["spaghetti", "croissant", "sushi", "taco", "biryani"]
}

# -------------------------------
# HANGMAN DRAWINGS
# -------------------------------
hangman_stages = [
    "😀",
    "😯\n |", 
    "😟\n/|", 
    "😫\n/|\\", 
    "😵\n/|\\\n /", 
    "💀\n/|\\\n/ \\"
]

# -------------------------------
# INITIALIZE SESSION STATE
# -------------------------------
if 'category' not in st.session_state:
    st.session_state.category = None
    st.session_state.secret_word = None
    st.session_state.guesses = []
    st.session_state.attempts = 0
    st.session_state.start_time = None
    st.session_state.name = ""
    st.session_state.game_over = False
    st.session_state.win = False

# -------------------------------
# FUNCTIONS
# -------------------------------
def get_hint(word, category):
    prompt = f"Give a helpful but not too obvious clue for the word '{word}' from the category '{category}'."
    response = model.generate_content(prompt)
    return response.text.strip()

def get_funny_comment(wrong_letter):
    prompt = f"Make a short funny comment when someone wrongly guesses the letter '{wrong_letter}' in a hangman game."
    response = model.generate_content(prompt)
    return response.text.strip()

def reset_game():
    st.session_state.category = None
    st.session_state.secret_word = None
    st.session_state.guesses = []
    st.session_state.attempts = 0
    st.session_state.start_time = None
    st.session_state.name = ""
    st.session_state.game_over = False
    st.session_state.win = False

def update_leaderboard(name, category, time_taken):
    try:
        df = pd.read_csv("leaderboard.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Category", "Time (s)"])
    df = pd.concat([df, pd.DataFrame([{"Name": name, "Category": category, "Time (s)": round(time_taken)}])])
    df.to_csv("leaderboard.csv", index=False)

# -------------------------------
# UI LAYOUT
# -------------------------------
st.title("🎯 Hangman AI Challenge")
st.caption("Built with Python, Streamlit & Gemini API")

if not st.session_state.category:
    st.header("1️⃣ Choose a Category")
    st.session_state.name = st.text_input("Enter your name to start:")
    category = st.selectbox("Pick a category", list(categories.keys()))
    if st.button("Start Game") and st.session_state.name:
        st.session_state.category = category
        st.session_state.secret_word = random.choice(categories[category])
        st.session_state.start_time = time.time()
        st.rerun()

# -------------------------------
# GAMEPLAY
# -------------------------------
else:
    word = st.session_state.secret_word
    masked_word = ''.join([letter if letter in st.session_state.guesses else '_' for letter in word])
    st.subheader(f"Category: {st.session_state.category}")
    st.text(f"Word: {' '.join(masked_word)}")

    st.write(f"Guesses: {', '.join(st.session_state.guesses)}")
    st.write(f"Attempts Left: {5 - st.session_state.attempts}")
    st.write("Drawing:")
    st.text(hangman_stages[st.session_state.attempts])

    if st.session_state.game_over:
        if st.session_state.win:
            st.success(f"🎉 You won in {round(time.time() - st.session_state.start_time)} seconds!")
            update_leaderboard(st.session_state.name, st.session_state.category, time.time() - st.session_state.start_time)
        else:
            st.error(f"Game Over! The word was **{word}**. Better luck next time!")

        if st.button("Play Again"):
            reset_game()
            st.rerun()
        st.markdown("---")
        st.subheader("🏆 Leaderboard")
        try:
            df = pd.read_csv("leaderboard.csv").sort_values(by="Time (s)").head(10)
            st.table(df)
        except FileNotFoundError:
            st.info("Leaderboard is empty.")
        st.stop()

    # --- Hint ---
    if st.button("💡 Get Hint"):
        with st.spinner("Gemini is thinking..."):
            hint = get_hint(word, st.session_state.category)
            st.info(f"Hint: {hint}")

    # --- Guess input ---
    guess = st.text_input("Guess a letter:", max_chars=1).lower()

    if guess and guess not in st.session_state.guesses:
        st.session_state.guesses.append(guess)
        if guess in word:
            st.success(f"✅ Nice! '{guess}' is correct! 🎉")
        else:
            st.session_state.attempts += 1
            with st.spinner("Gemini's roast incoming..."):
                comment = get_funny_comment(guess)
                st.error(f"❌ Nope! {comment}")

    # --- Win or Lose ---
    if all(letter in st.session_state.guesses for letter in word):
        st.session_state.game_over = True
        st.session_state.win = True
        st.rerun()

    elif st.session_state.attempts >= 5:
        st.session_state.game_over = True
        st.session_state.win = False
        st.rerun()
masked_word = ''.join([letter if letter in st.session_state.guesses else '_' for letter in word])
st.text(f"Word: {' '.join(masked_word)}")
