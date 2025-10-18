# cli/utils.py

import click
import os
# CRITICAL: Import the User model to fetch the user object from the DB
from models.user import User 

# Path to the file where the user ID is saved
SESSION_FILE = '.session_user_id'

def login_required(f):
    """
    Decorator to ensure a user is logged in by checking the in-memory context 
    or loading the session from the persistent file.
    """
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        user = ctx.obj.get('user') if ctx.obj and ctx.obj.get('user') else None
        
        # --- FIX: Load session from file if not in context ---
        if not user and os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, 'r') as f:
                    user_id = int(f.read().strip())
                
                # Fetch the full User object from the database using the ID
                user = User.get_by_id(user_id) 
                
                # Restore the user to the current in-memory context for this run
                if user:
                    ctx.obj['user'] = user
                
            except Exception:
                # If file read or DB fetch fails, treat as logged out
                user = None 

        if not user:
            click.echo("❌ Error: You must be logged in to run this command.", err=True)
            ctx.exit()
            
        # Call the decorated function, injecting the 'user' object
        return ctx.invoke(f, user, *args, **kwargs)
        
    return wrapper

def get_current_user():
    """Retrieves the current logged-in user from the Click context."""
    ctx = click.get_current_context()
    return ctx.obj.get('user') if ctx.obj and ctx.obj.get('user') else None