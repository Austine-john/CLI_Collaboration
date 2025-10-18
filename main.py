# main.py
import click
from db import initialize_db

# Import the command groups from your 'cli' directory
from cli.auth import auth_group
from cli.project import project_group
from cli.task import task_group

# --- Main Application Logic ---

@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.pass_context
def cli(ctx):
    """
    A CLI Collaboration and Task Management Tool.
    
    Use 'cli <command> --help' for detailed usage information.
    """
    # 1. Initialize the context object to hold session data (like the logged-in user)
    # This ensures ctx.obj is ready to store the user when 'auth login' is run.
    if ctx.obj is None:
        ctx.obj = {}
        
    # 2. Initialize the database if it doesn't exist
    try:
        initialize_db()
    except Exception as e:
        # A clean exit if the database cannot be initialized
        click.echo(f"FATAL ERROR: Could not initialize database. Details: {e}", err=True)
        ctx.exit(1)


# 3. Add the command groups as sub-commands to the main CLI
cli.add_command(auth_group)
cli.add_command(project_group)
cli.add_command(task_group)


# --- Entry Point ---
if __name__ == '__main__':
    # Run the main Click command line interface
    # Calling with obj={} ensures the context object is initialized for the top-level command
    cli(obj={})