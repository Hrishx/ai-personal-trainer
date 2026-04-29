import tkinter as tk
import subprocess

def start_trainer():
    subprocess.run(["python", "main.py"])

app = tk.Tk()
app.title("AI Fitness Coach")
app.geometry("400x300")

title = tk.Label(app, text="AI Fitness Coach", font=("Arial",20))
title.pack(pady=20)

desc = tk.Label(
    app,
    text="Real-time exercise analysis using AI",
    font=("Arial",12)
)
desc.pack(pady=10)

start_btn = tk.Button(
    app,
    text="Start Workout Analysis",
    font=("Arial",14),
    command=start_trainer
)
start_btn.pack(pady=20)

app.mainloop()