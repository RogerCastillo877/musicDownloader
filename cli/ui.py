from rich.console import Console

console = Console()


def info(msg: str):
    console.print(f"[cyan]{msg}[/cyan]")


def success(msg: str):
    console.print(f"[green]{msg}[/green]")


def error(msg: str):
    console.print(f"[red]{msg}[/red]")