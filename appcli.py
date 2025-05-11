import typer
from rich.console import Console
from rich.table import Table
from models.message_model import Message
from models.problem_model import Problem
from models.user_model import User
from dbs.db import *
import json

console = Console()
app = typer.Typer()


USER_FILE = 'current_user.json'

CEO_NAME = 'Сидорчук Наталія'

# console.print
ERROR_MESS = f'[bold magenta]Виникла помилка.[/bold magenta]'
INCORRECT_DATA = f'[bold magenta]Неправильно введено дані.[/bold magenta]'
NO_ACCESS = f'[bold magenta]У Вас немає доступу до цієї команди.[/bold magenta]'

USER_NOT_FOUND = f'[bold magenta]Не знайдено такого користувача.[/bold magenta]'
PROBLEM_NOT_FOUND = f'[bold magenta]Не знайдено такого зауваження.[/bold magenta]'
MESSAGE_NOT_FOUND = f'[bold magenta]Не знайдено такого повідомлення.[/bold magenta]'

NO_MESSAGES = f'[bold blue]Немає повідомлень.[/bold blue]'
MESSAGE_SENT = f'[bold magenta]Повідомлення надіслано.[/bold magenta]'

SHOW_TIP = f'Введіть [italic yellow]users[/italic yellow], [italic yellow]problems[/italic yellow], [italic yellow]messages[/italic yellow] або [italic yellow]myself[/italic yellow] після команди [italic yellow]show[/italic yellow].'
ADD_TIP = f'Введіть [italic yellow]user[/italic yellow], [italic yellow]problem[/italic yellow] після команди [italic yellow]add[/italic yellow].'
DELETE_TIP = f'Введіть [italic yellow]user[/italic yellow], [italic yellow]problem[/italic yellow], [italic yellow]message[/italic yellow] після команди [italic yellow]delete[/italic yellow].'
UPDATE_TIP = f'Введіть [italic yellow]user[/italic yellow], [italic yellow]problem[/italic yellow] після команди [italic yellow]update[/italic yellow].'


def save_user(id: int, name: str, role: str):
    user_info = {
        'id': id,
        'name': name,
        'role': role
    }
    json_object = json.dumps(user_info, indent=3)
    with open(USER_FILE, 'w') as f:
        f.write(json_object)


def load_user():
    if os.path.exists(USER_FILE):
        extracted = []
        with open(USER_FILE, 'r') as f:
            json_object = json.load(f)
            extracted.append(json_object['id'])
            extracted.append(json_object['name'])
            extracted.append(json_object['role'])
        return extracted
    return None


def quit_user():
    if os.path.exists(USER_FILE):
        os.remove(USER_FILE)
    else:
        console.print(ERROR_MESS)


@app.command()
def login():
    if load_user() is None:
        console.print(f'[bold magenta]Вхід[/bold magenta]\nВведіть свій Id в системі')
        current_id = int(typer.prompt('Id'))
        row = find_user_id(current_id)
        if row is not None:
            current_name = cut_str(row[1])
            current_role = cut_str(row[2])
            save_user(current_id, current_name, current_role)
            console.print(f'Добрий день, [bold magenta]{current_name}[/bold magenta]!')
        else:
            console.print(USER_NOT_FOUND)
    else:
        logout()
        login()


@app.command()
def logout():
    console.print(f'[bold magenta]Вихід із системи...[/bold magenta]')
    if load_user() is not None:
        quit_user()
    console.print(f'[bold magenta]До побачення![/bold magenta]')


def show_myself():
    current_user = load_user()
    if current_user is None:
        console.print(ERROR_MESS)
    else:
        console.print(current_user[0])
        console.print(current_user[1])
        console.print(current_user[2])


@app.command(short_help='інформація про автора')
def about():
    console.print(f"[bold magenta]Курсова робота з баз даних [bold blue]Топки Тіни, ІС-32[/bold blue].[/bold magenta]")


@app.command(short_help='вивід усіх користувачів (users) / проблем (problems) / повідомлень (messages) / свої дані (myself)')
def show(what: str):
    current_user = load_user()
    if what is not None:
        if what == 'users':
            show_users()
        elif what == 'problems':
            show_problems()
        elif what == 'messages':
            if current_user is not None:
                choice = typer.prompt('Повідомлення надіслані чи отримані [1/2]')
                if choice == '1' or choice == 'from-me':
                    show_messages_sent()
                elif choice == '2' or choice == 'to-me':
                    show_messages_received()
                else:
                    console.print(INCORRECT_DATA)
            else:
                console.print(NO_ACCESS)
        elif what == 'myself':
            show_myself()
        else:
            console.print(SHOW_TIP)
    else:
        console.print(SHOW_TIP)


