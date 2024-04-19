# first page for client (fpfc)
import pyfiglet
import termcolor



class User:
    user_info = []

    def main_page(self):
        quarto = pyfiglet.figlet_format('Q u a r t o')
        quarto = termcolor.colored(quarto, color='blue')
        text = termcolor.colored('By Seyed Mohsen Razavi Zadegan\n StdNum : 40030489', color='blue')
        print(quarto, text)
        print('\n\n---> Login \n---> Signup\n---> Exit')
        while True:
            los = input()
            if los == 'Login':
                self.login()
                break
            elif los == 'Signup':
                self.sign_up()
                break
            elif los == 'Exit':
                break
            else:
                print('---> Enter your choice as same as message.')

    def sign_up(self):
        userPass = open('user_pass.txt', 'a')
        user_Pass = (open('user_pass.txt').readlines())[1:]
        mojaz_color = ['red', 'green', 'yellow',
                    'blue', 'magenta', 'cyan', 'white']

        euser_name = input('Enter your user name(dont use space) : ')
        epassword = input('Enter you password(dont use space) : ')
        user_color = input('enter your color : \nred - green - yellow - blue - magneta - cyan - white')
        while True:
            while user_color not in mojaz_color:
                print("The color doesn't supported")
                user_color = input('enter your color : \ngrey - red - green - yellow - blue - magneta - cyan - white\n')

            for i in user_Pass:
                if euser_name in user_Pass and epassword in user_Pass:
                    print('This accuont already exists.')
                    return 'Restart the game'
            User.user_info.append(euser_name)
            User.user_info.append(epassword)
            User.user_info.append(user_color)
            print(f'Signup successfull !  \nWelcome {euser_name} \nEnter START to start game')
            userPass.write('\n')
            for i in User.user_info:
                userPass.write(i+' ')
            userPass.close()
            s = input()
            while True:
                if s == 'START':
                    self.start_game()
                    break
                else:
                    print('---> Enter your choice as same as message.')
                    s = input()
            break

    def login(self):
        found = 0
        userPass = ((open('user_pass.txt')).readlines())[1:]
        UP = [a.split(' ') for a in userPass]
        euser_name = input('Enter your user name : ')
        epassword = input('Enter you password : ')
        for i in UP:
            if i[0] == euser_name and i[1] == epassword:
                found = 1
                print(f'Login successfull ! \nWelcome {euser_name} \nEnter START to start game')
                User.user_info = i
                s = input()
                while True:
                    if s == 'START':
                        self.start_game()
                        break
                    else:
                        print('---> Enter your choice as same as message.')
                        s = input()
        if found == 0 :
            print(
                "Wrong login information \n---> Cancel\n---> Login again \nDon't have an account ? Enter Signup to "
                "create one .")
            what_to_do_what_not_to_do = input()  # arastoo amel
            while True:
                if what_to_do_what_not_to_do == 'Cancel':
                    return 'You canceled the game'
                elif what_to_do_what_not_to_do == "Signup":
                    self.sign_up()
                    break
                elif what_to_do_what_not_to_do == "Login again" or what_to_do_what_not_to_do == "Login":
                    self.login()
                    break
                else:
                    print('---> Enter your choice as same as message.')
                    what_to_do_what_not_to_do = input()

    def start_game(self):
        print('---> Waiting for other player ...')
        return 1

    def new_game(self):
        print('---> Would you like to start a new game ?\n---> New Game\n---> Exit')
        noe = input()
        while True:
            if noe == 'New Game':
                User.main_page(self)
                break
            elif noe == 'Exit':
                return 'Exit'
                break
            else:
                print('---> Enter your choice as same as message.')
                noe = input()