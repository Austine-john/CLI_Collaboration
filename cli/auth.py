# cli/auth.py (Persistence Update)

import click
import os
from models.user import User

# Path to the file where the user ID will be saved (e.g., in the project root)
SESSION_FILE = '.session_user_id'

@auth_group.command()
@click.argument('username')
@click.password_option()
@click.pass_context
def login(ctx, username, password):
    """Log in with existing credentials."""
    user = User.login(username, password)
    
    if user:
        # --- FIX: Store User ID to file system ---
        with open(SESSION_FILE, 'w') as f:
            f.write(str(user.id))
        
        ctx.obj = {'user': user}
        click.echo(f" Welcome back, {user.username}!")
        click.echo("You are now logged in.")
    else:
        click.echo("Invalid username or password.", err=True)

@auth_group.command()
@click.pass_context
def logout(ctx):
    """Log out the current user."""
    # ... (existing logic) ...
    
    # --- FIX: Delete the session file ---
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        username = ctx.obj['user'].username
        ctx.obj['user'] = None
        click.echo(f"🚪 User {username} logged out.")
    else:
        click.echo("You are not currently logged in.")