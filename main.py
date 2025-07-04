import re
import sys
import datetime
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt


USERS_FILE = "Data-storage/users.csv"
PROJECTS_FILE = "Data-storage/projects.csv"
console = Console()


# Utility Functions
def clear_screen():
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def load_users():
    """Load users from the users file."""
    users = []
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                users.append(line.strip().split(","))
    except FileNotFoundError:
        pass
    return users


def save_users(users):
    """Save users to the users file."""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        for user in users:
            f.write(",".join(user) + "\n")


def load_projects():
    """Load projects from the projects file."""
    projects = []
    try:
        with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                projects.append(line.strip().split(","))
    except FileNotFoundError:
        pass
    return projects


def save_projects(projects):
    """Save projects to the projects file."""
    with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
        for project in projects:
            f.write(",".join(project) + "\n")


def validate_egyptian_phone(phone):
    """Validate Egyptian mobile phone number format."""
    return re.fullmatch(r"01[0125][0-9]{8}", phone) is not None


def validate_email(email):
    """Validate email format."""
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None


def validate_date(date_text):
    """Validate date format (YYYY-MM-DD)."""
    try:
        return datetime.datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        return None


def input_nonempty(prompt):
    """Prompt for input until a non-empty value is received."""
    while True:
        value = Prompt.ask(prompt).strip()
        if value:
            return value


# Authentication
def register():
    """Register a new user."""
    clear_screen()
    console.print(Panel("[bold magenta]Registration[/bold magenta]"))
    first = input_nonempty("First Name")
    last = input_nonempty("Last Name")
    while True:
        email = Prompt.ask("Email").strip()
        if not validate_email(email):
            console.print("[red]Invalid email format.[/red]")
            continue
        if any(u[2] == email for u in load_users()):
            console.print("[red]Email already registered.[/red]")
            continue
        break
    while True:
        password = Prompt.ask("Password", password=True).strip()
        confirm = Prompt.ask("Confirm Password", password=True).strip()
        if password != confirm:
            console.print("[red]Passwords do not match.[/red]")
            continue
        if len(password) < 6:
            console.print("[red]Password must be at least 6 characters.[/red]")
            continue
        break
    while True:
        phone = Prompt.ask("Mobile Phone (Egyptian)").strip()
        if validate_egyptian_phone(phone):
            break
        console.print("[red]Invalid Egyptian phone number.[/red]")
    users = load_users()
    users.append([first, last, email, password, phone, "inactive"])
    save_users(users)
    console.print("[green]Registration successful. Please activate your account (simulated activation).[/green]")
    # Simulate activation
    for user in users:
        if user[2] == email:
            user[5] = "active"
    save_users(users)
    console.print("[green]Account activated. You can now login.[/green]")


def login():
    """Login an existing user."""
    clear_screen()
    console.print(Panel("[bold magenta]Login[/bold magenta]"))
    email = Prompt.ask("Email").strip()
    password = Prompt.ask("Password", password=True).strip()
    users = load_users()
    for user in users:
        if user[2] == email and user[3] == password and user[5] == "active":
            console.print(f"[green]Welcome, {user[0]} {user[1]}![/green]")
            return user
    console.print("[red]Invalid credentials or inactive account.[/red]")
    return None


# Project Management
def create_project(user):
    """Create a new project."""
    clear_screen()
    console.print(Panel("[bold blue]Create Project[/bold blue]"))
    title = input_nonempty("Title")
    details = input_nonempty("Details")
    while True:
        target = Prompt.ask("Total Target (EGP)").strip()
        if target.isdigit() and int(target) > 0:
            break
        console.print("[red]Invalid target amount.[/red]")
    while True:
        start = Prompt.ask("Start Date (YYYY-MM-DD)").strip()
        start_dt = validate_date(start)
        if start_dt:
            break
        console.print("[red]Invalid date format.[/red]")
    while True:
        end = Prompt.ask("End Date (YYYY-MM-DD)").strip()
        end_dt = validate_date(end)
        if end_dt and end_dt > start_dt:
            break
        console.print("[red]End date must be after start date and valid format.[/red]")
    projects = load_projects()
    project_id = str(len(projects) + 1)
    projects.append([project_id, user[2], title, details, target, start, end])
    save_projects(projects)
    console.print("[green]Project created successfully.[/green]")


def show_projects(projects, title="All Projects"):
    """Display a table of projects."""
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return
    users = load_users()
    email_to_name = {u[2]: f"{u[0]} {u[1]}" for u in users}
    table = Table(title=title)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Owner", style="magenta")
    table.add_column("Title", style="green")
    table.add_column("Target (EGP)", justify="right", style="yellow")
    table.add_column("Start", style="white")
    table.add_column("End", style="white")
    table.add_column("Details", style="dim")
    for p in projects:
        owner_name = email_to_name.get(p[1], p[1])
        table.add_row(p[0], owner_name, p[2], p[4], p[5], p[6], p[3])
    console.print(table)


