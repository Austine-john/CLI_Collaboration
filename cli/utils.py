# cli/utils.py

import click

def login_required(f):
    """Decorator to ensure a user is logged in before running a command."""
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        # Retrieve the 'user' object from the top-level Click context (ctx.obj)
        user = ctx.obj.get('user') if ctx.obj else None
        
        if not user:
            click.echo("Error: You must be logged in to run this command.", err=True)
            ctx.exit()
            
        # Inject the user object into the command function as the first argument
        return f(user, *args, **kwargs)
        
    return click.wrap_callback(wrapper, f)

def get_current_user():
    """Retrieves the current logged-in user from the Click context."""
    ctx = click.get_current_context()
    return ctx.obj.get('user') if ctx.obj and ctx.obj else None