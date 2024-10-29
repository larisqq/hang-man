import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import json
import os

# Extended list of words for different themes
words_by_theme = {
    "Animals": ["cat", "dog", "elephant", "giraffe", "tiger", "lion", "zebra", "kangaroo", "dolphin", "panda"],
    "Technology": ["python", "java", "hangman", "algorithm", "computer", "internet", "robot", "software", "gadget", "database"],
    "Sports": ["football", "basketball", "tennis", "swimming", "running", "hockey", "baseball", "cricket", "golf", "volleyball"],
    "Fruits": ["apple", "banana", "cherry", "grape", "orange", "peach", "kiwi", "melon", "pineapple", "mango"],
    "Countries": ["france", "italy", "germany", "canada", "brazil", "japan", "india", "spain", "mexico", "china"],
    "Movies": ["inception", "gladiator", "titanic", "avatar", "matrix", "jaws", "frozen", "moana", "joker", "parasite"],
    "Colors": ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown", "black", "white"]
}

# Path for leaderboard file
LEADERBOARD_FILE = "leaderboard.json"

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.config(bg="#f0f8ff")
        self.master.geometry("900x600")  # Initial dimensions

        # Game settings
        self.theme = self.random_theme()
        self.words = words_by_theme[self.theme]
        self.word = random.choice(self.words)
        self.guesses = ""
        self.max_attempts = 6
        self.attempts = 0
        self.suggestions_left = 2
        self.score = 0
        self.start_time = 0
        self.timer_duration = 30
        self.timer_running = False

        # UI elements
        self.setup_ui()

    def random_theme(self):
        """Randomly select a theme from the available themes."""
        return random.choice(list(words_by_theme.keys()))

    def setup_ui(self):
        # Display the theme
        self.theme_label = tk.Label(self.master, text=f"Current theme: {self.theme}", font=("Arial", 24), bg="#f0f8ff")
        self.theme_label.pack(pady=20)

        # Display the word
        self.word_label = tk.Label(self.master, text=self.get_display_word(), font=("Arial", 36), bg="#f0f8ff")
        self.word_label.pack(pady=20)

        # Entry for guesses
        self.guess_entry = tk.Entry(self.master, font=("Arial", 36), justify='center')
        self.guess_entry.pack(pady=20)
        self.guess_entry.bind("<Return>", self.make_guess)

        # Labels
        self.attempts_label = tk.Label(self.master, text=f"Attempts left: {self.max_attempts - self.attempts}", font=("Arial", 24), bg="#f0f8ff")
        self.attempts_label.pack(pady=5)

        self.guessed_letters_label = tk.Label(self.master, text="Guessed letters: ", font=("Arial", 24), bg="#f0f8ff")
        self.guessed_letters_label.pack(pady=5)

        self.suggestions_label = tk.Label(self.master, text=f"Suggestions left: {self.suggestions_left}", font=("Arial", 24), bg="#f0f8ff")
        self.suggestions_label.pack(pady=5)

        self.score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Arial", 24), bg="#f0f8ff")
        self.score_label.pack(pady=5)

        self.timer_label = tk.Label(self.master, text=f"Time left: {self.timer_duration}", font=("Arial", 24), bg="#f0f8ff")
        self.timer_label.pack(pady=5)

        # Hangman Canvas
        self.hangman_canvas = tk.Canvas(self.master, width=300, height=300)  # Adjusted Canvas size
        self.hangman_canvas.pack(pady=20)
        self.draw_hangman()

        # Frame for buttons on canvas
        self.button_frame = tk.Frame(self.master, bg="#f0f8ff")
        self.button_frame.pack(pady=10)

        # Smaller buttons
        self.change_theme_button = tk.Button(self.button_frame, text="Change Theme", command=self.change_theme, font=("Arial", 16), bg="#d0e8f2", width=12)
        self.change_theme_button.pack(side=tk.LEFT, padx=5)

        self.restart_button = tk.Button(self.button_frame, text="Restart Game", command=self.reset_game, font=("Arial", 16), bg="#d0e8f2", width=12)
        self.restart_button.pack(side=tk.LEFT, padx=5)

        # Increased size for Show Leaderboard button
        self.leaderboard_button = tk.Button(self.button_frame, text="Show Leaderboard", command=self.show_leaderboard, font=("Arial", 18), bg="#d0e8f2", width=18)
        self.leaderboard_button.pack(side=tk.LEFT, padx=5)

        self.suggestion_button = tk.Button(self.button_frame, text="Get Suggestion", command=self.get_suggestion, font=("Arial", 16), bg="#d0e8f2", width=16)
        self.suggestion_button.pack(side=tk.LEFT, padx=5)

        self.start_timer()

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return

        elapsed_time = int(time.time() - self.start_time)
        time_left = self.timer_duration - elapsed_time
        if time_left <= 0:
            self.timer_running = False
            messagebox.showinfo("Time's up!", f"You lost! The word was '{self.word}'.")
            self.reset_game()
        else:
            self.timer_label.config(text=f"Time left: {time_left}")
            self.master.after(1000, self.update_timer)

    def get_display_word(self):
        return " ".join([letter if letter in self.guesses else "_" for letter in self.word])

    def draw_hangman(self):
        self.hangman_canvas.delete("all")
        stages = [
            "  O  \n /|\\ \n / \\",
            "  O  ",
            "  O  \n  |  ",
            "  O  \n /|  ",
            "  O  \n /|\\ ",
            "  O  \n /|\\ \n  |  ",
            "  O  \n /|\\ \n / \\",
        ]
        self.hangman_canvas.create_text(150, 150, text=stages[self.attempts], font=("Courier", 24), fill="black")

    def make_guess(self, event=None):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if len(guess) == 1 and guess.isalpha():
            if guess in self.guesses:
                messagebox.showinfo("Info", "You already guessed that letter.")
            else:
                self.guesses += guess
                if guess not in self.word:
                    self.attempts += 1
                    self.draw_hangman()
                else:
                    self.score += 5  # Points for correct guesses

                self.word_label.config(text=self.get_display_word())
                self.attempts_label.config(text=f"Attempts left: {self.max_attempts - self.attempts}")
                self.guessed_letters_label.config(text=f"Guessed letters: {self.guesses}")
                self.score_label.config(text=f"Score: {self.score}")

                if self.attempts == self.max_attempts:
                    self.timer_running = False  # Stop the timer
                    messagebox.showinfo("Game Over", f"You lost! The word was '{self.word}'.")
                    self.reset_game()
                elif all(letter in self.guesses for letter in self.word):
                    self.timer_running = False  # Stop the timer
                    self.score += 10 * (self.max_attempts - self.attempts)  # Bonus points
                    messagebox.showinfo("Congratulations", "You guessed the word!")
                    self.update_leaderboard()
                    self.show_top_players()  # Show top players after the game
                    self.reset_game()
        else:
            messagebox.showwarning("Invalid input", "Please enter a single letter.")

    def get_suggestion(self):
        if self.suggestions_left > 0:
            unguessed_letters = [letter for letter in self.word if letter not in self.guesses]
            if unguessed_letters:
                suggestion = random.choice(unguessed_letters)
                self.guesses += suggestion
                self.suggestions_left -= 1
                messagebox.showinfo("Suggestion", f"Try guessing the letter: {suggestion}")
                self.word_label.config(text=self.get_display_word())
                self.guessed_letters_label.config(text=f"Guessed letters: {self.guesses}")
                self.attempts_label.config(text=f"Attempts left: {self.max_attempts - self.attempts}")
                self.suggestions_label.config(text=f"Suggestions left: {self.suggestions_left}")
            else:
                messagebox.showinfo("No suggestions", "You have already guessed all letters.")
        else:
            messagebox.showinfo("No suggestions", "You have no suggestions left.")

    def change_theme(self):
        self.theme = self.random_theme()
        self.words = words_by_theme[self.theme]
        self.word = random.choice(self.words)
        self.guesses = ""
        self.attempts = 0
        self.suggestions_left = 2
        self.score = 0

        # Update the UI
        self.theme_label.config(text=f"Current theme: {self.theme}")
        self.word_label.config(text=self.get_display_word())
        self.attempts_label.config(text=f"Attempts left: {self.max_attempts - self.attempts}")
        self.guessed_letters_label.config(text="Guessed letters: ")
        self.suggestions_label.config(text=f"Suggestions left: {self.suggestions_left}")
        self.score_label.config(text=f"Score: {self.score}")
        self.timer_label.config(text=f"Time left: {self.timer_duration}")
        self.draw_hangman()

        self.start_timer()  # Restart the timer

    def reset_game(self):
        self.theme = self.random_theme()
        self.words = words_by_theme[self.theme]
        self.word = random.choice(self.words)
        self.guesses = ""
        self.attempts = 0
        self.suggestions_left = 2
        self.score = 0
        self.start_time = 0
        self.timer_duration = 30
        self.timer_running = False

        # Update the UI
        self.theme_label.config(text=f"Current theme: {self.theme}")
        self.word_label.config(text=self.get_display_word())
        self.attempts_label.config(text=f"Attempts left: {self.max_attempts - self.attempts}")
        self.guessed_letters_label.config(text="Guessed letters: ")
        self.suggestions_label.config(text=f"Suggestions left: {self.suggestions_left}")
        self.score_label.config(text=f"Score: {self.score}")
        self.timer_label.config(text=f"Time left: {self.timer_duration}")
        self.draw_hangman()

        self.start_timer()  # Restart the timer

    def update_leaderboard(self):
        player_name = simpledialog.askstring("Player Name", "Enter your name:")
        if player_name:
            leaderboard = self.load_leaderboard()
            leaderboard[player_name] = self.score
            leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)[:10])  # Keep top 10 players
            self.save_leaderboard(leaderboard)

    def load_leaderboard(self):
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_leaderboard(self, leaderboard):
        with open(LEADERBOARD_FILE, "w") as file:
            json.dump(leaderboard, file)

    def show_leaderboard(self):
        leaderboard = self.load_leaderboard()
        if leaderboard:
            leaderboard_message = "Leaderboard:\n"
            for i, (player, score) in enumerate(sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)):
                leaderboard_message += f"{i + 1}. {player}: {score}\n"
            messagebox.showinfo("Leaderboard", leaderboard_message)
        else:
            messagebox.showinfo("Leaderboard", "No entries yet.")

    def show_top_players(self):
        leaderboard = self.load_leaderboard()
        if leaderboard:
            top_players_message = "Top Players:\n"
            for i, (player, score) in enumerate(sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)[:3]):
                top_players_message += f"{i + 1}. {player}: {score}\n"
            messagebox.showinfo("Top Players", top_players_message)

if __name__ == "__main__":
    root = tk.Tk()
    hangman_game = HangmanGame(root)
    root.mainloop()
