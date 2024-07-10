import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

TODO_FILE = 'todos.json'

def load_todos():
    try:
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error reading the todo file. Starting with an empty list.")
        return []

def save_todos(todos):
    try:
        with open(TODO_FILE, 'w') as file:
            json.dump(todos, file, indent=4)
    except IOError:
        print("Error saving the todo file.")

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.todos = load_todos()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Task:").grid(row=0, column=0, padx=10, pady=10)
        self.task_entry = tk.Entry(self.root, width=50)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Priority (low, medium, high):").grid(row=1, column=0, padx=10, pady=10)
        self.priority_entry = tk.Entry(self.root, width=50)
        self.priority_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
        self.due_date_entry = tk.Entry(self.root, width=50)
        self.due_date_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=3, column=0, padx=10, pady=10)

        self.done_button = tk.Button(self.root, text="Mark as Done", command=self.mark_task_done)
        self.done_button.grid(row=3, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=3, column=2, padx=10, pady=10)

        self.task_listbox = tk.Listbox(self.root, width=100, height=20)
        self.task_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.update_task_list()

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for i, todo in enumerate(self.todos):
            status = "Done" if todo['done'] else "Pending"
            self.task_listbox.insert(tk.END, f"{i + 1}. {todo['task']} | Priority: {todo['priority']} | Due Date: {todo['due_date']} | Status: {status}")

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
            self.todos.append({'task': task, 'priority': priority, 'due_date': due_date, 'done': False})
            save_todos(self.todos)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Task added!")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Task not added.")

    def mark_task_done(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.todos[selected_task_index]['done'] = True
            save_todos(self.todos)
            self.update_task_list()
            messagebox.showinfo("Success", "Task marked as done!")
        except IndexError:
            messagebox.showerror("Error", "No task selected.")

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.todos.pop(selected_task_index)
            save_todos(self.todos)
            self.update_task_list()
            messagebox.showinfo("Success", "Task deleted!")
        except IndexError:
            messagebox.showerror("Error", "No task selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
