# cli/utils.py (CORRECTED)

import click

def login_required(f):
    
    # 1. Use @click.pass_context to get the current context (ctx)
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        # Retrieve the 'user' object from the top-level Click context (ctx.obj)
        user = ctx.obj.get('user') if ctx.obj and ctx.obj.get('user') else None
        
        if not user:
            click.echo(" Error: You must be logged in to run this command.", err=True)
            ctx.exit()
            
        # 2. Call the original function (f), passing the user object first, 
        #    followed by any original arguments (*args, **kwargs).
        return ctx.invoke(f, user, *args, **kwargs)
        
    # 3. Use the wrapper function as the actual decorated function
    #    and ensure it carries the metadata of the original function (f).
    #    This is the standard way to return a decorated function in Python.
    return wrapper

def get_current_user():
    """Retrieves the current logged-in user from the Click context."""
    ctx = click.get_current_context()
    return ctx.obj.get('user') if ctx.obj and ctx.obj.get('user') else None