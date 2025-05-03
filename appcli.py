import typer
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()


@app.command(short_help='інформація про автора')
def about():
    typer.echo("Курсова робота з баз даних Топки Тіни, ІС-32.")





if __name__ == '__main__':
    app()
