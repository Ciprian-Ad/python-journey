from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import json
console = Console()

def load_tasks():
    try:
        with open("tasks.json", "r") as f: # "r" for read
            return  json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist yet or is corrupted, just return an empty list
        return []
# Initialize an empty list to store tasks
tasks = load_tasks()

def show_menu():
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Delete Task")
    print("4. View Stats")
    print("5. Exit")

def add_task(task_list):
    name = input("Enter the task name: ")
    try:
        score = int(input("Enter the task score (1-10): "))
        #Create a dictionary for the task
        new_task = {"name":name, "score":score}
        task_list.append(new_task)
        save_all_tasks(task_list)
        console.print(f"[green]Added '{name}' with complexity {score}![/green]")
    except ValueError:
        console.print("[red]Please enter a valid integer for the score![/red]")

def save_all_tasks(task_list):
    with open("tasks.json", "w") as f:
        #indent=4 makes the JSON file more readable by adding indentation
        json.dump(task_list, f, indent=4)

def save_single_task(task):
    with open("tasks.txt", "a") as f:
        f.write(task + "\n")

def view_tasks(task_list):
    if not task_list:
        console.print("[yellow]No tasks found![/yellow]")
        return
        
    table = Table(title="Your To-Do List", style="cyan")
    table.add_column("ID", justify="right", style="magenta")
    table.add_column("Task Description", style="green")

    for index, task in enumerate(task_list, start=1):
        table.add_row(str(index), f"{task['name']} (Complexity: {task['score']})")
    console.print(table)

def delete_task(task_list):
    #Step 1: Show the numbered list of tasks
    for index, task in enumerate(task_list, start=1):
        print(f"{index}. {task['name']} (Complexity: {task['score']})")
    #step 2: Ask the user which task to delete
    try:
        choice = int(input("Enter the number of the task to delete: "))
        #Step 3: Remove the task from the list
        if 1 <= choice <= len(task_list):
            removed = task_list.pop(choice - 1)
            print(f"Task '{removed['name']}' deleted.")
        else:
            print("Invalid task number.")
        #Step 4: Save the updated list back to the file
        save_all_tasks(task_list)
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid task number.")   

def show_stats(task_list):
    if not task_list:
        console.print("[bold red]No tasks to analyze![/bold red]")
        return
    #Use a List Comprehension to grap just the scores
    scores = [t['score'] for t in task_list]
    
    avg_score = sum(scores) / len(scores)
    max_val = max(scores)
    min_val = min(scores)
    # Using Rich's Panel to display stats
    stats_summary = (
        f"📊 [bold]Average Complexity:[/bold] {avg_score:.2f}\n"
        f"🔥 [bold]Highest Priority:[/bold] {max_val}\n"
        f"🧊 [bold]Lowest Priority:[/bold] {min_val}"
    )
    console.print(Panel(stats_summary, title="Task Analytics", style="bold blue"))

# The main loop
choice = ""
while choice != "5":
    show_menu()
    choice = input("Choose an option (1-5): ")
    
    if choice == "1":
        # logic to view tasks
        view_tasks(tasks)
    elif choice == "2":
        # logic to add a task
        add_task(tasks)
    elif choice == "3":
        # logic to delete a task
        delete_task(tasks)
    elif choice == "4":
        # logic to show stats
        show_stats(tasks)
    elif choice == "5":
        print("Goodbye!")
    else:
        print("Invalid choice, try again.")
save_all_tasks(tasks)