def view_projects(user=None):
    """View all projects or user's projects."""
    clear_screen()
    projects = load_projects()
    if user:
        projects = [p for p in projects if p[1] == user[2]]
        show_projects(projects, title="Your Projects")
    else:
        show_projects(projects)


def edit_project(user):
    """Edit an existing project."""
    clear_screen()
    projects = load_projects()
    user_projects = [p for p in projects if p[1] == user[2]]
    if not user_projects:
        console.print("[yellow]You have no projects to edit.[/yellow]")
        return
    show_projects(user_projects, title="Your Projects")
    pid = Prompt.ask("Enter Project ID to edit").strip()
    for p in projects:
        if p[0] == pid and p[1] == user[2]:
            console.print("[dim]Leave blank to keep current value.[/dim]")
            title = Prompt.ask(f"Title [{p[2]}]").strip() or p[2]
            details = Prompt.ask(f"Details [{p[3]}]").strip() or p[3]
            while True:
                target = Prompt.ask(f"Target [{p[4]}]").strip()
                if not target:
                    target = p[4]
                    break
                if target.isdigit() and int(target) > 0:
                    break
                console.print("[red]Invalid target amount.[/red]")
            while True:
                start = Prompt.ask(f"Start Date [{p[5]}]").strip()
                if not start:
                    start = p[5]
                    start_dt = validate_date(start)
                    break
                start_dt = validate_date(start)
                if start_dt:
                    break
                console.print("[red]Invalid date format.[/red]")
            while True:
                end = Prompt.ask(f"End Date [{p[6]}]").strip()
                if not end:
                    end = p[6]
                    end_dt = validate_date(end)
                    break
                end_dt = validate_date(end)
                if end_dt and end_dt > start_dt:
                    break
                console.print("[red]End date must be after start date and valid format.[/red]")
            p[2], p[3], p[4], p[5], p[6] = title, details, target, start, end
            save_projects(projects)
            console.print("[green]Project updated.[/green]")
            return
    console.print("[red]Project not found or not owned by you.[/red]")


def delete_project(user):
    """Delete an existing project."""
    clear_screen()
    projects = load_projects()
    user_projects = [p for p in projects if p[1] == user[2]]
    if not user_projects:
        console.print("[yellow]You have no projects to delete.[/yellow]")
        return
    show_projects(user_projects, title="Your Projects")
    pid = Prompt.ask("Enter Project ID to delete").strip()
    for i, p in enumerate(projects):
        if p[0] == pid and p[1] == user[2]:
            projects.pop(i)
            save_projects(projects)
            console.print("[green]Project deleted.[/green]")
            return
    console.print("[red]Project not found or not owned by you.[/red]")


def search_projects_by_date():
    """Search projects by date."""
    clear_screen()
    console.print(Panel("[bold blue]Search Projects by Date[/bold blue]"))
    date_str = Prompt.ask("Enter date (YYYY-MM-DD)").strip()
    date_obj = validate_date(date_str)
    if not date_obj:
        console.print("[red]Invalid date format.[/red]")
        return
    projects = load_projects()
    found = []
    for p in projects:
        start = validate_date(p[5])
        end = validate_date(p[6])
        if start and end and start <= date_obj <= end:
            found.append(p)
    show_projects(found, title=f"Projects Active on {date_str}")


# Main Application Loop
def main():
    """Main application loop."""
    while True:
        clear_screen()
        console.print(Panel("[bold blue]Crowdfunding Console App[/bold blue]", expand=False))
        console.print("1. Register\n2. Login\n3. Exit", style="cyan")
        choice = Prompt.ask("Choose an option").strip()
        if choice == "1":
            register()
            Prompt.ask("\nPress Enter to continue...")
        elif choice == "2":
            user = login()
            if user:
                while True:
                    console.print("\n[bold green]Project Menu[/bold green]")
                    console.print("1. Create Project\n2. View All Projects\n3. View Your Projects\n4. Edit Your Project\n5. Delete Your Project\n6. Search Projects by Date\n7. Logout", style="cyan")
                    p_choice = Prompt.ask("Choose an option").strip()
                    if p_choice == "1":
                        create_project(user)
                        Prompt.ask("\nPress Enter to continue...")
                    elif p_choice == "2":
                        view_projects()
                        Prompt.ask("\nPress Enter to continue...")
                    elif p_choice == "3":
                        view_projects(user)
                        Prompt.ask("\nPress Enter to continue...")
                    elif p_choice == "4":
                        edit_project(user)
                        Prompt.ask("\nPress Enter to continue...")
                    elif p_choice == "5":
                        delete_project(user)
                        Prompt.ask("\nPress Enter to continue...")
                    elif p_choice == "6":
                        search_projects_by_date()
                        Prompt.ask("\nPress Enter to continue...")
                    elif p_choice == "7":
                        break
                    else:
                        console.print("[red]Invalid option.[/red]")
                        Prompt.ask("\nPress Enter to continue...")
        elif choice == "3":
            console.print("[bold yellow]Goodbye![/bold yellow]")
            sys.exit()
        else:
            console.print("[red]Invalid option.[/red]")
            Prompt.ask("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
