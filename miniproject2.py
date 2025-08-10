import tkinter as tk
from tkinter import ttk
import time
import random

# Paragraphs by difficulty
PARAGRAPHS = {
    "Easy": [
        "The quick brown fox jumps over the lazy dog.",
        "Typing is a useful skill that can save you time."
    ],
    "Medium": [
        "Python is a high-level programming language known for its readability.",
        "Tkinter is Python's standard library for creating graphical user interfaces."
    ],
    "Hard": [
        "Data science uses scientific methods, algorithms, and systems to extract insights from structured and unstructured data.",
        "Artificial Intelligence is transforming industries by automating complex tasks and improving decision-making."
    ]
}

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⌨ Typing Speed Test")
        self.root.geometry("950x500")
        self.root.configure(bg="#f4f6f7")

        self.paragraph = ""
        self.start_time = 0
        self.timer_running = False

        self.create_widgets()

    def create_widgets(self):
        # Title
        header = tk.Label(self.root, text="Typing Speed Test", font=("Helvetica", 26, "bold"), bg="#f4f6f7", fg="#2c3e50")
        header.pack(pady=15)

        # Difficulty Selector
        difficulty_frame = tk.Frame(self.root, bg="#f4f6f7")
        difficulty_frame.pack()
        tk.Label(difficulty_frame, text="Difficulty:", font=("Helvetica", 14), bg="#f4f6f7").pack(side=tk.LEFT, padx=5)
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_menu = ttk.Combobox(difficulty_frame, textvariable=self.difficulty_var, values=list(PARAGRAPHS.keys()), state="readonly", width=10)
        difficulty_menu.pack(side=tk.LEFT, padx=5)

        # Timer
        self.timer_label = tk.Label(self.root, text="Time: 0s", font=("Helvetica", 14), bg="#f4f6f7", fg="#555")
        self.timer_label.pack(pady=5)

        # Paragraph
        self.paragraph_label = tk.Label(self.root, text="", wraplength=900, font=("Helvetica", 16), justify="left", bg="#ecf0f1", fg="#2c3e50", pady=10, padx=10, relief="groove")
        self.paragraph_label.pack(pady=15, fill="x", padx=20)

        # Typing Box
        self.input_text = tk.Text(self.root, height=6, width=100, font=("Helvetica", 14), state=tk.DISABLED, wrap="word", relief="solid", bd=1)
        self.input_text.pack(pady=10)
        self.input_text.bind("<KeyRelease>", self.check_text)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#f4f6f7")
        btn_frame.pack(pady=15)

        self.start_button = tk.Button(btn_frame, text="Start Test", command=self.start_test, font=("Helvetica", 14, "bold"),
                                      bg="#27ae60", fg="white", padx=15, pady=8, relief="flat", activebackground="#2ecc71")
        self.start_button.grid(row=0, column=0, padx=10)

        self.reset_button = tk.Button(btn_frame, text="Reset Test", command=self.reset_test, font=("Helvetica", 14, "bold"),
                                      bg="#c0392b", fg="white", padx=15, pady=8, relief="flat", activebackground="#e74c3c")
        self.reset_button.grid(row=0, column=1, padx=10)

        # Results Box
        self.results_frame = tk.LabelFrame(self.root, text="Results", font=("Helvetica", 14, "bold"), bg="#f4f6f7", fg="#2c3e50", labelanchor="n")
        self.results_frame.pack(pady=10, fill="x", padx=20)

        self.wpm_label = tk.Label(self.results_frame, text="WPM: 0", font=("Helvetica", 14), bg="#f4f6f7")
        self.wpm_label.grid(row=0, column=0, padx=20, pady=5)

        self.accuracy_label = tk.Label(self.results_frame, text="Accuracy: 0%", font=("Helvetica", 14), bg="#f4f6f7")
        self.accuracy_label.grid(row=0, column=1, padx=20, pady=5)

    def start_test(self):
        self.paragraph = random.choice(PARAGRAPHS[self.difficulty_var.get()])
        self.paragraph_label.config(text=self.paragraph, fg="#2c3e50")
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete("1.0", tk.END)
        self.input_text.focus()
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

        # Reset stats
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 0%")

    def reset_test(self):
        self.timer_running = False
        self.input_text.config(state=tk.DISABLED)
        self.paragraph_label.config(text="", fg="#2c3e50")
        self.timer_label.config(text="Time: 0s")
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 0%")

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.root.after(1000, self.update_timer)

    def check_text(self, event):
        typed_text = self.input_text.get("1.0", "end-1c")

        # Paragraph color feedback
        if self.paragraph.startswith(typed_text):
            self.paragraph_label.config(fg="green")
        else:
            self.paragraph_label.config(fg="red")

        self.update_stats(typed_text)

        # End when done
        if typed_text.strip() == self.paragraph:
            self.timer_running = False
            self.input_text.config(state=tk.DISABLED)

    def update_stats(self, typed_text):
        time_taken = max(time.time() - self.start_time, 1)
        words = typed_text.strip().split()
        correct_words = sum(1 for i, w in enumerate(words) if i < len(self.paragraph.split()) and w == self.paragraph.split()[i])

        wpm = (correct_words / time_taken) * 60
        correct_chars = sum(1 for i, c in enumerate(typed_text) if i < len(self.paragraph) and c == self.paragraph[i])
        accuracy = (correct_chars / len(self.paragraph)) * 100

        self.wpm_label.config(text=f"WPM: {wpm:.2f}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()