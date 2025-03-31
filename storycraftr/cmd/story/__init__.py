import click

@click.group()
def story():
    """Story-related commands for book writing."""
    pass

from .outline import outline
from .worldbuilding import worldbuilding
from .chapters import chapters
from .iterate import iterate

story.add_command(outline)
story.add_command(worldbuilding)
story.add_command(chapters)
story.add_command(iterate)
