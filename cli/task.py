# cli/task.py (Simplified)
import click
from models.task import Task
from models.project import Project 
from cli.utils import login_required # Assumed utility import

@click.group(name='task')
def task_group():
    """Commands for managing tasks within projects."""
    pass

# --- ADD COMMAND ---
@task_group.command(name='add')
@click.argument('project_id', type=int)
@click.argument('description')
@click.option('--assignee', 'assignee_id', type=int, default=None, help='ID of the user to assign the task to.')
@login_required
def add_task_command(user, project_id, description, assignee_id):
    """Add a new task to a specific project."""
    
    project = Project.get_by_id(project_id)
    if not project:
        return click.echo(f"Error: Project ID {project_id} not found.", err=True)
        
    try:
        new_task = Task.create(project_id, description, assignee_id)
        click.echo(f"Task ID {new_task.id} added to '{project.name}'. Status: {new_task.status}")
    except Exception as e:
        click.echo(f"An error occurred creating the task: {e}", err=True)

# --- ASSIGN COMMAND ---
@task_group.command(name='assign')
@click.argument('task_id', type=int)
@click.argument('user_id', type=int)
@login_required
def assign_task_command(user, task_id, user_id):
    """Assign a task to a different user."""
    
    Task.assign(task_id, user_id)
    click.echo(f"Task ID {task_id} successfully assigned to User ID {user_id}.")

# --- STATUS COMMAND ---
@task_group.command(name='status')
@click.argument('task_id', type=int)
@click.argument('status', type=click.Choice(['pending', 'in-progress', 'complete', 'blocked']))
@login_required
def update_task_status_command(user, task_id, status):
    """Update the status of a specific task."""
    
    Task.update_status(task_id, status)
    click.echo(f"Task ID {task_id} status updated to '{status}'.")

# --- LIST COMMAND (Simplified) ---
@task_group.command(name='list')
@click.option('--project', 'project_id', type=int, help='Filter tasks by Project ID.')
@login_required
def list_tasks_command(user, project_id):
    """List tasks, optionally filtered by project."""
    
    if project_id:
        tasks = Task.get_by_project(project_id)
        header = f"--- Tasks for Project ID {project_id} ---"
    else:
        # Assuming you want to list all tasks assigned to the user by default
        tasks = Task.get_by_assigned_user(user.id) # Requires Task model update
        header = f"--- Tasks Assigned to You ({user.username}) ---"

    if not tasks:
        click.echo("No tasks found matching the criteria.")
        return

    click.echo(header)
    for t in tasks:
        click.echo(f"[{t.id}] {t.description[:40]}... | Status: {t.status}")
    click.echo("-" * 40)