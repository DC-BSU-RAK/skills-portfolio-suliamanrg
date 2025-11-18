import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# SCORE BOARD SECTION
score = 0
question_count = 0
correct_answer = 0
attempt = 1
difficulty = "Easy"


# MAIN CLASS SECTION
class MathQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")

        # FULLSCREEN & RESIZABLE
        self.root.state("zoomed")
        self.root.minsize(900, 600)

        # Resize event
        self.root.bind("<Configure>", self.resize_bg)

        # LOAD BACKGROUND
        self.original_bg = Image.open("download.jpeg")   # Your background image
        self.bg_photo = ImageTk.PhotoImage(self.original_bg)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Start app
        self.main_menu()

    # RESIZE BACKGROUND
    def resize_bg(self, event):
        try:
            resized = self.original_bg.resize((event.width, event.height))
            self.bg_photo = ImageTk.PhotoImage(resized)
            self.bg_label.config(image=self.bg_photo)
        except:
            pass

    # CLEAR SCREEN
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Re-add background
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # MAIN MENU
    def main_menu(self):
        self.clear()

        tk.Label(
            self.root,
            text="MATH QUIZ",
            font=("Arial", 40, "bold"),
            fg="yellow",
            bg="#000000"
        ).place(relx=0.5, rely=0.18, anchor="center")

        tk.Button(
            self.root, text="Start Quiz",
            font=("Arial", 26), bg="yellow", fg="black",
            command=self.select_difficulty
        ).place(relx=0.5, rely=0.40, anchor="center")

        tk.Button(
            self.root, text="How It Works",
            font=("Arial", 22), bg="yellow", fg="black",
            command=self.how_it_works
        ).place(relx=0.5, rely=0.52, anchor="center")

        tk.Button(
            self.root, text="Exit",
            font=("Arial", 22), bg="red", fg="white",
            command=self.root.quit
        ).place(relx=0.5, rely=0.63, anchor="center")

    # HOW IT WORKS PAGE
    def how_it_works(self):
        self.clear()

        tk.Label(
            self.root,
            text="HOW THE MATH QUIZ WORKS",
            font=("Arial", 40, "bold"),
            fg="yellow",
            bg="#000"
        ).place(relx=0.5, rely=0.15, anchor="center")

        instructions = (
            " Welcome to the Math Quiz!\n\n"
            "Here's how the game works:\n\n"
            "1️- Choose a difficulty (Easy, Moderate, Advanced)\n"
            "2️- You will get 10 math questions\n"
            "3️- Each question allows up to TWO attempts\n\n"
            "Scoring System:\n"
            "   ✔ 10 points — correct on first try\n"
            "   ✔ 5 points — correct on second try\n"
            "   ✘ 0 points — wrong both tries\n\n"
            " Goal: Score as high as possible out of 100!\n\n"
            " Good luck!"
        )

        tk.Label(
            self.root,
            text=instructions,
            font=("Arial", 22),
            fg="white",
            bg="#000",
            justify="left"
        ).place(relx=0.5, rely=0.55, anchor="center")

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 22),
            bg="yellow",
            fg="black",
            command=self.main_menu
        ).place(relx=0.5, rely=0.87, anchor="center")

    # SELECT DIFFICULTY
    def select_difficulty(self):
        self.clear()

        tk.Label(
            self.root, text="Select Difficulty Level",
            font=("Arial", 36, "bold"), fg="yellow",
            bg="#000"
        ).place(relx=0.5, rely=0.18, anchor="center")

        tk.Button(
            self.root, text="Easy (1–9)", font=("Arial", 26),
            bg="yellow", command=lambda: self.start_quiz("Easy")
        ).place(relx=0.5, rely=0.40, anchor="center")

        tk.Button(
            self.root, text="Moderate (10–99)", font=("Arial", 26),
            bg="yellow", command=lambda: self.start_quiz("Moderate")
        ).place(relx=0.5, rely=0.50, anchor="center")

        tk.Button(
            self.root, text="Advanced (100–9999)", font=("Arial", 26),
            bg="yellow", command=lambda: self.start_quiz("Advanced")
        ).place(relx=0.5, rely=0.60, anchor="center")

        tk.Button(
            self.root, text="Exit", font=("Arial", 22),
            bg="red", fg="white", command=self.root.quit
        ).place(relx=0.5, rely=0.75, anchor="center")

    # START QUIZ
    def start_quiz(self, level):
        global score, question_count, attempt, difficulty

        self.clear()

        score = 0
        question_count = 0
        difficulty = level
        attempt = 1

        self.q_label = tk.Label(
            self.root, text="", font=("Arial", 36, "bold"),
            fg="yellow", bg="#000"
        )
        self.q_label.place(relx=0.5, rely=0.20, anchor="center")

        self.score_label = tk.Label(
            self.root, text="Score: 0",
            font=("Arial", 26), fg="white", bg="#000"
        )
        self.score_label.place(relx=0.85, rely=0.10, anchor="center")

        self.answer = tk.Entry(
            self.root, font=("Arial", 30),
            width=10, justify="center"
        )
        self.answer.place(relx=0.5, rely=0.40, anchor="center")

        tk.Button(
            self.root, text="Submit", font=("Arial", 26),
            bg="yellow", fg="black", command=self.check_answer
        ).place(relx=0.5, rely=0.50, anchor="center")

        tk.Button(
            self.root, text="Exit", font=("Arial", 16),
            bg="red", fg="white", command=self.root.quit
        ).place(relx=0.90, rely=0.93, anchor="center")

        self.feedback = tk.Label(
            self.root, text="", font=("Arial", 26),
            fg="white", bg="#000"
        )
        self.feedback.place(relx=0.5, rely=0.60, anchor="center")

        self.new_question()

    # NEW QUESTION
    def new_question(self):
        global correct_answer, question_count, attempt

        question_count += 1
        attempt = 1

        if difficulty == "Easy":
            a = random.randint(1, 9)
            b = random.randint(1, 9)
        elif difficulty == "Moderate":
            a = random.randint(10, 99)
            b = random.randint(10, 99)
        else:
            a = random.randint(100, 9999)
            b = random.randint(1, 50)

        op = random.choice(["+", "-", "*"])

        if op == "+":
            correct_answer = a + b
        elif op == "-":
            correct_answer = a - b
        else:
            correct_answer = a * b

        self.q_label.config(text=f"{a} {op} {b} = ?")
        self.answer.delete(0, tk.END)
        self.feedback.config(text="")

    # CHECK ANSWER
    def check_answer(self):
        global score, attempt, question_count

        try:
            user = int(self.answer.get())
        except:
            self.feedback.config(text="Enter a valid number!", fg="red")
            return

        if user == correct_answer:
            if attempt == 1:
                score += 10
                self.feedback.config(text="Correct! +10 🦇", fg="yellow")
            else:
                score += 5
                self.feedback.config(text="Correct! +5 🦇", fg="lightgreen")

            self.score_label.config(text=f"Score: {score}")

            if question_count == 10:
                self.results()
            else:
                self.root.after(800, self.new_question)

        else:
            if attempt == 1:
                attempt = 2
                self.feedback.config(text="Wrong! Try again…", fg="red")
            else:
                self.feedback.config(
                    text=f"Wrong! Correct = {correct_answer}",
                    fg="red"
                )

                if question_count == 10:
                    self.root.after(1200, self.results)
                else:
                    self.root.after(1200, self.new_question)

    # RESULTS SCREEN
    def results(self):
        self.clear()

        percent = (score / 100) * 100

        if percent >= 90:
            grade = "A+"
        elif percent >= 80:
            grade = "A"
        elif percent >= 70:
            grade = "B"
        elif percent >= 60:
            grade = "C"
        else:
            grade = "F"

        tk.Label(
            self.root, text="RESULTS",
            font=("Arial", 44, "bold"), fg="yellow", bg="#000"
        ).place(relx=0.5, rely=0.15, anchor="center")

        tk.Label(
            self.root, text=f"Total Score: {score}/100",
            font=("Arial", 30), fg="white", bg="#000"
        ).place(relx=0.5, rely=0.30, anchor="center")

        tk.Label(
            self.root, text=f"Percentage: {percent:.1f}%",
            font=("Arial", 30), fg="white", bg="#000"
        ).place(relx=0.5, rely=0.40, anchor="center")

        tk.Label(
            self.root, text=f"Rank: {grade}",
            font=("Arial", 30), fg="yellow", bg="#000"
        ).place(relx=0.5, rely=0.50, anchor="center")

        # SCORING RULES
        tk.Label(
            self.root,
            text="Scoring System:\n✔ 10 points — Correct on 1st try\n✔ 5 points — Correct on 2nd try\n✘ 0 points — Wrong both tries",
            font=("Arial", 22, "bold"),
            fg="lightblue",
            bg="#000",
            justify="center"
        ).place(relx=0.5, rely=0.67, anchor="center")

        tk.Button(
            self.root, text="Play Again",
            font=("Arial", 26), bg="yellow",
            command=self.main_menu
        ).place(relx=0.5, rely=0.82, anchor="center")

        tk.Button(
            self.root, text="Exit",
            font=("Arial", 22), bg="red", fg="white",
            command=self.root.quit
        ).place(relx=0.5, rely=0.90, anchor="center")


# RUN APP
root = tk.Tk()
MathQuiz(root)
root.mainloop()
