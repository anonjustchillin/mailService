import typer
from rich.console import Console
from rich.table import Table
from models.message_model import Message
from models.problem_model import Problem
from models.user_model import User
from dbs import message_db, problem_db, user_db
from dbs.db import *

CEO_NAME = 'Сидорчук Наталія'

console = Console()
app = typer.Typer()

current_user = User(4, 'Сидорчук Наталія', 'Директор')


@app.command(short_help='інформація про автора')
def about():
    typer.echo("Курсова робота з баз даних Топки Тіни, ІС-32.")


@app.command(short_help='вивід усіх учасників (users) / проблем (problems) / повідомлень (messages) / свої дані (myself)')
def show(what: str):
    if what is not None:
        if what == 'users':
            if current_user.role != 'Користувач':
                show_users()
            else:
                console.print('У вас немає доступу до цієї команди.')
        elif what == 'problems':
            show_problems()
        elif what == 'messages':
            choice = typer.prompt('Повідомлення надіслані (1) чи отримані (2)')
            if choice == '1' or choice == 'from-me':
                show_messages_sent()
            elif choice == '2' or choice == 'to-me':
                show_messages_received()
            else:
                console.print('Неправильно введено дані.')
        elif what == 'myself':
            show_myself()
        else:
            console.print('Введіть users, problems, messages або myself після команди show.')
    else:
        console.print('Введіть users, problems, messages або myself після команди show.')


@app.command(short_help='додавання учасника (user) / зауваження (problem)')
def add(what: str):
    if current_user.role == 'Користувач':
        console.print('У вас немає доступу до цієї команди.')
    elif what is not None:
        if what == 'user':
            add_user()
        elif what == 'problem':
            add_problem()
        else:
            console.print('Введіть user або problem після команди add.')
    else:
        typer.echo('Введіть user або problem після команди add.')


@app.command(short_help='оновлення учасника (user) / зауваження (problem)')
def update(what: str):
    if current_user.role == 'Користувач':
        console.print('У вас немає доступу до цієї команди.')
    elif what is not None:
        if what == 'user':
            update_user()
        elif what == 'problem':
            update_problem()
        else:
            console.print('Введіть user або problem після команди update.')
    else:
        typer.echo('Введіть user або problem після команди update.')


@app.command(short_help='видалення учасника (user) / зауваження (problem)')
def delete(what: str):
    if current_user.role == 'Користувач':
        console.print('У вас немає доступу до цієї команди.')
    elif what is not None:
        if what == 'user':
            delete_user()
        elif what == 'problem':
            delete_problem()
        else:
            console.print('Введіть user або problem після команди delete.')
    else:
        typer.echo('Введіть user або problem після команди delete.')


# User
def add_user():
    name = typer.prompt("Прізвище та ім'я")
    role = typer.prompt("Роль")
    user = User(0, name, role)
    insert_user(user)
    typer.echo(f"Додано учасника: {name} | {role}")
    show_users()


def delete_user():
    id = typer.prompt('Id учасника')
    delete_user_db(id)
    typer.echo(f"Видалено учасника {id}")
    show_users()


def update_user():
    id = typer.prompt('Id учасника')
    name = typer.prompt("Прізвище Ім'я")
    role = typer.prompt("Роль")
    if name is not None or role is not None:
        update_user(id, name, role)
        typer.echo(f"Оновлено дані про учасника\n{id}")
        show_users()
    else:
        typer.echo('Не коректно введено дані')


def show_users():
    users = get_all_users()
    console.print("[bold magenta]Учасники[/bold magenta]")

    table = Table(show_header=True, header_style="bold blue")
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
        table.add_row(cut_str(user.name), f'[{color}]{cut_str(user.role)}[/{color}]')
    console.print(table)


def show_myself():
    console.print(current_user.id)
    console.print(current_user.name)
    console.print(current_user.role)


# Problem

def add_problem():
    title = typer.prompt("Назва")
    progress = typer.prompt("Статус")
    problem = Problem(0, title, progress)
    insert_problem(problem)
    typer.echo(f"Додано зауваження: {title} | {progress}")
    show_problems()


def delete_problem():
    id = typer.prompt('Id зауваження')
    delete_problem_db(id)
    typer.echo(f"Видалено зауваження {id}")
    show_problems()


def update_problem():
    id = typer.prompt('Id зауваження')
    title = typer.prompt("Назва")
    progress = typer.prompt("Статус")
    if title is not None or progress is not None:
        update_problem(id, title, progress)
        typer.echo(f"Оновлено дані про зауваження\n{id}")
        show_problems()
    else:
        typer.echo('Не коректно введено дані')


