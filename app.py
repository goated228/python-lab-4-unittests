import json

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():

    tasks = load_tasks()

    if request.method == "POST":

        task = request.form.get("task")

        if task:
            tasks.append({"text":task, "done":False})

            save_tasks(tasks)

        return redirect("/")

    return render_template("index.html", tasks=tasks)

@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    tasks = load_tasks()

    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
        save_tasks(tasks)

    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = load_tasks()

    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)