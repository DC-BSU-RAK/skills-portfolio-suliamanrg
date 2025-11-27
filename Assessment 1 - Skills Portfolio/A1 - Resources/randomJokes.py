import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageFont
import random
import winsound
import time
import io

# GENERATE NEON BACKGROUND IMAGE
def create_neon_background(size):
    w, h = size
    img = Image.new("RGBA", size, (5, 5, 10, 255))
    draw = ImageDraw.Draw(img)

    grid_color = (0, 30, 30, 100)
    step = 50
    for i in range(0, w, step):
        draw.line([(i, 0), (i, h)], fill=grid_color, width=1)
    for j in range(0, h, step):
        draw.line([(0, j), (w, j)], fill=grid_color, width=1)

    glow_size = min(w, h) // 3
    glow_center_x = w // 2
    glow_center_y = h // 2

    glow_layer = Image.new("RGBA", size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)

    glow_draw.ellipse(
        (glow_center_x - glow_size, glow_center_y - glow_size,
         glow_center_x + glow_size, glow_center_y + glow_size),
        fill=(0, 255, 255, 60)
    )

    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=50))
    img.alpha_composite(glow_layer, (0, 0))
    return ImageTk.PhotoImage(img)

# LOAD JOKES
def load_jokes():
    all_jokes = [
        ("Why don't scientists trust atoms?", "Because they make up everything!", "Tech/Science"),
        ("What do you call a fish with no eyes?", "Fsh!", "Pun"),
        ("Why did the scarecrow win an award?", "Because he was outstanding in his field!", "Pun"),
        ("I told my wife she was drawing her eyebrows too high.", "She looked surprised.", "General"),
        ("What's the best thing about Switzerland?", "I don't know, but the flag is a big plus.", "General"),
        ("There are 10 types of people in the world:", "Those who understand binary, and those who don't.", "Tech/Science"),
        ("What's a programmer's favorite place to hang out?", "The foo bar.", "Tech/Science"),
        ("Why don't skeletons fight each other?", "They don't have the guts.", "Pun"),
        ("Did you hear about the restaurant on the moon?", "Great food, no atmosphere.", "General"),
    ]

    jokes_by_genre = {}
    for setup, punch, genre in all_jokes:
        jokes_by_genre.setdefault(genre, []).append((setup, punch))
    return jokes_by_genre

# NEON BUTTON IMAGE CREATOR
def make_button_images(text, size=(240, 60), neon_color=(0, 255, 255)):
    w, h = size
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except:
        font = ImageFont.load_default()

    base_color = (15, 15, 25, 255)

    img = Image.new("RGBA", size, base_color)
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((w - tw) / 2, (h - th) / 2), text, font=font, fill="white")

    glow = Image.new("RGBA", size, base_color)
    g = ImageDraw.Draw(glow)
    g.text(((w - tw) / 2, (h - th) / 2), text, font=font, fill=neon_color)
    glow = glow.filter(ImageFilter.GaussianBlur(6))

    final_glow = Image.new("RGBA", size)
    final_glow.alpha_composite(img)
    final_glow.alpha_composite(glow)

    return ImageTk.PhotoImage(img), ImageTk.PhotoImage(final_glow)

# CUSTOM NEON MESSAGEBOX
def neon_messagebox(title, message):
    box = tk.Toplevel()
    box.title(title)
    box.geometry("420x220")
    box.config(bg="#000000")
    box.overrideredirect(True)

    frame = tk.Frame(box, bg="#00ffff", bd=4)
    frame.pack(fill="both", expand=True, padx=4, pady=4)

    inner = tk.Frame(frame, bg="#050510")
    inner.pack(fill="both", expand=True)

    lbl = tk.Label(inner, text=message, font=("Arial", 16), bg="#050510",
                   fg="#00ffff", wraplength=380, justify="center")
    lbl.pack(pady=25)

    btn = tk.Button(inner, text="OK", font=("Arial", 14, "bold"), fg="#050510",
                    bg="#00ffff", width=10, command=box.destroy, relief=tk.FLAT)
    btn.pack(pady=10)

    box.update_idletasks()
    x = (box.winfo_screenwidth() - box.winfo_width()) // 2
    y = (box.winfo_screenheight() - box.winfo_height()) // 2
    box.geometry(f"+{x}+{y}")

