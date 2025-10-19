# cli/auth.py

import click
import os
from models.user import User

SESSION_FILE = '.session_user_id'

# ----------------- SESSION HELPERS -----------------
def get_current_user():
    """Load logged-in user from session file."""
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE, 'r') as f:
            user_id = int(f.read().strip())
            return User.get_by_id(user_id)
    except:
        return None


def require_login(f):
    """Decorator to require authentication."""
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        user = get_current_user()
        if not user:
            click.echo(" Error: You must be logged in to run this command.", err=True)
            ctx.exit(1)
        ctx.obj = ctx.obj or {}
        ctx.obj['user'] = user
        return f(ctx, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


# ----------------- COMMANDS -----------------
@click.group(name='auth')
def auth_group():
    """User authentication commands."""
    pass


@auth_group.command()
@click.argument('username')
@click.password_option()
def login(username, password):
    """Log in with your credentials."""
    user = User.login(username, password)
    if not user:
        click.echo(" Invalid username or password.", err=True)
        return
    
    try:
        with open(SESSION_FILE, 'w') as f:
            f.write(str(user.id))
        click.echo(f"👋 Welcome back, {user.username}!")
    except Exception as e:
        click.echo(f"⚠️ Login successful but session save failed: {e}", err=True)


@auth_group.command()
@click.argument('username')
@click.password_option()
def register(username, password):
    """Register a new user account."""
    if User.create(username, password):
        click.echo(f" User '{username}' registered successfully!")
        click.echo("You can now login with: python main.py auth login <username>")
    else:
        click.echo(f" Username '{username}' already exists.", err=True)


@auth_group.command()
def logout():
    """Log out current user."""
    user = get_current_user()
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        name = user.username if user else "User"
        click.echo(f"🚪 {name} logged out.")
    else:
        click.echo("ℹ  Not logged in.")


@auth_group.command()
def whoami():
    """Show current user."""
    user = get_current_user()
    if user:
        click.echo(f"👤 {user.username}")
    else:
        click.echo("ℹ Not logged in.")