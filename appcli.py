import typer
from rich.console import Console
from models.message_model import Message
from models.problem_model import Problem
from models.user_model import User
from dbs import message_db, problem_db, user_db

console = Console()
app = typer.Typer()


@app.command(short_help='інформація про автора')
def about():
    typer.echo("Курсова робота з баз даних Топки Тіни, ІС-32.")


# User

@app.command(short_help='додавання учасника')
def add_user(name: str = None, role: str = None):
    typer.echo(f"Додано учасника: {name} | {role}")


@app.command(short_help='видалення учасника')
def delete_user(name: str = None, role: str = None):
    typer.echo(f"Видалено учасника: {name} | {role}")


@app.command(short_help='оновлення даних про учасника')
def update_user(old_name: str, old_role: str, name: str = None, role: str = None):
    if name is not None and role is not None:
        typer.echo(f"Оновлено дані про учасника\n{old_name} | {old_role} ---> {name} | {role}")
    elif name is not None:
        typer.echo(f"Оновлено дані про учасника\n{old_name} | {old_role} ---> {name} | {old_role}")
    elif role is not None:
        typer.echo(f"Оновлено дані про учасника\n{old_name} | {old_role} ---> {old_name} | {role}")
    else:
        typer.echo('Не коректно введено дані')


# Problem

@app.command(short_help='додавання зауваження')
def add_problem(title: str, progress: str = None):
    typer.echo(f"Додано зауваження: {title} | {progress}")


@app.command(short_help='видалення зауваження')
def delete_problem(title: str, progress: str = None):
    typer.echo(f"Видалено зауваження: {title} | {progress}")


@app.command(short_help='оновлення даних про зауваження')
def update_problem(old_title: str, old_progress: str, title: str = None, progress: str = None):
    if title is not None and progress is not None:
        typer.echo(f"Оновлено дані про зауваження\n{old_title} | {old_progress} ---> {title} | {progress}")
    elif title is not None:
        typer.echo(f"Оновлено дані про зауваження\n{old_title} | {old_progress} ---> {title} | {old_progress}")
    elif progress is not None:
        typer.echo(f"Оновлено дані про зауваження\n{old_title} | {old_progress} ---> {old_title} | {progress}")


# Message

@app.command(short_help='надсилання повідомлення')
def send(mssg_date,
             sender: str,
             receiver: str,
             descript: str = None,
             mssg_type: str = None,
             problem: str = None):
    mssg_date = mssg_date.isoformat()
    typer.echo(
        f"Надіслано повідомлення {mssg_date} \nКому: {receiver} | Від: {sender}\n{mssg_type} | {problem}\n{descript}"
    )


if __name__ == '__main__':
    app()
