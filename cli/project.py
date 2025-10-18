# cli/project.py

import click
from cli.auth import require_login
from models.project import Project

@click.group(name='project')
def project_group():
    """Project management commands."""
    pass


@project_group.command()
@click.argument('name')
@require_login
def create(ctx, name):
    """Create a new project."""
    user = ctx.obj['user']
    project = Project.create(name=name, owner_id=user.id)
    
    if project:
        click.echo(f"✅ Project '{name}' created successfully!")
        click.echo(f"📁 Project ID: {project.id}")
    else:
        click.echo("❌ Failed to create project.", err=True)


@project_group.command()
@require_login
def list(ctx):
    """List all your projects."""
    user = ctx.obj['user']
    projects = Project.get_by_user(user.id)
    
    if projects:
        click.echo(f"📋 Your projects ({len(projects)}):")
        for p in projects:
            click.echo(f"  • [{p.id}] {p.name}")
    else:
        click.echo("ℹ️  You don't have any projects yet.")
        click.echo("💡 Create one with: python main.py project create <name>")


@project_group.command()
@require_login
def all(ctx):
    """List all projects in the system."""
    projects = Project.get_all()
    
    if projects:
        click.echo(f"📋 All projects ({len(projects)}):")
        for p in projects:
            click.echo(f"  • [{p.id}] {p.name} (Owner ID: {p.owner_id})")
    else:
        click.echo("ℹ️  No projects in the system yet.")


@project_group.command()
@click.argument('project_id', type=int)
@require_login
def view(ctx, project_id):
    """View details of a specific project."""
    project = Project.get_by_id(project_id)
    
    if not project:
        click.echo(f" Project with ID {project_id} not found.", err=True)
        return
    
    user = ctx.obj['user']
    is_owner = project.owner_id == user.id
    
    click.echo(f"📁 Project Details:")
    click.echo(f"   ID: {project.id}")
    click.echo(f"   Name: {project.name}")
    click.echo(f"   Owner ID: {project.owner_id}")
    click.echo(f"   You are {'the owner' if is_owner else 'not the owner'}")


@project_group.command()
@click.argument('project_id', type=int)
@click.confirmation_option(prompt='Are you sure you want to delete this project?')
@require_login
def delete(ctx, project_id):
    """Delete a project (you must own it)."""
    user = ctx.obj['user']
    
    if Project.delete(project_id, user.id):
        click.echo(f"Project {project_id} deleted successfully!")
    else:
        click.echo(f"Failed to delete project. Make sure it exists and you own it.", err=True)