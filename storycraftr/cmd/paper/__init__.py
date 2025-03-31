import click

@click.group()
def paper():
    """Paper-related commands for academic writing."""
    pass

from .define import define
from .organize_lit import organize_lit
from .outline_sections import outline
from .analyze import analyze
from .finalize import finalize

paper.add_command(define)
paper.add_command(organize_lit)
paper.add_command(outline)
paper.add_command(analyze)
paper.add_command(finalize)
