from cryptography.fernet import InvalidToken
from helpers.controller import Controller, help_menu
from helpers.login import Login
import speech_recognition as sr

def main():
    controller = Controller()
    print("Welcome to password saver!")
    help_menu()
    while True:
        try:
            do_what = input('What you want to do? ')
            if do_what == 's':
                while True:
                    search = input('Enter part of the login: ')
                    controller.search(search)
                    break
            if do_what == 'sr':
                while True:
                    r = sr.Recognizer()
                    with sr.Microphone() as source:
                        print("Talk")
                        search = r.listen(source)
                        print("Time over, thanks")
                    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling

                    try:
                        # using google speech recognition
                        print("Text: "+r.recognize_google(search))
                        controller.search(r.recognize_google(search))
                    except:
                        print("Sorry, I did not get that")
                    # controller.search(search)
                    break
            elif do_what == 'c':
                while True:
                    controller.show_all()
                    search = input('Enter ID of login: ')
                    try:
                        controller.get_password(int(search))
                        print('Password copied to clipboard!')
                    except InvalidToken:
                        print('Invalid key!')
                    break
            elif do_what == 'a':
                while True:
                    login = input('Enter login: ')
                    password = input('Enter password: ')
                    desc = input('Enter description: ')
                    login_data = Login(login, password, desc)
                    controller.save(login_data)
                    break
            elif do_what == 'd':
                while True:
                    controller.show_all()
                    search = input('Enter ID of login to delete: ')
                    controller.delete(search)
                    break
            elif do_what == 'all':
                controller.show_all()
            elif do_what == 'uuid-show':
                controller.show_uuid()
            elif do_what == 'help':
                help_menu()
            else:
                print(f'Unrecognized command - {do_what}')
        except EOFError:
            print('See you later!')
            break


if __name__ == '__main__':
    main()
