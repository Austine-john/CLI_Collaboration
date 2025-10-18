# CLI Collaboration Tool

A command-line interface (CLI) application for collaborative project and task management. Built with Python and Click, this tool allows teams to manage projects, create tasks, assign work, and track progress—all from the terminal.

## Features

✨ **User Authentication**
- Secure user registration and login
- Session persistence across commands
- User profile management

📁 **Project Management**
- Create and organize projects
- List all projects or filter by owner
- View detailed project information
- Delete projects you own

📝 **Task Management**
- Create tasks within projects
- Assign tasks to team members
- Update task status (pending, in-progress, completed)
- View tasks by project or assigned user
- Delete tasks

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CLI_Collaboration
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Linux/Mac:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install click
   ```

5. **Initialize the database**
   ```bash
   python main.py --help
   ```
   This will automatically create the SQLite database on first run.

## Usage

### Authentication Commands

**Register a new user**
```bash
python main.py auth register <username>
```

**Login**
```bash
python main.py auth login <username>
```

**Check current user**
```bash
python main.py auth whoami
```

**Logout**
```bash
python main.py auth logout
```

### Project Commands

**Create a project**
```bash
python main.py project create "Project Name"
```

**List your projects**
```bash
python main.py project list
```

**List all projects in the system**
```bash
python main.py project all
```

**View project details**
```bash
python main.py project view <project_id>
```

**Delete a project**
```bash
python main.py project delete <project_id>
```

### Task Commands

**Create a task**
```bash
python main.py task create <project_id> "Task title"
```

**Create and assign a task**
```bash
python main.py task create <project_id> "Task title" --assign <user_id>
```

**List tasks in a project**
```bash
python main.py task list <project_id>
```

**View your assigned tasks**
```bash
python main.py task mytasks
```

**List all tasks**
```bash
python main.py task all
```

**Assign a task to a user**
```bash
python main.py task assign <task_id> <user_id>
```

**Update task status**
```bash
python main.py task status <task_id> <status>
```
Status options: `pending`, `in-progress`, `completed`

**Delete a task**
```bash
python main.py task delete <task_id>
```

## Example Workflow

```bash
# 1. Register and login
python main.py auth register alice
python main.py auth login alice

# 2. Create a project
python main.py project create "Website Redesign"
# Output: Project ID: 1

# 3. Create tasks
python main.py task create 1 "Design homepage mockup"
python main.py task create 1 "Implement navigation" --assign 1
python main.py task create 1 "Setup database schema"

# 4. View tasks
python main.py task list 1
python main.py task mytasks

# 5. Update task progress
python main.py task status 1 in-progress
python main.py task status 1 completed

# 6. View project details
python main.py project view 1

# 7. Logout when done
python main.py auth logout
```

## Project Structure

```
CLI_Collaboration/
├── main.py                 # Application entry point
├── db.py                   # Database connection and initialization
├── collaboration.db        # SQLite database (auto-generated)
├── cli/
│   ├── auth.py            # Authentication commands
│   ├── project.py         # Project management commands
│   └── task.py            # Task management commands
├── models/
│   ├── user.py            # User model
│   ├── project.py         # Project model
│   └── task.py            # Task model
├── venv/                  # Virtual environment (not in repo)
└── README.md              # This file
```

## Database Schema

### Users Table
- `id` (INTEGER, PRIMARY KEY)
- `username` (TEXT, UNIQUE, NOT NULL)
- `password` (TEXT, NOT NULL)

### Projects Table
- `id` (INTEGER, PRIMARY KEY)
- `name` (TEXT, NOT NULL)
- `owner_id` (INTEGER, FOREIGN KEY → users.id)

### Tasks Table
- `id` (INTEGER, PRIMARY KEY)
- `title` (TEXT, NOT NULL)
- `project_id` (INTEGER, FOREIGN KEY → projects.id)
- `assigned_to` (INTEGER, FOREIGN KEY → users.id)
- `status` (TEXT, DEFAULT 'pending')

## Session Management

The tool uses file-based session management. When you login, a `.session_user_id` file is created in the project root directory containing your user ID. This allows you to stay logged in across multiple command invocations.

**Important:** The session file is created in the current directory, so always run commands from the project root.

## Security Notes

⚠️ **This is a development/learning project and should not be used in production without proper security enhancements:**

- Passwords are stored in plain text (should use hashing like bcrypt)
- No token expiration for sessions
- No rate limiting or brute force protection
- File-based session storage is not secure for production

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is open source and available under the MIT License.

## Author

Built as a CLI collaboration and task management learning project.

## Troubleshooting

**"You must be logged in" error after login**
- Make sure you're running commands from the project root directory
- Check if `.session_user_id` file was created after login
- Try logging out and back in

**Database errors**
- Delete `collaboration.db` and restart the application to recreate tables
- Ensure you have write permissions in the project directory

**Command not found**
- Make sure your virtual environment is activated
- Verify Click is installed: `pip list | grep click`

## Future Enhancements

- [ ] Password hashing and secure authentication
- [ ] Email notifications for task assignments
- [ ] Due dates and reminders for tasks
- [ ] Task comments and activity logs
- [ ] Project collaboration invites
- [ ] Export projects/tasks to CSV or JSON
- [ ] Search and filter functionality
- [ ] Task priority levels
- [ ] User roles and permissions