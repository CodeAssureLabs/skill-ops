from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

app = typer.Typer(
    name="skill-ops",
    help="Agentic DevOps framework for managing AI agent skills",
    add_completion=False,
)
console = Console()


class LinkStrategy(str, Enum):
    SYMLINK = "symlink"
    JUNCTION = "junction"
    COPY = "copy"


@app.command()
def init(
    path: Path = typer.Option(
        Path(".agent"), help="Path to create the .agent directory"
    ),
):
    """
    Initialize a new Skill-Ops manifest in the current repository.
    """
    from .core import init_manifest

    try:
        manifest_path = init_manifest(path)
        console.print(
            f"[green]Successfully initialized Skill-Ops manifest at {manifest_path}[/green]"
        )
    except Exception as e:
        console.print(f"[red]Error initializing Skill-Ops: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def hydrate(
    force: bool = typer.Option(
        False, "--force", "-f", help="Force hydration even if symlinks exist"
    ),
    strategy: Optional[LinkStrategy] = typer.Option(
        None, "--link-strategy", "-s", help="Override the default linking strategy"
    ),
):
    """
    Read the Skill-Ops manifest and create symlinks for skills.
    """
    from .core import hydrate_skills

    try:
        stats = hydrate_skills(
            force=force, strategy=strategy.value if strategy else None
        )
        console.print("[green]Successfully hydrated skills![/green]")
        for ns, count in stats.items():
            console.print(f"  - {ns}: {count} skills linked")
    except Exception as e:
        console.print(f"[red]Error hydrating skills: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def list():
    """
    List all available skills categorized by namespace.
    """
    from .core import list_skills

    try:
        skills = list_skills()
        if not skills:
            console.print("[yellow]No skills found.[/yellow]")
            return

        for ns, items in skills.items():
            console.print(f"[bold blue]{ns}[/bold blue]")
            for item in items:
                console.print(f"  - {item}")
    except Exception as e:
        console.print(f"[red]Error listing skills: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def validate():
    """
    Check for broken symlinks or missing sources in hydrated namespaces.
    """
    from .core import validate_hydration

    try:
        issues = validate_hydration()
        if not issues:
            console.print("[green]All symlinks are valid![/green]")
        else:
            console.print("[yellow]Found hydration issues:[/yellow]")
            for issue in issues:
                console.print(f"  - {issue}")
            raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]Error validating hydration: {e}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
