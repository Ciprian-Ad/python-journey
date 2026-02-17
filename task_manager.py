def load_tasks():
    loaded_tasks = []
    try:
        with open("tasks.txt", "r") as f: # "r" for read
            for line in f:
                # .strip() removes the invisible newline character (\n)
                loaded_tasks.append(line.strip())
    except FileNotFoundError:
        # If the file doesn't exist yet, just return an empty list
        pass
    return loaded_tasks
# Initialize an empty list to store tasks
tasks = load_tasks()

def show_menu():
    print("\n--- Task Manager ---")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Exit")

def add_task(task_list):
    new_task = input("Enter the task: ")
    task_list.append(new_task)
    save_single_task(new_task)
    print(f"Task '{new_task}' added and saved!")

def save_all_tasks(task_list):
    with open("tasks.txt", "w") as f:
        for task in task_list:
            f.write(task + "\n")

def save_single_task(task):
    with open("tasks.txt", "a") as f:
        f.write(task + "\n")

def delete_task(task_list):
    #Step 1: Show the numbered list of tasks
    for index, task in enumerate(task_list, start=1):
        print(f"{index}. {task}")
    #step 2: Ask the user which task to delete
    try:
        choice = int(input("Enter the number of the task to delete: "))
        #Step 3: Remove the task from the list
        if 1 <= choice <= len(task_list):
            removed = task_list.pop(choice - 1)
            print(f"Task '{removed}' deleted.")
        else:
            print("Invalid task number.")
        #Step 4: Save the updated list back to the file
        save_all_tasks(task_list)
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid task number.")   

# The main loop
choice = ""
while choice != "3":
    show_menu()
    choice = input("Choose an option (1-3): ")
    
    if choice == "1":
        # logic to view tasks
        if not tasks:
            print("No tasks found")
        else:
            for t in tasks:
                print(f"- {t}")
    elif choice == "2":
        # logic to add a task
        add_task(tasks)
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice, try again.")
save_all_tasks(tasks)