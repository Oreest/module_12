from AddressBook import Record, AddressBook

contacts = AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Wrong name'
        except TypeError:
            return 'Please enter correct command'
        except IndexError:
            return 'Wrong amount values'
        except ValueError:
            return "Give me Name and Phone Number, please"

    return inner


@input_error
def add(data: list):
    if contacts.has_record(data[0]):
        raise KeyError
    if not (data[1].strip()).isnumeric():
        raise ValueError
    record = Record(data[0].strip())
    # print("created record ", data[0].strip())
    for phone in data[1:]:
        record.add_phone(phone)
        # print(f"added {phone} to contact {data[0]}")
    contacts.add_record(record)
    return f'Added new Contact "{data[0]}"'


@input_error
def change(data):
    if not contacts.has_record(data[0]):
        return "No such contact"
    if not (data[1]).isnumeric():
        raise ValueError
    record = contacts.get_record(data[0])
    record.edit_phone(data[1], data[2])
    return f'Number {data[1]} with name {data[0]} was changed.'


@input_error
def find_phone(name):
    return contacts.get_record(name[0])


# def help_command():
@input_error
def show_all():
    all_contacts = ''
    page_number = 1

    for page in contacts.iterator():
        all_contacts += f'Page #{page_number}\n'

        for record in page:
            all_contacts += f'{record.get_info()}\n'
        page_number += 1
    print(all_contacts)


@input_error
def hello():
    return 'Hello, How can I help you?'


@input_error
def wrong_command():
    return 'Wrong command.. Make sure you typed correctly and try again.'


def delete(name):
    contacts.delete(name[0].strip())
    return 'contact has been deleted'


def birthday(data):
    # command example: birthday john 2011-01-18
    record = contacts.get_record(data[0])
    print(record)
    record.birthday = data[1]
    return f"added birthday to contact{data[0]}"


def days_to_birthday(name):
    # command example: bday john
    return contacts.get_record(name[0]).days_to_birthday()


def find(data):
    # command example find test123
    for contact in contacts.find_extended(data[0]):
        print(contact)


def show_help():
    available_commands = {
        'hello':    "say hello",
        'add':      "add contact, example add john 1234567890",
        'change':   'change number in existing contact. example: change John old_phone new_phone',
        'phone':    "find contact by name. example: phone John",
        'show all': "returns all contacts in book",
        'delete':   "remove contact from the book, example: delete john",
        'birthday': "set a birthday for contact, example: birthday john 2022-11-11",
        'bday':     'return days till next birthday of a contact, example: bday john',
        'find':     'find any matches in contact name or phones, example: find xxx'
    }
    for key, description in available_commands.items():

        print("{:<10} -> {}".format(key, description))


COMMANDS = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': find_phone,
    'show all': show_all,
    'wrong command': wrong_command,
    'delete': delete,
    'birthday': birthday,
    'bday': days_to_birthday,
    'find': find,
    'help': show_help
}


@input_error
def handler(user_line):
    result = {
        'user_command': '',
        'data': []
    }
    if user_line.lower() == 'show all':
        result['user_command'] = user_line.lower()
        # print(result)
        return result['user_command'], result['data']
    user_line_list = user_line.split(' ')
    # print(user_line_list)
    result['user_command'] = user_line_list[0].lower()
    result['data'] = user_line_list[1:]

    return result['user_command'], result['data']


@input_error
def command_handler(command):
    if command not in COMMANDS:
        return COMMANDS['wrong command']
    return COMMANDS[command]


def main():
    try:
        while True:
            user_input = input(">>")
            if user_input.lower() == 'exit' or user_input.lower() == 'good bye' or user_input.lower() == 'bye':
                print("Good bye")
                break
            command, data = handler(user_input)
            if not data:
                result = command_handler(command)
                result()
                continue
            result = command_handler(command)(data)
            if result:
                print(result)
    finally:
        contacts.save_data_to_file()


if __name__ == "__main__":
    print("Welcome to CLI contacts bot.")
    print("Please enter your command\nFor more info type 'help'")
    main()
