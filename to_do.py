import tkinter as tk
from tkinter import messagebox, ttk
import json

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do App")
        self.master.geometry("400x500")
        self.master.configure(bg='#f0f0f0')

        self.tasks = self.load_tasks()

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.master, text="My To-Do List", font=("Helvetica", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)

        # Task entry
        self.task_entry = ttk.Entry(self.master, width=40, font=("Helvetica", 12))
        self.task_entry.pack(pady=10)

        # Add task button
        self.add_button = ttk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        # Task listbox
        self.task_listbox = tk.Listbox(self.master, width=50, height=15, font=("Helvetica", 12))
        self.task_listbox.pack(pady=10)

        # Populate listbox with saved tasks
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

        # Remove task button
        self.remove_button = ttk.Button(self.master, text="Remove Selected Task", command=self.remove_task)
        self.remove_button.pack()

        # Clear all button
        self.clear_button = ttk.Button(self.master, text="Clear All Tasks", command=self.clear_tasks)
        self.clear_button.pack(pady=10)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def remove_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(task_index)
            self.tasks.pop(task_index)
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def clear_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.task_listbox.delete(0, tk.END)
            self.tasks.clear()
            self.save_tasks()

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
    