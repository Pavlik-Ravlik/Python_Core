contacts = {}


def input_error(func):
    def inner(*args):
        try:
            return func(*args)

        except (KeyError, ValueError, IndexError) as f:
            return str(f)

    return inner


def normalise(number):
    new_phone = (
        number.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone


def handle_hello():
    return 'How can I help you?\n add - the bot saves in memory a new contact\n change - the bot saves a new phone number for an existing contact in memory\n phone - the bot outputs the phone number for the specified contact to the console.\n show all - By this command, the bot displays all saved contacts with phone numbers to the console.\n good bye, close, exit - on any of these commands, the bot completes its robot after'


def handler_add(name, number):
    number = normalise(number)

    if len(name) == 0 or name.isdigit() or len(number) < 12 or number.isalpha():
        raise ValueError(
            'Please enter the correct name and phone number, the name must be a period and the number must be numbers, preferably without symbols')

    contacts[name.lower()] = number
    return f'Added contact - {name} : with phone - {number}'


def handler_change(name, number):
    number = normalise(number)

    if name not in contacts:
        raise KeyError(f"{name} : is not in contacts")

    contacts[name.lower()] = number
    return f'Changed phone for contact - {name} : to - {number}'


def handler_phone(name):

    if name.lower() not in contacts:
        raise KeyError(f"{name}: is not in contacts")

    return contacts[name.lower()]


def handle_show_all(contacts):
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])


def main():

    while True:
        comands = input('Type hello to see a list of commands: ').lower()

        # По цій команді бот виводить усі доступні команди.
        if comands == 'hello':
            print(handle_hello())

        # По цій команді бот зберігає новий контакт.
        elif comands == 'add':
            name_and_phone = input(
                'Please enter your name and phone number separated by a comma: ')

            try:
                name, number = name_and_phone.rsplit(',', 1)
                message = handler_add(name, number)

            except ValueError as e:
                print(str(e))

        # По цій команді бот змінює номер телефону по існуючому контакту.
        elif comands == 'change':
            name_and_phone = input(
                'Please enter your name and phone number separated by a comma: ')

            try:
                name, number = name_and_phone.rsplit(',', 1)
                message = handler_change(name, number)

            except (KeyError, ValueError) as e:
                print(str(e))

        # По цій команді бот виводить на екран номер телефону існуючого контакту.
        elif comands == 'phone':
            name = input('Please enter the name: ')

            try:
                message = handler_phone(name)

            except KeyError as e:
                print(str(e))

        # По цій команді бот виводить на екран усі номера телефонів.
        elif comands == "show all":

            if len(contacts) >= 1:
                message = handle_show_all(contacts)
            elif len(contacts) == 0:
                message = 'Empty list'

        # По цій команді бот закінчує свою роботу.
        elif comands == 'good bye' or 'close' or 'exit':
            print('Good bye =)')
            break

        else:
            message = "Unknown command. Please try again."
        print(message)


if __name__ == '__main__':
    main()
