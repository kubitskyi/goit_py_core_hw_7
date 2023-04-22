import json
from datetime import datetime
from classes import UserName, PhoneNumber, Record, ContactsBook, Birthday


ADRESS_BOOK =  ContactsBook()
DATA = 'data.json'
users = []

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError as ex:
            print(ex)
            return ex
        except KeyError as ex:
            return ex
        except ValueError as ex:
            return ex
        except TypeError as ex:
            return ex
    return inner

@input_error
def hello(*args):
    return "How can I help you?"

def help(*args):
    return"""Tthis is an instruction"""

@input_error
def add_phone(*args):
    lst_param = args[0].split()
    name = UserName(lst_param[0])
    phone = PhoneNumber(lst_param[1])
    if len(lst_param) < 3:
        birthday = None
    else:
        birthday = Birthday(datetime.strptime(lst_param[2], '%Y-%m-%d').date())
        

    for contact, rec in ADRESS_BOOK.items(): 
        if name.value == contact:
            rec.add_number(phone)
            return f'{rec.name.value.capitalize()}: {rec.numbers}'
    else:
        record = Record(name,phone, birthday)
        ADRESS_BOOK.add_contact(record)
    
    


@input_error
def change_phone(*args):
    lst_param = args[0].split()
    contact = UserName(lst_param[0])
    old_number = PhoneNumber(lst_param[1])
    new_number = PhoneNumber(lst_param[2])
    for k, v in ADRESS_BOOK.items():
        if k == contact.value:
            v.change_number(old_number,new_number)
    return f'{contact.value.capitalize()}: {new_number.value}'

@input_error
def show_phone(*args):
    contact = args[0]
    for name, record  in ADRESS_BOOK.items():
        if name == contact:
            return record.numbers
    return 'Number not found'

def show_all(*args):
    return '\n'.join([str(k) + ': ' + str(v) for k,v in ADRESS_BOOK.items()])

@input_error
def exit(*args):
    return 'Bay'


def add_birthday(*args):
    name = args[0]
    bh = args[1]
    for k, v in ADRESS_BOOK.items():
        if k == name:
            v.add_birthday(Birthday(datetime.strptime(bh,'%Y-%m-%d').date()))

def to_birthday(name):
    day_to_bh = 0
    for k, v in ADRESS_BOOK.items():
        if k == name:
            day_to_bh = v.days_to_birthday()
    return day_to_bh

def paginator(iter_obj, page=2):
    start =0
    while True:
        result_key = list(iter_obj)[start:start + page]
        result = [iter_obj.get(k) for k in result_key]
        if not result:
            break
        yield result
        start += page

def search(param):
    return ADRESS_BOOK.search(param)

COMMANDS = {help: 'help',
            add_phone: 'add',
            show_phone: "show",
            change_phone: "change",
            show_all: "all",
            exit: 'exit',
            add_birthday: 'birthday',
            to_birthday: 'tobirthday',
            search: "search"}

def command_handler(text: str):
    for command, kword in COMMANDS.items():
        if text.startswith(kword):
            
            return command, text.replace(kword, '').strip()
    return None, None

def main():
    while True:
        try:
            ADRESS_BOOK.load_data(DATA)
        except json.decoder.JSONDecodeError:
            pass

        user_input = input('>>>')

        command, data = command_handler(user_input)
        print(command(data))

        ADRESS_BOOK.save_data(DATA)

        if command == exit:
            break
    

if __name__=="__main__":
    main()