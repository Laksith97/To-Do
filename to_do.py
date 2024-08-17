import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime
import random

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do App")
        self.master.geometry("500x600")
        self.master.configure(bg='#f0f0f0')
        self.tasks = self.load_tasks()
        self.colors = ['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA', '#FFD8B8']
        self.last_color = None
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.master, text="My To-Do List", font=("Helvetica", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)

        self.task_entry = ttk.Entry(self.master, width=50, font=("Helvetica", 12))
        self.task_entry.pack(pady=10)

        self.add_button = ttk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.task_frame = tk.Frame(self.master, bg='#f0f0f0')
        self.task_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.task_canvas = tk.Canvas(self.task_frame, bg='#f0f0f0')
        self.task_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.task_frame, orient=tk.VERTICAL, command=self.task_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.task_canvas.bind('<Configure>', lambda e: self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all")))

        self.inner_frame = tk.Frame(self.task_canvas, bg='#f0f0f0')
        self.task_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.remove_button = ttk.Button(self.master, text="Remove Selected Task", command=self.remove_task)
        self.remove_button.pack()

        self.clear_button = ttk.Button(self.master, text="Clear All Tasks", command=self.clear_tasks)
        self.clear_button.pack(pady=10)

        self.populate_tasks()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task_with_time = f"{task} (Added: {timestamp})"
            self.tasks.append(task_with_time)
            self.add_task_to_frame(task_with_time)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def add_task_to_frame(self, task):
        color = self.get_next_color()
        task_frame = tk.Frame(self.inner_frame, bg=color, pady=5, padx=5)
        task_frame.pack(fill=tk.X, padx=5, pady=2)
        
        task_number = len(self.inner_frame.winfo_children())
        task_label = tk.Label(task_frame, text=f"{task_number}. {task}", bg=color, wraplength=400, justify=tk.LEFT)
        task_label.pack(anchor='w')
        
        task_frame.bind("<Button-1>", lambda e, tf=task_frame: self.select_task(tf))
        task_label.bind("<Button-1>", lambda e, tf=task_frame: self.select_task(tf))

    def get_next_color(self):
        available_colors = [c for c in self.colors if c != self.last_color]
        color = random.choice(available_colors)
        self.last_color = color
        return color

    def select_task(self, task_frame):
        for child in self.inner_frame.winfo_children():
            child.configure(relief=tk.FLAT)
        task_frame.configure(relief=tk.RAISED)

    def remove_task(self):
        for index, task_frame in enumerate(self.inner_frame.winfo_children()):
            if task_frame.cget('relief') == tk.RAISED:
                self.tasks.pop(index)
                task_frame.destroy()
                self.save_tasks()
                self.renumber_tasks()
                return
        messagebox.showwarning("Warning", "Please select a task to remove.")

    def clear_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            for widget in self.inner_frame.winfo_children():
                widget.destroy()
            self.tasks.clear()
            self.save_tasks()

    def populate_tasks(self):
        for task in self.tasks:
            self.add_task_to_frame(task)

    def renumber_tasks(self):
        for index, task_frame in enumerate(self.inner_frame.winfo_children(), start=1):
            task_label = task_frame.winfo_children()[0]
            old_text = task_label.cget("text")
            new_text = f"{index}. {old_text.split('. ', 1)[1]}"
            task_label.configure(text=new_text)

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
    