@app.command(short_help='додавання користувача (user) / зауваження (problem)')
def add(what: str):
    current_user = load_user()
    if current_user[2] == 'Користувач':
        console.print(NO_ACCESS)
    elif what is not None:
        if what == 'user':
            add_user()
        elif what == 'problem':
            add_problem()
        else:
            console.print(ADD_TIP)
    else:
        console.print(ADD_TIP)


@app.command(short_help='оновлення користувача (user) / зауваження (problem)')
def update(what: str):
    current_user = load_user()
    if current_user[2] == 'Користувач':
        console.print(NO_ACCESS)
    elif what is not None:
        if what == 'user':
            update_user()
        elif what == 'problem':
            update_problem()
        else:
            console.print(UPDATE_TIP)
    else:
        console.print(UPDATE_TIP)


@app.command(short_help='видалення користувача (user) / зауваження (problem) / повідомлення (message)')
def delete(what: str):
    current_user = load_user()
    if what is not None:
        if what == 'user':
            if current_user[2] == 'Користувач':
                console.print(NO_ACCESS)
                return
            delete_user()
        elif what == 'problem':
            if current_user[2] == 'Користувач':
                console.print(NO_ACCESS)
                return
            delete_problem()
        elif what == 'message':
            delete_message()
        else:
            console.print(DELETE_TIP)
    else:
        console.print(DELETE_TIP)


# User
def add_user():
    name = typer.prompt("Прізвище та ім'я")
    role = typer.prompt("Роль")
    user = User(0, name, role)
    insert_user(user)
    typer.echo(f"Додано користувача: {name} | {role}")
    show_users()


def delete_user():
    current_user = load_user()

    id = int(typer.prompt('Id користувача'))

    if id == current_user[0]:
        console.print(f'[bold magenta]Ви не можете видалити себе.[/bold magenta]')
        return

    row = find_user_id(id)
    if row is None:
        console.print(USER_NOT_FOUND)
        return
    mess_exist = check_user_in_mess(id)
    if mess_exist:
        console.print(f'[bold magenta]Користувач зазначається в повідомленнях![/bold magenta]')
        while True:
            check = typer.prompt('Видалити користувача? [y/n]')
            if check == 'y':
                break
            elif check == 'n':
                return
    delete_user_db(id, mess_exist)
    typer.echo(f"Видалено користувача {id}")
    show_users()


def update_user():
    id = int(typer.prompt('Id користувача'))
    name = typer.prompt("Прізвище Ім'я (або -)")
    role = typer.prompt("Роль (або -)")
    if name != "-" or role != "-":
        update_user_db(id, name, role)
        typer.echo(f"Оновлено дані про користувача {id}")
        show_users()
    else:
        console.print(INCORRECT_DATA)


def show_users():
    users = get_all_users()
    console.print("[bold magenta]Користувачі[/bold magenta]")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Ім'я", min_width=20)
    table.add_column("Роль", min_width=12)
    table.add_column("Id", min_width=5)

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
        table.add_row(cut_str(user.name), f'[{color}]{cut_str(user.role)}[/{color}]', str(user.id))
    console.print(table)


# Problem

def add_problem():
    title = typer.prompt("Назва")
    while True:
        console.print('Статус: 1 - На розгляді, 2 - У процесі, 3 - Виконано, 4 - Відхилено')
        progress_num = int(typer.prompt("[1/2/3/4]"))
        match progress_num:
            case 1:
                progress = 'На розгляді'
                break
            case 2:
                progress = 'У процесі'
                break
            case 3:
                progress = 'Виконано'
                break
            case 4:
                progress = 'Відхилено'
                break
            case _:
                console.print(INCORRECT_DATA)

    problem = Problem(0, title, progress)
    insert_problem(problem)
    typer.echo(f"Додано зауваження: {title} | {progress}")
    show_problems()


def delete_problem():
    id = int(typer.prompt('Id зауваження'))
    row = find_problem_id(id)
    if row is None:
        console.print(f'Зауваження {id} не існує.')
        return
    mess_exist = check_problem_in_mess(id)
    if mess_exist:
        console.print(f'[bold magenta]Це зауваження зазначається в повідомленнях![/bold magenta]')
        while True:
            check = typer.prompt('Видалити зауваження? [y/n]')
            if check == 'y':
                break
            elif check == 'n':
                return
    delete_problem_db(id, mess_exist)
    typer.echo(f"Видалено зауваження {id}")
    show_problems()