# MAIN APP
class JokeApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Alexa Advanced Joke Assistant")
        self.geometry("700x500")
        self.minsize(600, 400)

        self.jokes_by_genre = load_jokes()
        self.available_genres = list(self.jokes_by_genre.keys())
        self.current_joke = None
        self.current_genre = tk.StringVar(value="General")

        self.bg_image = None
        
       #CODE TO CHANGE ICON IS ADDED HERE.
        icon_path = "tom.png" 
        
        try:
            
            icon_img = Image.open(icon_path)
            icon_img = icon_img.resize((32, 32)) 
            self.app_icon = ImageTk.PhotoImage(icon_img) 
            
            
            self.iconphoto(True, self.app_icon)
        except FileNotFoundError:
            print(f"Warning: Icon file not found at {icon_path}. Using default icon.")
        except Exception as e:
            print(f"Warning: Could not set icon. Error: {e}")
            

        self.container = tk.Frame(self, bg="#050510")
        self.container.place(relwidth=1, relheight=1)

        self.frames = {}
        for F in (StartPage, JokePage, InstructionPage):
            page = F(self.container, self)
            self.frames[F] = page
            page.place(relwidth=1, relheight=1)

        self.bind("<Configure>", self.update_background)

        self.show_frame(StartPage, first=True)

    def update_background(self, event=None):
        w = self.winfo_width()
        h = self.winfo_height()
        self.bg_image = create_neon_background((w, h))

        for frame in self.frames.values():
            if hasattr(frame, "bg_label"):
                frame.bg_label.config(image=self.bg_image)
                frame.bg_label.image = self.bg_image

    def show_frame(self, page, first=False):
        current_frame = self.frames.get(JokePage)
        next_frame = self.frames[page]

        if first:
            next_frame.lift()
            return

        next_frame.place(x=700, y=0)
        next_frame.lift()

        for x in range(700, 0, -100):
            next_frame.place(x=x, y=0)
            next_frame.update()
        next_frame.place(x=0, y=0)

    def random_joke(self, genre=None):
        if genre is None or genre not in self.jokes_by_genre:
            genre = self.current_genre.get()
            if genre not in self.jokes_by_genre:
                genre = "General"

        jokes_list = self.jokes_by_genre.get(genre, [])
        if jokes_list:
            return random.choice(jokes_list)

        all_jokes = [j for group in self.jokes_by_genre.values() for j in group]
        return random.choice(all_jokes) if all_jokes else ("No jokes available!", "")

# STARTING PAGE
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#050510")
        self.controller = controller

        self.bg_label = tk.Label(self, bg="#050510")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        title = tk.Label(self, text="ALEXA JOKE ASSISTANT",
                         fg="#00ffff", bg="#050510",
                         font=("Arial", 28, "bold"))
        title.pack(pady=50)

        normal, glow = make_button_images("Start App")
        start_btn = tk.Label(self, image=normal, bg="#050510")
        start_btn.pack(pady=20)
        start_btn.bind("<Enter>", lambda e: start_btn.config(image=glow))
        start_btn.bind("<Leave>", lambda e: start_btn.config(image=normal))
        start_btn.bind("<Button-1>", lambda e: controller.show_frame(JokePage))

        inst_norm, inst_glow = make_button_images("Instructions", neon_color=(255, 255, 0))
        inst_btn = tk.Label(self, image=inst_norm, bg="#050510")
        inst_btn.pack(pady=10)
        inst_btn.bind("<Enter>", lambda e: inst_btn.config(image=inst_glow))
        inst_btn.bind("<Leave>", lambda e: inst_btn.config(image=inst_norm))
        inst_btn.bind("<Button-1>", lambda e: controller.show_frame(InstructionPage))

        quit_normal, quit_glow = make_button_images("Quit", neon_color=(255, 0, 0))
        quit_btn = tk.Label(self, image=quit_normal, bg="#050510")
        quit_btn.pack(pady=20)
        quit_btn.bind("<Enter>", lambda e: quit_btn.config(image=quit_glow))
        quit_btn.bind("<Leave>", lambda e: quit_btn.config(image=quit_normal))
        quit_btn.bind("<Button-1>", lambda e: controller.quit())

