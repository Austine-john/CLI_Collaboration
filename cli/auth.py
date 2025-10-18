# cli/auth.py

import click
from models.user import User
from cli.utils import login_required # Import the necessary utility

# ----------------- MAIN AUTH GROUP -----------------
@click.group(name='auth')
def auth_group():
    """Commands for user authentication and profile management."""
    pass

# ----------------- REGISTER COMMAND -----------------
@auth_group.command()
@click.argument('username')
@click.password_option(confirmation_prompt=True)
def register(username, password):
    """Register a new user account."""
    
    try:
        # User.create should handle password hashing and return the new User object
        new_user = User.create(username, password) 
        
        click.echo(f"User '{new_user.username}' registered successfully.")

    except Exception as e:
        # In a real app, catch IntegrityError specifically for cleaner output
        click.echo(f"Error during registration. Username might already exist.", err=True)


# ----------------- LOGIN COMMAND -----------------
@auth_group.command()
@click.argument('username')
@click.password_option()
@click.pass_context
def login(ctx, username, password):
    """Log in with existing credentials."""
    
    user = User.login(username, password)
    
    if user:
        # Store the user object in the Click context for other commands to use
        ctx.obj = {'user': user}
        click.echo(f"Welcome back, {user.username}!")
        click.echo("You are now logged in.")
    else:
        click.echo("Invalid username or password.", err=True)
        
        
# ----------------- LOGOUT COMMAND -----------------
@auth_group.command()
@click.pass_context
def logout(ctx):
    """Log out the current user."""
    
    # Use the stored user object to confirm logout
    current_user = ctx.obj.get('user') if ctx.obj else None

    if current_user:
        username = current_user.username
        ctx.obj['user'] = None # Clear the session data
        click.echo(f" User {username} logged out.")
    else:
        click.echo("You are not currently logged in.")
        
# ----------------- PROFILE COMMAND -----------------
@auth_group.command(name='profile')
@login_required
def view_profile(user):
    """View your current user profile information."""
    
    click.echo("\n--- Your Profile ---")
    click.echo(f"ID:       {user.id}")
    click.echo(f"Username: {user.username}")
    click.echo("--------------------")
    click.echo("You are currently logged in.")