# cli/task.py

import click
from cli.auth import require_login
from models.task import Task
from models.project import Project
from models.user import User

@click.group(name='task')
def task_group():
    """Task management commands."""
    pass


@task_group.command()
@click.argument('project_id', type=int)
@click.argument('title')
@click.option('--assign', '-a', type=int, help='User ID to assign task to')
@require_login
def create(ctx, project_id, title, assign):
    """Create a new task in a project."""
    # Check if project exists
    project = Project.get_by_id(project_id)
    if not project:
        click.echo(f" Project {project_id} not found.", err=True)
        return
    
    # Create the task
    task = Task.create(project_id, title, assign)
    if task:
        click.echo(f"✅ Task created successfully!")
        click.echo(f"📝 Task ID: {task.id}")
        click.echo(f"📁 Project: {project.name}")
        if assign:
            click.echo(f"👤 Assigned to User ID: {assign}")
    else:
        click.echo(" Failed to create task.", err=True)


@task_group.command()
@click.argument('project_id', type=int)
@require_login
def list(ctx, project_id):
    """List all tasks in a project."""
    project = Project.get_by_id(project_id)
    if not project:
        click.echo(f" Project {project_id} not found.", err=True)
        return
    
    tasks = Task.get_by_project(project_id)
    if tasks:
        click.echo(f" Tasks in '{project.name}' ({len(tasks)}):")
        for t in tasks:
            status_icon = "✅" if t.status == "completed" else "⏳"
            assigned = f"→ User {t.assigned_to}" if t.assigned_to else "→ Unassigned"
            click.echo(f"  {status_icon} [{t.id}] {t.title} {assigned}")
    else:
        click.echo(f"ℹ  No tasks in '{project.name}' yet.")


@task_group.command()
@require_login
def mytasks(ctx):
    """List all tasks assigned to you."""
    user = ctx.obj['user']
    tasks = Task.get_by_user(user.id)
    
    if tasks:
        click.echo(f" Your tasks ({len(tasks)}):")
        for t in tasks:
            status_icon = "✅" if t.status == "completed" else "⏳"
            project = Project.get_by_id(t.project_id)
            project_name = project.name if project else "Unknown"
            click.echo(f"  {status_icon} [{t.id}] {t.title}")
            click.echo(f"      📁 Project: {project_name} (ID: {t.project_id})")
    else:
        click.echo("ℹ  You have no assigned tasks.")


@task_group.command()
@require_login
def all(ctx):
    """List all tasks in the system."""
    tasks = Task.get_all()
    
    if tasks:
        click.echo(f" All tasks ({len(tasks)}):")
        for t in tasks:
            status_icon = "✅" if t.status == "completed" else "⏳"
            assigned = f"User {t.assigned_to}" if t.assigned_to else "Unassigned"
            click.echo(f"  {status_icon} [{t.id}] {t.title} (Project: {t.project_id}, {assigned})")
    else:
        click.echo(" No tasks in the system yet.")


@task_group.command()
@click.argument('task_id', type=int)
@click.argument('user_id', type=int)
@require_login
def assign(ctx, task_id, user_id):
    """Assign a task to a user."""
    # Check if task exists
    task = Task.get_by_id(task_id)
    if not task:
        click.echo(f" Task {task_id} not found.", err=True)
        return
    
    # Check if user exists
    user = User.get_by_id(user_id)
    if not user:
        click.echo(f" User {user_id} not found.", err=True)
        return
    
    if Task.assign(task_id, user_id):
        click.echo(f" Task {task_id} assigned to {user.username}!")
    else:
        click.echo(" Failed to assign task.", err=True)


@task_group.command()
@click.argument('task_id', type=int)
@click.argument('status', type=click.Choice(['pending', 'in-progress', 'completed']))
@require_login
def status(ctx, task_id, status):
    """Update task status."""
    task = Task.get_by_id(task_id)
    if not task:
        click.echo(f"❌ Task {task_id} not found.", err=True)
        return
    
    if Task.update_status(task_id, status):
        click.echo(f"✅ Task {task_id} status updated to '{status}'!")
    else:
        click.echo("❌ Failed to update status.", err=True)


@task_group.command()
@click.argument('task_id', type=int)
@click.confirmation_option(prompt='Are you sure you want to delete this task?')
@require_login
def delete(ctx, task_id):
    """Delete a task."""
    if Task.delete(task_id):
        click.echo(f" Task {task_id} deleted successfully!")
    else:
        click.echo(f" Task {task_id} not found.", err=True)