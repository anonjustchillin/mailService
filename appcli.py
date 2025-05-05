import typer
from rich.console import Console
from rich.table import Table
from models.message_model import Message
from models.problem_model import Problem
from models.user_model import User
from dbs import message_db, problem_db, user_db
from dbs.db import *

console = Console()
app = typer.Typer()

current_user = User(2, None, None)


@app.command(short_help='інформація про автора')
def about():
    typer.echo("Курсова робота з баз даних Топки Тіни, ІС-32.")


@app.command(short_help='вивід усіх учасників (users) / проблем (problems) / повідомлень (messages)')
def show(what: str):
    if what is not None:
        if what == 'users':
            show_users()
        elif what == 'problems':
            show_problems()
        elif what == 'messages':
            show_messages()
    else:
        typer.echo('Введіть users, problems або messages після команди show.')


# User

@app.command(short_help='додавання учасника')
def add_user():
    name = typer.prompt("Прізвище та ім'я")
    role = typer.prompt("Роль")
    user = User(0, name, role)
    insert_user(user)
    typer.echo(f"Додано учасника: {name} | {role}")
    show_users()


@app.command(short_help='видалення учасника')
def delete_user(id: int):
    delete_user_db(id)
    typer.echo(f"Видалено учасника {id}")
    show_users()


@app.command(short_help='оновлення даних про учасника')
def update_user(my_id: int):
    name = typer.prompt("Прізвище Ім'я")
    role = typer.prompt("Роль")
    if name is not None or role is not None:
        update_user(my_id, name, role)
        typer.echo(f"Оновлено дані про учасника\n{my_id}")
        show_users()
    else:
        typer.echo('Не коректно введено дані')


def show_users():
    users = get_all_users()
    console.print("[bold magenta]Учасники[/bold magenta]")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Id", width=5, style="dim")
    table.add_column("Ім'я", min_width=20)
    table.add_column("Роль", min_width=12)

    def get_user_color(role):
        COLORS = {'Користувач': 'yellow',
                  'Програміст': 'cyan',
                  'Тестувальник': 'green',
                  'Директор': 'red'}
        if role in COLORS:
            return COLORS[role]
        return 'white'

    for i, user in enumerate(users, start=1):
        color = get_user_color(user.role)
        table.add_row(str(i), user.name, f'[{color}]{user.role}[/{color}]')
    console.print(table)


# Problem

@app.command(short_help='додавання зауваження')
def add_problem(title: str, progress: str = None):
    typer.echo(f"Додано зауваження: {title} | {progress}")


@app.command(short_help='видалення зауваження')
def delete_problem(title: str):
    typer.echo(f"Видалено зауваження: {title}")


@app.command(short_help='оновлення даних про зауваження')
def update_problem(old_title: str, old_progress: str, title: str = None, progress: str = None):
    
    if title is not None and progress is not None:
        typer.echo(f"Оновлено дані про зауваження\n{old_title} | {old_progress} ---> {title} | {progress}")
    elif title is not None:
        typer.echo(f"Оновлено дані про зауваження\n{old_title} | {old_progress} ---> {title} | {old_progress}")
    elif progress is not None:
        typer.echo(f"Оновлено дані про зауваження\n{old_title} | {old_progress} ---> {old_title} | {progress}")


def show_problems():
    problems = get_all_problems()
    console.print("[bold magenta]Проблеми[/bold magenta]")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Id", width=5, style="dim")
    table.add_column("Назва", min_width=15)
    table.add_column("Статус", min_width=12)

    for i, prob in enumerate(problems, start=1):
        table.add_row(str(i), prob.title, prob.progress)
    console.print(table)


# Message

@app.command(short_help='надсилання повідомлення')
def send():
    mssg_date = datetime.datetime.now()
    sender = current_user.id
    receiver = int(typer.prompt("Кому"))
    mssg_type = typer.prompt("Тип (Проблема чи Побажання)")
    problem = int(typer.prompt("Номер проблеми"))
    descript = typer.prompt("Опис")

    message = Message(0, descript, mssg_type, mssg_date, sender, receiver, problem)
    send_message(message)

    typer.echo(
        f"Надіслано повідомлення {mssg_date} \nКому: {receiver} | Від: {sender}\n{mssg_type} | {problem}\n{descript}"
    )


@app.command()
def show_messages():
    messages = get_all_messages(current_user.id)
    console.print("[bold magenta]Повідомлення[/bold magenta]")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Id", width=5, style="dim")
    table.add_column("Дата", min_width=12)
    table.add_column("Від", min_width=12)
    table.add_column("До", min_width=12)
    table.add_column("Тип", min_width=12)
    table.add_column("Проблема", min_width=12)
    table.add_column("Опис", min_width=15)

    for i, mes in enumerate(messages, start=1):
        table.add_row(str(i),
                      mes.mssg_date.isoformat(),
                      str(mes.sender),
                      str(mes.receiver),
                      mes.mssg_type,
                      str(mes.problem),
                      mes.descript)
    console.print(table)


@app.command()
def login():
    console.print(f'[bold magenta]Вхід[/bold magenta]\nВведіть свій Id в системі')
    current_id = int(typer.prompt('Id: '))
    row = find_user(current_id)
    if row is not None:
        current_name = " ".join(row[1].split())
        current_role = " ".join(row[2].split())
        global current_user
        current_user = User(row[0], current_name, current_role)
        console.print(f'Добрий день, [bold magenta]{current_user.name}[/bold magenta]!')
    else:
        typer.echo('Не знайдено такого учасника')


def main():
    console.print(f'[bold magenta]Вхід[/bold magenta]!\nВведіть свій Id в системі')
    current_id = int(typer.prompt('Id: '))
    login(current_id)


if __name__ == '__main__':
    app()
