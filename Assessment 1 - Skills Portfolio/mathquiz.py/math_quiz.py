import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import sys

#Utility function to play a notification sound across platforms

def play_beep(ok=True):
    try:
        if sys.platform.startswith("win"):
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK if ok else winsound.MB_ICONHAND)
        else:
            print("\a", end="")
    except Exception:
        pass

#code for app's theme color etc
class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Math Quiz — Sharpen the Mind")
        self.root.geometry("720x520")
        self.root.minsize(560, 420)

        # Colors / theme
        self.light = {
            "bg":"#E8EEF6",
            "fg":"#0f172a",
            "accent":"#4F46E5",
            "ok":"#16a34a",
            "warn":"#ef4444",
            "card":"#ffffff"
        }
        self.dark = {
            "bg":"#0B1220",
            "fg":"#E6E6E6",
            "accent":"#7C3AED",
            "ok":"#34d399",
            "warn":"#f87171",
            "card":"#111827"
        }
        self.theme = self.light

        # code for Game state
        self.difficulty = 1
        self.score = 0
        self.q_num = 0
        self.second_try = False
        self.num1 = self.num2 = 0
        self.operation = "+"
        self.correct_answer = 0
        self.best_streak = 0
        self.streak = 0
        self.total_correct = 0
        self.total_start_time = None
        self.question_deadline = None
        self.time_per_q = 20   # seconds
        self.timer_job = None
        self.allow_mult = tk.BooleanVar(value=True)
        self.allow_div = tk.BooleanVar(value=False)

        # Fonts
        self.fonts = {}
        self.root.bind("<Configure>", self._resize_fonts)

        # Pages
        self.container = tk.Frame(self.root, bg=self.theme["bg"])
        self.container.pack(fill="both", expand=True)

        self._build_topbar()
        self._build_pages()
        self.show_page(self.start_page)

        # Keyboard shortcuts
        self.root.bind("<Return>", lambda e: self._submit_if_visible())
        self.root.bind("<Escape>", lambda e: self.root.quit())

    # Adjusts text size automatically when you resize the window

    def _resize_fonts(self, event=None):
        w = max(self.root.winfo_width(), 560)
        h = max(self.root.winfo_height(), 420)
        base = int(min(w, h) / 26)

        def mk(size, weight="normal"):
            return ("Segoe UI", max(size, 10), weight)

        self.fonts["h1"] = mk(base+12, "bold")
        self.fonts["h2"] = mk(base+6, "bold")
        self.fonts["h3"] = mk(base+2, "bold")
        self.fonts["p"]  = mk(base)
        self.fonts["btn"] = mk(base, "bold")
        self.fonts["mono"] = ("Consolas", max(base, 12), "bold")

        # Apply fonts if widgets exist
        if hasattr(self, "start_title"):
            self.start_title.config(font=self.fonts["h1"])
            self.start_sub.config(font=self.fonts["p"])
            for b in (self.start_btn, self.rules_btn):
                b.config(font=self.fonts["btn"])

        if hasattr(self, "mode_title"):
            self.mode_title.config(font=self.fonts["h2"])
            self.level_lbl.config(font=self.fonts["p"])
            for b in (self.easy_btn, self.mod_btn, self.adv_btn):
                b.config(font=self.fonts["btn"])
            self.ops_lbl.config(font=self.fonts["p"])
            self.cb_mul.config(font=self.fonts["p"])
            self.cb_div.config(font=self.fonts["p"])
            self.play_btn.config(font=self.fonts["btn"])

        if hasattr(self, "quiz_title"):
            self.quiz_title.config(font=self.fonts["h3"])
            self.quiz_question.config(font=self.fonts["mono"])
            self.timer_lbl.config(font=self.fonts["p"])
            self.msg_lbl.config(font=self.fonts["p"])
            self.score_lbl.config(font=self.fonts["p"])
            self.entry.config(font=self.fonts["h2"])
            self.submit_btn.config(font=self.fonts["btn"])
            self.skip_btn.config(font=self.fonts["btn"])

        if hasattr(self, "end_title"):
            self.end_title.config(font=self.fonts["h2"])
            self.end_stats.config(font=self.fonts["p"])
            self.play_again_btn.config(font=self.fonts["btn"])
            self.exit_btn.config(font=self.fonts["btn"])

    #Top bar (theme toggle + progress) 
    def _build_topbar(self):
        self.topbar = tk.Frame(self.container, bg=self.theme["bg"])
        self.topbar.pack(fill="x", side="top")

        self.theme_btn = ttk.Button(self.topbar, text="🌙 Dark", command=self.toggle_theme)
        self.theme_btn.pack(side="right", padx=10, pady=10)

        self.progress = ttk.Progressbar(self.topbar, mode="determinate", maximum=10)
        self.progress.pack(side="right", padx=10, pady=14)
        self._style_ttk()

    def _style_ttk(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TProgressbar", troughcolor=self.theme["card"], background=self.theme["accent"])

    def toggle_theme(self):
        self.theme = self.dark if self.theme is self.light else self.light
        self.container.config(bg=self.theme["bg"])
        for f in (self.start_page, self.mode_page, self.quiz_page, self.end_page):
            f.config(bg=self.theme["bg"])
        def recolor(frame):
            for w in frame.winfo_children():
                try:
                    if isinstance(w, (tk.Label, tk.Frame, tk.Entry, tk.Text)):
                        w.config(bg=self.theme["bg"], fg=self.theme["fg"])
                except Exception:
                    pass
        for f in (self.start_page, self.mode_page, self.quiz_page, self.end_page):
            recolor(f)
        self._style_ttk()
        self.theme_btn.config(text="🌞 Light" if self.theme is self.dark else "🌙 Dark")

    #Pages
    def _build_pages(self):
        # Start
        self.start_page = tk.Frame(self.container, bg=self.theme["bg"])
        self.start_title = tk.Label(self.start_page, text="بِسْمِ اللَّهِ — Math Quiz", fg=self.theme["fg"], bg=self.theme["bg"])
        self.start_sub = tk.Label(self.start_page, text="10 questions. Two tries. Beat the clock. Earn bonuses. 🎯",
                                  fg=self.theme["fg"], bg=self.theme["bg"])
        self.start_btn = tk.Button(self.start_page, text="Start", command=lambda: self.show_page(self.mode_page),
                                   bd=0, padx=18, pady=10, fg="#fff", bg=self.theme["accent"], activebackground=self.theme["accent"])
        self.rules_btn = tk.Button(self.start_page, text="How it works", command=self._show_rules,
                                   bd=0, padx=12, pady=10, fg=self.theme["fg"], bg=self.theme["card"], activebackground=self.theme["card"])
        self.start_title.pack(pady=24)
        self.start_sub.pack(pady=6)
        self.start_btn.pack(pady=16)
        self.rules_btn.pack()

        # Mode
        self.mode_page = tk.Frame(self.container, bg=self.theme["bg"])
        self.mode_title = tk.Label(self.mode_page, text="Select Your Challenge", fg=self.theme["fg"], bg=self.theme["bg"])
        self.level_lbl = tk.Label(self.mode_page, text="Difficulty:", fg=self.theme["fg"], bg=self.theme["bg"])
        btn_wrap = tk.Frame(self.mode_page, bg=self.theme["bg"])
        self.easy_btn = tk.Button(btn_wrap, text="Easy", command=lambda: self._pick_level(1),
                                  bd=0, padx=14, pady=10, fg="#0f172a", bg="#a7f3d0", activebackground="#a7f3d0")
        self.mod_btn  = tk.Button(btn_wrap, text="Moderate", command=lambda: self._pick_level(2),
                                  bd=0, padx=14, pady=10, fg="#1f2937", bg="#fde68a", activebackground="#fde68a")
        self.adv_btn  = tk.Button(btn_wrap, text="Advanced", command=lambda: self._pick_level(3),
                                  bd=0, padx=14, pady=10, fg="#fff", bg="#f87171", activebackground="#f87171")

        self.ops_lbl = tk.Label(self.mode_page, text="Extra Operations:", fg=self.theme["fg"], bg=self.theme["bg"])
        self.cb_mul = tk.Checkbutton(self.mode_page, text="× (Multiplication)", variable=self.allow_mult,
                                     bg=self.theme["bg"], fg=self.theme["fg"], selectcolor=self.theme["card"], activebackground=self.theme["bg"])
        self.cb_div = tk.Checkbutton(self.mode_page, text="÷ (No remainders)", variable=self.allow_div,
                                     bg=self.theme["bg"], fg=self.theme["fg"], selectcolor=self.theme["card"], activebackground=self.theme["bg"])

        self.play_btn = tk.Button(self.mode_page, text="Play ▶", command=self.start_quiz,
                                  bd=0, padx=18, pady=10, fg="#fff", bg=self.theme["accent"], activebackground=self.theme["accent"])

        self.mode_title.pack(pady=18)
        self.level_lbl.pack(pady=(4,8))
        btn_wrap.pack()
        self.easy_btn.grid(row=0, column=0, padx=6, pady=6)
        self.mod_btn.grid(row=0, column=1, padx=6, pady=6)
        self.adv_btn.grid(row=0, column=2, padx=6, pady=6)
        self.ops_lbl.pack(pady=(18,6))
        self.cb_mul.pack()
        self.cb_div.pack()
        self.play_btn.pack(pady=18)

        # Quiz
        self.quiz_page = tk.Frame(self.container, bg=self.theme["bg"])
        top_info = tk.Frame(self.quiz_page, bg=self.theme["bg"])
        self.quiz_title = tk.Label(top_info, text="Question 1 of 10", fg=self.theme["fg"], bg=self.theme["bg"])
        self.timer_lbl = tk.Label(top_info, text="⏱ 20s", fg=self.theme["fg"], bg=self.theme["bg"])
        self.score_lbl = tk.Label(top_info, text="Score: 0", fg=self.theme["fg"], bg=self.theme["bg"])
        self.quiz_title.pack(side="left", padx=6)
        self.timer_lbl.pack(side="right", padx=6)
        self.score_lbl.pack(side="right", padx=6)
        top_info.pack(fill="x", pady=8)

        center = tk.Frame(self.quiz_page, bg=self.theme["bg"])
        self.quiz_question = tk.Label(center, text="0 + 0 = ?", fg=self.theme["fg"], bg=self.theme["bg"])
        self.entry = tk.Entry(center, justify="center", bd=0, highlightthickness=0, insertwidth=3, fg=self.theme["fg"], bg=self.theme["card"])
        self.entry.bind("<Control-BackSpace>", lambda e: self._clear_entry())
        self.entry.bind("<KP_Enter>", lambda e: self.check_answer())
        self.msg_lbl = tk.Label(center, text="Type your answer and press Enter.", fg=self.theme["fg"], bg=self.theme["bg"])
        self.quiz_question.pack(pady=(16,10))
        self.entry.pack(ipady=8, ipadx=8, padx=12, pady=6, fill="x")
        self.msg_lbl.pack(pady=6)
        center.pack(fill="both", expand=True)

        action = tk.Frame(self.quiz_page, bg=self.theme["bg"])
        self.submit_btn = tk.Button(action, text="Submit", command=self.check_answer,
                                    bd=0, padx=16, pady=10, fg="#fff", bg=self.theme["accent"], activebackground=self.theme["accent"])
        self.skip_btn = tk.Button(action, text="Skip (-2 pts)", command=self.skip_question,
                                  bd=0, padx=12, pady=10, fg=self.theme["fg"], bg=self.theme["card"], activebackground=self.theme["card"])
        self.submit_btn.pack(side="left", padx=8, pady=8)
        self.skip_btn.pack(side="left", padx=8, pady=8)
        action.pack(pady=(0,14))

        # Confetti canvas (celebration)
        self.fx_canvas = tk.Canvas(self.quiz_page, bg=self.theme["bg"], highlightthickness=0)
        self.fx_canvas.pack(fill="both", expand=True)
        self.confetti_items = []

        # End
        self.end_page = tk.Frame(self.container, bg=self.theme["bg"])
        self.end_title = tk.Label(self.end_page, text="🎉 Quiz Complete!", fg=self.theme["fg"], bg=self.theme["bg"])
        self.end_stats = tk.Label(self.end_page, text="", fg=self.theme["fg"], bg=self.theme["bg"], justify="left")
        btns = tk.Frame(self.end_page, bg=self.theme["bg"])
        self.play_again_btn = tk.Button(btns, text="Play Again", command=lambda: self.show_page(self.mode_page),
                                        bd=0, padx=16, pady=10, fg="#fff", bg=self.theme["accent"], activebackground=self.theme["accent"])
        self.exit_btn = tk.Button(btns, text="Exit", command=self.root.quit,
                                  bd=0, padx=16, pady=10, fg="#fff", bg=self.theme["warn"], activebackground=self.theme["warn"])
        self.end_title.pack(pady=18)
        self.end_stats.pack(pady=8)
        btns.pack(pady=10)
        self.play_again_btn.grid(row=0, column=0, padx=6)
        self.exit_btn.grid(row=0, column=1, padx=6)

        self._resize_fonts()

    def show_page(self, page):
        for p in (self.start_page, self.mode_page, self.quiz_page, self.end_page):
            p.pack_forget()
        page.pack(fill="both", expand=True)

    #Flow 
    def _show_rules(self):
        messagebox.showinfo(
            "How to Play",
            "• 10 questions. Two attempts each.\n"
            "• First-try correct = +10 points. Second try = +5 points.\n"
            f"• Timer: {self.time_per_q}s per question. Fast answers earn up to +5 bonus.\n"
            "• Streaks raise your bragging rights. Skip costs 2 points.\n"
            "• Choose difficulty and extra operations on the next screen."
        )

    def _pick_level(self, level):
        self.difficulty = level
        for btn in (self.easy_btn, self.mod_btn, self.adv_btn):
            btn.config(relief="raised")
        (self.easy_btn if level==1 else self.mod_btn if level==2 else self.adv_btn).config(relief="sunken")

    def start_quiz(self):
        self.score = 0
        self.q_num = 0
        self.streak = 0
        self.best_streak = 0
        self.total_correct = 0
        self.total_start_time = time.time()
        self.progress['value'] = 0
        self.show_page(self.quiz_page)
        self.next_question()

    def randomInt(self):
        if self.difficulty == 1:
            return random.randint(1, 9)
        elif self.difficulty == 2:
            return random.randint(10, 99)
        else:
            return random.randint(100, 999)

    def decideOperation(self):
        ops = ["+", "-"]
        if self.allow_mult.get():
            ops.append("×")
        if self.allow_div.get():
            ops.append("÷")
        return random.choice(ops)

    def next_question(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        if self.q_num == 10:
            self.display_results()
            return

        self.q_num += 1
        self.second_try = False

        self.num1 = self.randomInt()
        self.num2 = self.randomInt()
        self.operation = self.decideOperation()

        if self.operation == "+":
            self.correct_answer = self.num1 + self.num2
        elif self.operation == "-":
            self.correct_answer = self.num1 - self.num2
        elif self.operation == "×":
            self.correct_answer = self.num1 * self.num2
        else:
            self.correct_answer = max(1, random.randint(2, 12))
            self.num2 = self.correct_answer
            self.num1 = self.correct_answer * random.randint(2, 12)

        self.quiz_title.config(text=f"Question {self.q_num} of 10")
        self.quiz_question.config(text=f"{self.num1} {self.operation} {self.num2} = ?")
        self.entry.delete(0, tk.END)
        self.entry.focus_set()
        self.msg_lbl.config(text=random.choice([
            "Breathe. Focus. You’ve got this. 🤝",
            "Small steps. Strong mind. 💪",
            "Sabr + Effort = Success. 🌟",
            "Aim true. Type clean. 🎯",
        ]))
        self.score_lbl.config(text=f"Score: {self.score}")
        self.progress['value'] = self.q_num - 1

        self.question_deadline = time.time() + self.time_per_q
        self._tick_timer()
        self.fx_canvas.delete("all")
        self.confetti_items.clear()

    def _tick_timer(self):
        remaining = int(self.question_deadline - time.time())
        if remaining < 0:
            self.timer_lbl.config(text="⏱ 0s")
            self._time_up()
            return
        self.timer_lbl.config(text=f"⏱ {remaining}s")
        self.timer_job = self.root.after(200, self._tick_timer)

    def _time_up(self):
        play_beep(ok=False)
        self.msg_lbl.config(text=f"Time’s up! Correct answer: {self.correct_answer}", fg=self.theme["warn"])
        self.streak = 0
        self.root.after(1200, self.next_question)

    def _clear_entry(self):
        self.entry.delete(0, tk.END)

    def _submit_if_visible(self):
        if self.quiz_page.winfo_ismapped():
            self.check_answer()

    def check_answer(self):
        text = self.entry.get().strip()
        if not text:
            play_beep(ok=False)
            self.msg_lbl.config(text="Enter an answer!", fg=self.theme["warn"])
            return
        try:
            ans = int(text)
        except ValueError:
            play_beep(ok=False)
            self.msg_lbl.config(text="Numbers only please!", fg=self.theme["warn"])
            return

        fast_bonus = max(0, int(self.time_per_q - (self.question_deadline - time.time())))
        fast_bonus = max(0, 5 - int(fast_bonus / 3))

        if ans == self.correct_answer:
            play_beep(ok=True)
            self.total_correct += 1
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            gain = (10 if not self.second_try else 5) + fast_bonus
            self.score += gain
            self.msg_lbl.config(text=f"✅ Correct! +{gain} pts ({fast_bonus} fast bonus)", fg=self.theme["ok"])
            self._confetti()
            self.progress['value'] = self.q_num
            self.root.after(800, self.next_question)
        else:
            play_beep(ok=False)
            if self.second_try:
                self.msg_lbl.config(text=f"❌ Nope! Answer: {self.correct_answer}", fg=self.theme["warn"])
                self.streak = 0
                self.root.after(1000, self.next_question)
            else:
                self.msg_lbl.config(text="Not quite. Try again ⏳", fg=self.theme["warn"])
                self.second_try = True
                self.entry.delete(0, tk.END)

    def skip_question(self):
        play_beep(ok=False)
        self.score = max(0, self.score - 2)
        self.msg_lbl.config(text=f"Skipped. -2 pts (Correct: {self.correct_answer})", fg=self.theme["warn"])
        self.root.after(600, self.next_question)

    def _confetti(self):
        for _ in range(15):
            x = random.randint(0, self.root.winfo_width())
            y = random.randint(0, self.root.winfo_height()//2)
            size = random.randint(4, 8)
            c = self.fx_canvas.create_oval(x, y, x+size, y+size,
                                           fill=random.choice(["#f87171", "#34d399", "#60a5fa", "#facc15", "#c084fc"]),
                                           outline="")
            self.confetti_items.append(c)
            
        #start animaation loop    
        self._animate_confetti()


    def _animate_confetti(self):
        for c in list(self.confetti_items):
            self.fx_canvas.move(c, 0, random.randint(3, 7))
            if self.fx_canvas.coords(c)[1] > self.root.winfo_height():
                self.fx_canvas.delete(c)
                self.confetti_items.remove(c)
        if self.confetti_items:
            self.root.after(50, self._animate_confetti)

#results screen
    def display_results(self):
        total_time = time.time() - self.total_start_time
        self.end_stats.config(text=(
            f"Total Score: {self.score}\n"
            f"Accuracy: {self.total_correct}/10\n"
            f"Best Streak: {self.best_streak}\n"
            f"Time Taken: {total_time:.1f}s"
        ))
        self.show_page(self.end_page)


#Main part
if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()