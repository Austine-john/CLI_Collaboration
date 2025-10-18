
import click
from models.project import Project
from cli.utils import login_required # Assumed utility import

@click.group(name='project')
def project_group():
    """Commands for managing your collaboration projects."""
    pass

# --- CREATE COMMAND ---
@project_group.command(name='create')
@click.argument('name')
@login_required 
def create_project_command(user, name):
    """Create a new project."""
    
    try:
        # User is automatically passed by the decorator
        Project.create(name, user.id) 
        click.echo(f"Project '{name}' created successfully (Owner: {user.username}).")
    except Exception as e:
        click.echo(f" Error creating project: {e}", err=True)

# --- LIST COMMAND ---
@project_group.command(name='list')
@login_required
def list_projects_command(user):
    """List all projects you own."""
    
    projects = Project.get_by_user(user.id)
    
    if not projects:
        click.echo("You have no projects yet.")
        return

    click.echo("\n--- Your Projects ---")
    for p in projects:
        # List only the core details
        click.echo(f"[{p.id}] {p.name}")
    click.echo("-" * 20)

# --- DELETE COMMAND ---
@project_group.command(name='delete')
@click.argument('project_id', type=int)
@login_required
def delete_project_command(user, project_id):
    """Delete a project by its ID."""
    
    # For robust deletion, we rely on the Project model's logic.
    Project.delete(project_id) 
    
    click.echo(f"Attempted deletion of Project ID {project_id}.")