# INSTRUCTION PAGE
class InstructionPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#050510")
        self.controller = controller

        self.bg_label = tk.Label(self, bg="#050510")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        header = tk.Label(self, text="HOW TO USE THE APP",
                          fg="#00ffff", bg="#050510",
                          font=("Arial", 26, "bold"))
        header.pack(pady=40)

        instructions = (
            "How to Use This App:\n\n"
            "• Click 'Start App' from the Home page.\n"
            "• Choose any genre from the dropdown menu.\n"
            "• Click 'Tell me a Joke'.\n"
            "• First the setup appears, then the punchline.\n"
            "• Rate the joke using the 1–5 star system.\n"
            "• Press Back anytime to return to the Home screen.\n\n"
            "Enjoy your neon-powered joke experience!"
        )

        lbl = tk.Label(self, text=instructions, fg="#00ffcc", bg="#050510",
                       font=("Arial", 16), justify="left")
        lbl.pack(pady=20)

        back_norm, back_glow = make_button_images("Back", neon_color=(255, 255, 0))
        back_btn = tk.Label(self, image=back_norm, bg="#050510")
        back_btn.pack(pady=40)
        back_btn.bind("<Enter>", lambda e: back_btn.config(image=back_glow))
        back_btn.bind("<Leave>", lambda e: back_btn.config(image=back_norm))
        back_btn.bind("<Button-1>", lambda e: controller.show_frame(StartPage))

# JOKE PAGE
class JokePage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#050510")
        self.controller = controller

        self.bg_label = tk.Label(self, bg="#050510")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        header = tk.Label(self, text="JOKE MACHINE", fg="#00ff99", bg="#050510",
                          font=("Arial", 26, "bold"))
        header.pack(pady=20)

        genre_frame = tk.Frame(self, bg="#050510")
        genre_frame.pack(pady=10)

        tk.Label(genre_frame, text="Select Genre:", fg="#ff9900", bg="#050510",
                 font=("Arial", 14)).pack(side=tk.LEFT, padx=10)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="#050510", background="#00ffff",
                        foreground="#00ffff", selectbackground="#00ffff", selectforeground="black")

        genre_dropdown = ttk.Combobox(genre_frame, textvariable=self.controller.current_genre,
                                      values=self.controller.available_genres,
                                      state="readonly", width=15, font=("Arial", 12))
        genre_dropdown.pack(side=tk.LEFT, padx=10)

        normal, glow = make_button_images("Tell me a Joke")
        joke_btn = tk.Label(self, image=normal, bg="#050510")
        joke_btn.pack(pady=20)
        joke_btn.bind("<Enter>", lambda e: joke_btn.config(image=glow))
        joke_btn.bind("<Leave>", lambda e: joke_btn.config(image=normal))
        joke_btn.bind("<Button-1>", lambda e: self.show_setup())

        
        rating_lbl = tk.Label(self, text="Rate the last joke:", fg="#00ff99", bg="#050510",
                              font=("Arial", 14))
        rating_lbl.pack(pady=10)

        rating_frame = tk.Frame(self, bg="#050510")
        rating_frame.pack()

        self.star_buttons = []
        for i in range(1, 6):
            btn = tk.Button(rating_frame, text="★", font=("Arial", 20, "bold"),
                            fg="#333333", bg="#050510", bd=0,
                            command=lambda r=i: self.rate_joke(r))
            btn.pack(side=tk.LEFT, padx=5)
            self.star_buttons.append(btn)

        back_norm, back_glow = make_button_images("Back", neon_color=(255, 255, 0))
        back_btn = tk.Label(self, image=back_norm, bg="#050510")
        back_btn.pack(pady=40)
        back_btn.bind("<Enter>", lambda e: back_btn.config(image=back_glow))
        back_btn.bind("<Leave>", lambda e: back_btn.config(image=back_norm))
        back_btn.bind("<Button-1>", lambda e: controller.show_frame(StartPage))

    def rate_joke(self, rating):
        for i, btn in enumerate(self.star_buttons):
            btn.config(fg="#ffcc00" if i < rating else "#333333")

        if self.controller.current_joke:
            genre = self.controller.current_genre.get()
            neon_messagebox("Rating Confirmed",
                            f"You rated the {genre} joke {rating} out of 5 stars!")
        else:
            neon_messagebox("Rating Error", "Please hear a joke first.")

    def show_setup(self):
        for btn in self.star_buttons:
            btn.config(fg="#333333")

        genre = self.controller.current_genre.get()
        joke = self.controller.random_joke(genre)
        self.controller.current_joke = joke

        setup, _ = joke
        neon_messagebox("Setup 😂", setup)
        

        self.after(3000, self.show_punchline)

    def show_punchline(self):
        _, punch = self.controller.current_joke
        neon_messagebox("Punchline 🤣", punch)
        

# ----------------------------------------------------
# RUN APP
# ----------------------------------------------------
if __name__ == "__main__":
    JokeApp().mainloop()