def show_problems():
    problems = get_all_problems()
    console.print("[bold magenta]Зауваження[/bold magenta]")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("№", width=5, style="dim")
    table.add_column("Назва", min_width=15)
    table.add_column("Статус", min_width=12)

    for i, prob in enumerate(problems, start=1):
        table.add_row(str(i), cut_str(prob.title), cut_str(prob.progress))
    console.print(table)


# Message

@app.command(short_help='надсилання повідомлення')
def send():
    mssg_date = datetime.datetime.now()

    sender_id = current_user.id

    if current_user.role == 'Користувач':
        receiver_name = CEO_NAME
        row = find_user(receiver_name)
        receiver_id = row[0]
    else:
        while True:
            receiver_name = typer.prompt("Кому (Прізвище Ім'я)")
            row = find_user(receiver_name)
            if row is None:
                typer.echo('Не знайдено такого учасника')
            else:
                receiver_id = row[0]
                break

    while True:
        mssg_type_num = int(typer.prompt("Тип (Проблема - 1, Побажання - 2)"))
        if mssg_type_num == 1:
            mssg_type = 'Проблема'
            break
        elif mssg_type_num == 2:
            mssg_type = 'Побажання'
            break
        else:
            console.print('Неправильно введені дані. Спробуйте ще раз.')

    problem_name = typer.prompt("Проблема")
    row = find_problem(problem_name)
    if row is None:
        new_problem = Problem(0, problem_name, 'На розгляді')
        insert_problem(new_problem)
        row = find_problem(problem_name)
    problem_id = row[0]

    descript = typer.prompt("Опис")

    message = Message(0, descript, mssg_type, mssg_date, sender_id, receiver_id, problem_id)
    send_message(message)

    typer.echo("Надіслано повідомлення")


def show_messages_sent():
    console.print("[bold magenta]Надіслані повідомлення[/bold magenta]")
    messages = get_all_messages_sent(current_user.id)
    if messages is not None:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("№", width=5, style="dim")
        table.add_column("Дата", min_width=12)
        table.add_column("До", min_width=12)
        table.add_column("Тип", min_width=12)
        table.add_column("Проблема", min_width=12)
        table.add_column("Опис", min_width=20)

        for i, mes in enumerate(messages, start=1):
            table.add_row(str(i),
                          mes.mssg_date.strftime("%d/%m/%Y %H:%M"),
                          cut_str(str(mes.receiver)),
                          cut_str(mes.mssg_type),
                          cut_str(str(mes.problem)),
                          cut_str(mes.descript))
        console.print(table)
    else:
        console.print('Немає повідомлень')


def show_messages_received():
    console.print("[bold magenta]Отримані повідомлення[/bold magenta]")
    messages = get_all_messages_received(current_user.id)
    if messages is not None:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("№", width=5, style="dim")
        table.add_column("Дата", min_width=12)
        table.add_column("Від", min_width=12)
        table.add_column("Тип", min_width=12)
        table.add_column("Проблема", min_width=12)
        table.add_column("Опис", min_width=20)

        for i, mes in enumerate(messages, start=1):
            table.add_row(str(i),
                          mes.mssg_date.strftime("%d/%m/%Y %H:%M"),
                          cut_str(str(mes.sender)),
                          cut_str(mes.mssg_type),
                          cut_str(str(mes.problem)),
                          cut_str(mes.descript))
        console.print(table)
    else:
        console.print('Немає повідомлень')


def cut_str(text: str):
    return " ".join(text.split())


@app.command()
def login():
    console.print(f'[bold magenta]Вхід[/bold magenta]\nВведіть свій Id в системі')
    current_id = int(typer.prompt('Id'))
    row = find_user_id(current_id)
    if row is not None:
        current_name = cut_str(row[1])
        current_role = cut_str(row[2])
        global current_user
        current_user.id = row[0]
        current_user.name = current_name
        current_user.role = current_role
        console.print(f'Добрий день, [bold magenta]{current_user.name}[/bold magenta]!')
    else:
        typer.echo('Не знайдено такого учасника')


def main():
    console.print(f'[bold magenta]Вхід[/bold magenta]!\nВведіть свій Id в системі')
    current_id = int(typer.prompt('Id: '))
    login(current_id)


if __name__ == '__main__':
    app()