def update_problem():
    id = int(typer.prompt('Id зауваження'))
    title = typer.prompt("Назва (або -)")
    while True:
        console.print('Статус: 1 - На розгляді, 2 - У процесі, 3 - Виконано, 4 - Відхилено')
        progress_num = int(typer.prompt("[1/2/3/4]"))
        match progress_num:
            case 1:
                progress = 'На розгляді'
                break
            case 2:
                progress = 'У процесі'
                break
            case 3:
                progress = 'Виконано'
                break
            case 4:
                progress = 'Відхилено'
                break
            case _:
                console.print(INCORRECT_DATA)

    if title != "-" or progress != "-":
        update_problem_db(id, title, progress)
        typer.echo(f"Оновлено дані про зауваження {id}")
        show_problems()
    else:
        console.print(INCORRECT_DATA)


def show_problems():
    problems = get_all_problems()
    console.print("[bold magenta]Зауваження[/bold magenta]")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("№", width=5, style="dim")
    table.add_column("Назва", min_width=15)
    table.add_column("Статус", min_width=12)
    table.add_column("Id", min_width=5)

    for i, prob in enumerate(problems, start=1):
        table.add_row(str(i), cut_str(prob.title), cut_str(prob.progress), str(prob.id))
    console.print(table)


# Message
def delete_message():
    console.print(f'[bold magenta]Ви можете видалити тільки надіслані вами повідомлення![/bold magenta]')
    id = int(typer.prompt('Id повідомлення'))

    current_user = load_user()
    row = find_message_from_user(id, int(current_user[0]))
    if row is not None:
        delete_message_db(id)
        typer.echo(f"Видалено повідомлення {id}")
        show_messages_sent()
    else:
        console.print(MESSAGE_NOT_FOUND)


@app.command(short_help='надсилання повідомлення')
def send():
    current_user = load_user()

    mssg_date = datetime.datetime.now()

    sender_id = current_user[0]

    if current_user[2] == 'Користувач':
        receiver_name = CEO_NAME
        row = find_user(receiver_name)
        receiver_id = row[0]
        console.print('Кому: Директор')
    else:
        while True:
            receiver_name = typer.prompt("Кому [Прізвище Ім'я]")
            row = find_user(receiver_name)
            if row is None:
                typer.echo(USER_NOT_FOUND)
            else:
                receiver_id = row[0]
                break

    while True:
        mssg_type_num = int(typer.prompt("Тип [Проблема - 1, Побажання - 2]"))
        if mssg_type_num == 1:
            mssg_type = 'Проблема'
            break
        elif mssg_type_num == 2:
            mssg_type = 'Побажання'
            break
        else:
            console.print(INCORRECT_DATA)

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

    console.print(MESSAGE_SENT)


def show_messages_sent():
    current_user = load_user()

    console.print("[bold magenta]Надіслані повідомлення[/bold magenta]")
    messages = get_all_messages_sent(current_user[0])
    if messages:
        show_message_table(True, messages)
    else:
        console.print(NO_MESSAGES)


def show_messages_received():
    current_user = load_user()

    console.print("[bold magenta]Отримані повідомлення[/bold magenta]")
    messages = get_all_messages_received(current_user[0])
    if messages:
        show_message_table(False, messages)
    else:
        console.print(NO_MESSAGES)


def show_message_table(choice: bool, messages):
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("№", width=5, style="dim")
    table.add_column("Дата", min_width=12)
    table.add_column("До" if choice else "Від", min_width=12)
    table.add_column("Тип", min_width=12)
    table.add_column("Проблема", min_width=12)
    table.add_column("Опис", min_width=20)
    table.add_column("Id", min_width=4)

    for i, mes in enumerate(messages, start=1):
        table.add_row(str(i),
                      mes.mssg_date.strftime("%d/%m/%Y %H:%M"),
                      cut_str(str(mes.receiver) if choice else str(mes.sender)),
                      cut_str(mes.mssg_type),
                      cut_str(str(mes.problem)),
                      cut_str(mes.descript),
                      str(mes.id))
    console.print(table)


def cut_str(text: str):
    return " ".join(text.split())


if __name__ == "__main__":
    app()
