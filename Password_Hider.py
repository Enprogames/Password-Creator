import tkinter as tk
#import pyperclip
import hashlib
import random

user_seperator = "    "
item_seperator = ", "

class Login_Frame(tk.Frame):

    def __init__(self, parent, login_function, goto_register_function, skip_login_function, width=600, height=400):
        self.width = width
        self.height = height
        tk.Frame.__init__(self, parent, width=width, height=height, bg="grey25")
        self.parent = parent
        self.login_function = login_function
        self.goto_register_function = goto_register_function

        self.loginmessageLabel = tk.Label(self, text="Login Failed", fg="grey25", bg="grey25",
                                     font=('consolas', 10, 'bold'))
        self.loginmessageLabel.place(relx=.5, rely=.05, anchor="center")

        self.login_label = tk.Label(self, text="LOGIN", fg="white", bg="grey25", font=('consolas', 50, 'bold'))
        self.login_label.place(relx=.5, rely=.2, anchor="center")

        self.usernamelabel = tk.Label(self, text="Username", font=('consolas', 10, 'bold'), bg="grey25", fg="white")
        self.usernamelabel.place(relx=.5, rely=.45, anchor="center")
        self.usernamebox = tk.Entry(self, width="20")
        self.usernamebox.place(relx=.5, rely=.5, anchor="center")

        self.passwordlabel = tk.Label(self, text="Password", font=('consolas', 10, 'bold'), bg="grey25", fg="white")
        self.passwordlabel.place(relx=.5, rely=.6, anchor="center")
        self.passwordbox = tk.Entry(self, width="20")
        self.passwordbox.place(relx=.5, rely=.65, anchor="center")

        self.changetoregisterbutton = tk.Button(self, text="register", font=('consolas', 10, 'bold'), bg="white", fg="black", command=goto_register_function)
        self.changetoregisterbutton.place(relx=.43, rely=.75, anchor="center")

        self.loginbutton = tk.Button(self, text="login", font=('consolas', 10, 'bold'), bg="white", fg="black", command=login_function)
        self.loginbutton.place(relx=.58, rely=.75, anchor="center")

        self.no_loginbutton = tk.Button(self, text="Enter Without Account", font=('consolas', 10, 'bold'), bg="white", fg="black", command=skip_login_function)
        self.no_loginbutton.place(relx=.5, rely=.85, anchor="center")

        self.usernamebox.insert(0, "xXBroccoliLoverXx")
        self.passwordbox.insert(0, "p2ssw0rd1")


class Register_Frame(tk.Frame):

    def __init__(self, parent, register_function, goto_login_function, width=600, height=400):
        self.width = width
        self.height = height
        tk.Frame.__init__(self, parent, width=width, height=height, bg="grey25")
        self.parent = parent
        self.register_function = register_function
        self.goto_login_function = goto_login_function

        self.registermessagelabel = tk.Label(self, text="User Already Exists", bg="grey25", fg="grey25")
        self.registermessagelabel.place(relx=.5, rely=.05, anchor="center")

        self.register_label = tk.Label(self, text="REGISTER", fg="white", bg="grey25",
                                  font=('consolas', 50, 'bold'))
        self.register_label.place(relx=.5, rely=.2, anchor="center")

        self.registerusernamelabel = tk.Label(self, text="Username", font=('consolas', 10, 'bold'), bg="grey25",
                                         fg="white")
        self.registerusernamelabel.place(relx=.5, rely=.4, anchor="center")
        self.registerusernamebox = tk.Entry(self)
        self.registerusernamebox.place(relx=.5, rely=.45, anchor="center")

        self.registerpasswordlabel = tk.Label(self, text="Password", font=('consolas', 10, 'bold'), bg="grey25",
                                         fg="white")
        self.registerpasswordlabel.place(relx=.5, rely=.5, anchor="center")
        self.registerpasswordbox = tk.Entry(self)
        self.registerpasswordbox.place(relx=.5, rely=.55, anchor="center")

        self.confirmpasswordlabel = tk.Label(self, text="Confirm Password", font=('consolas', 10, 'bold'),
                                        bg="grey25", fg="white")
        self.confirmpasswordlabel.place(relx=.5, rely=.6, anchor="center")
        self.confirmpasswordbox = tk.Entry(self, width="20")
        self.confirmpasswordbox.place(relx=.5, rely=.65, anchor="center")

        self.registerbutton = tk.Button(self, text="register", font=('consolas', 10, 'bold'), bg="white",
                                   fg="black", command=register_function)
        self.registerbutton.place(relx=.43, rely=.85, anchor="center")

        self.changetologinbutton = tk.Button(self, text="login", font=('consolas', 10, 'bold'), bg="white",
                                        fg="black", command=goto_login_function)
        self.changetologinbutton.place(relx=.58, rely=.85, anchor="center")

        self.registerusernamebox.insert(0, "xXBroccoliLoverXx")  # temporary for debugging
        self.registerpasswordbox.insert(0, "p2ssw0rd1")  # temporary for debugging
        self.confirmpasswordbox.insert(0, "p2ssw0rd1")  # temporary for debugging


class File_Reader:
    def __init__(self, url):
        self.url = url

    def read_file_data(self):
        file = open(self.url, 'r')
        #contents = base64.b64decode(file.read().encode('utf-8')).decode('utf-8')
        contents = file.read()
        #print(contents)
        file.close()
        if len(contents) == 0: return ""
        return contents

    def write_file_data(self, data):
        file = open(self.url, 'w')
        #print(data, base64.b64encode(data))
        #file.write(base64.b64encode(data.encode('utf-8')).decode('utf-8'))
        file.write(data)
        file.close()

    def append_file_data(self, data):
        contents = self.read_file_data()
        #file = open(self.url, 'w', encoding='utf-8')
        file = open(self.url, 'w')
        if len(contents) == 0:
            #file.write(base64.b64encode(data.encode('utf-8')).decode('utf-8'))
            file.write(data)
        else:
            file.write(contents + user_seperator + data)
            #file.write(base64.b64encode((contents + user_seperator + data).encode('utf-8')).decode('utf-8'))
        file.close()


class User:
    def __init__(self, username, password, websites = None):
        self.username = username  # encrypted username
        self.password = password  # hashed password
        self.websites = websites  # list of website data lists
        self.websites = [['facebook', '8', '.'], ['roblox']]
        if self.websites == []:
            self.websites = None

    # def new_password(self, website):
    #     if website in self.websites:
    #         pass
    #     return hashlib.md5(self.username + self.password + website)

    def add_website(self, address, length=8, chars=None):
        if self.websites == None:
            self.websites = []
        self.websites.append([address, length, chars])

    def get_username(self):
        return simple_decrypt(self.username)

    def get_password(self):
        return self.password

    def __str__(self):
        return "Username: " + self.username + " Password: " + self.password + " Websites: " + str(self.websites)

    def encrypted_data(self):
        if self.websites is None:
            return str(simple_encrypt(self.username) + item_seperator + hashlib.md5(self.password.encode('utf-8')).hexdigest())
        else:
            raw_website_data = "[" # data in the websites as a string
            if not len(self.websites) == 0:
                for j in range(len(self.websites)): # loops through the array containing the data for the websites
                    raw_website_data = raw_website_data + '[' + ", ".join(self.websites[j]) + ']'
                    if j < len(self.websites)-1:
                        raw_website_data += ', '
            raw_website_data += "]"
            return str(simple_encrypt(self.username) + item_seperator + hashlib.md5(self.password.encode('utf-8')).hexdigest() + item_seperator + raw_website_data)
            

def get_users():

    # structure of file:
    # [encrypted username, hashed password, websites and passwords]
    # websites and passwords:
    # [hashed website address, (optional) optimal length, (optional) which characters the password requires]
    users = []
    output = []
    username = ""
    password = ""
    websites = []
    if not file_contents == "":

        for i in range(len(file_contents.split(user_seperator))):  # loops through each part of file separated by three spaces
            users.append([])
            for item in file_contents.split(user_seperator)[i].split(item_seperator): # loops through each comma seperated element in the current line of the file
                line = file_contents.split(user_seperator)[i]

                if not '[' in item: # if there is no square bracket, there is no website data for the user on this line
                    users[i].append(item.strip())
                    #print(users[i][0], simple_decrypt(users[i][0]))
                else: # there is website data

                    website_args = line[file_contents.split(user_seperator)[i].index(item) + 1:-1].split(item_seperator)
                    website_args = [x.strip() for x in website_args] # strip each element in the website_args list
                    users[i].append(website_args)
                    break

        for user in users:
            username = ""
            password = ""
            websites = []
            for i in range(len(user)):
                if i == 0:
                    username = user[i]
                elif i == 1:
                    password = user[i]
                else:
                    websites.append(user[i])
            user = User(username, password, websites)
            #print(user.encrypted_data())
            output.append(User(username, password, websites))
        return output
    else:
        return []


def update_user_data(username):
    for i in range(len(users)):
        if username == users[i].username:
            users[i] = current_user

def simple_encrypt(x):
    x = list(str(x))
    output = ""
    for i in x:

        num = str(printable_chars.index(i))
        output += num.zfill(3)

    return output


def simple_decrypt(x):
    output = ""
    a = []
    for i in range(0, len(x)+1):
        if i % 3 == 0 and i > 0:
            a.append(x[i-3:i])
    for i in a:
        output += printable_chars[int(i)]
    return output


def goto_frame(frame):
    global current_user
    if not frame == main_frame:
        current_user = None
        websites_menu.place_forget()
        add_website_button.place_forget()
        remove_website_button.place_forget()
    login_frame.pack_forget()
    register_frame.pack_forget()
    main_frame.pack_forget()
    frame.pack()


def login_button():

    global current_user

    username = login_frame.usernamebox.get()
    password = login_frame.passwordbox.get()

    for user in users:
        if username == '':
            login_frame.loginmessageLabel.config(text = "Please Enter a Username", fg='white')
        elif password == '':
            login_frame.loginmessageLabel.config(text = "Please Enter a Password", fg='white')
        elif not username == user.get_username() or not hashlib.md5(password.encode('utf-8')).hexdigest() == user.get_password(): # username or password is incorrect
            login_frame.loginmessageLabel.config(text = "Username or Password Incorrect", fg='white')
        else:
            login_frame.loginmessageLabel.config(fg='grey25')
            current_user = user
            goto_frame(main_frame)
            websites_menu.place(relx='0.7', rely='0.45', anchor='n')
            add_website_button.place(relx='0.7', rely='0.55', anchor='n')
            remove_website_button.place(relx='0.8', rely='0.65', anchor='n')
            break


    # remove this later
    # goto_frame(main_frame)


def register_button():

    global current_user

    username = register_frame.registerusernamebox.get()
    password = register_frame.registerpasswordbox.get()
    confirm_password = register_frame.confirmpasswordbox.get()
    if not password == confirm_password:
        register_frame.registermessagelabel.config(text='passwords don\'t match', fg='white')
    elif username == '':
        register_frame.registermessagelabel.config(text='Please input a username', fg='white')
    elif password  == '':
        register_frame.registermessagelabel.config(text='Please input a password', fg='white')
    else:
        register_frame.registermessagelabel.config(text='User Already Exists', fg='grey25')
        for user in users:
            #print(simple_decrypt(user.username), username, user.password, hashlib.md5(password.encode('utf-8')).hexdigest())
            if simple_decrypt(user.username) == username:
                print("user already exists")
                register_frame.registermessagelabel.config(fg='white')
                return # ends function if user already exists

        current_user = User(username, password)
        users.append(current_user)
        goto_frame(main_frame)
        websites_menu.place(relx='0.7', rely='0.45', anchor='n')
        add_website_button.place(relx='0.7', rely='0.55', anchor='n')
        remove_website_button.place(relx='0.8', rely='0.65', anchor='n')
        user_file.append_file_data(current_user.encrypted_data())


def isint(number):
    try:
        int(number)
        return True
    except:
        return False


def create_login_button_command():

    website = url_box.get()
    optimal_length = optimal_length_box.get()
    if isint(optimal_length):
        optimal_length = int(optimal_length)
    else:
        optimal_length = 8
    optimal_characters = optimal_characters_box.get()
    if website == "":
        return

    if not current_user == None:
        username = current_user.get_username()
        password = current_user.get_password()
        username_box.delete(0, 'end')
        username_box.insert(0, username)
        new_password_box.delete(0, 'end')
        new_password_box.insert(0, hashlib.md5(username + website + password).hexdigest()[0:optimal_length-len(optimal_characters)] + optimal_characters)
    else:
        username = random.choice(adjectives) + '_' + random.choice(nouns) + str(random.randint(0, 999))
        password = hashlib.md5(username + website).hexdigest()[0:optimal_length-len(optimal_characters)] + optimal_characters
        username_box.delete(0, 'end')
        username_box.insert(0, username)
        new_password_box.delete(0, 'end')
        new_password_box.insert(0,hashlib.md5(username + website + password).hexdigest()[0:optimal_length-len(optimal_characters)] + optimal_characters)


def copy_username_button_command():
    pass
    #pyperclip.copy(username_box.get())


def copy_new_password_button_command():
    pass
    #pyperclip.copy(new_password_box.get())

def store_website():
    if not current_user == None:
        website = url_box.get()
        optimal_length = optimal_length_box.get()
        if isint(optimal_length):
            optimal_length = int(optimal_length)
        else:
            optimal_length = 8
        optimal_characters = optimal_characters_box.get()
        if website == "":
            return
        current_user.add_website(website, optimal_length, optimal_characters)

def remove_website():
    if not current_user == None:
        pass

printable_chars = []
[printable_chars.append(chr(i)) for i in range(0,128)]

user_file = File_Reader('text.txt')
file_contents = user_file.read_file_data()
adjectives = (File_Reader('english-adjectives.txt').read_file_data()).split('\n')
nouns = (File_Reader('words_alpha.txt').read_file_data()).split('\n')
nouns = [noun[0:-1] for noun in nouns]

users = get_users() # All of the users in the text file
current_user = None

root = tk.Tk()
width = 400
height = 400
root.geometry("{}x{}".format(width, height))
root.title("Password Hider")
root.resizable(0, 0)

login_frame = Login_Frame(root, login_button, lambda: goto_frame(register_frame), lambda:goto_frame(main_frame), width, height)
register_frame = Register_Frame(root, register_button, lambda: goto_frame(login_frame), width, height)

comic_sans=('Comic Sans MS', 12, 'bold italic')
main_frame = tk.Frame(root, bg='grey25', width=width, height=height)
main_frame_title_label = tk.Label(main_frame, text='Enter Website URL', fg='white', bg='grey25', font=comic_sans)
main_frame_title_label.place(relx='0.5', rely='0.1', anchor='n')

url_box_label = tk.Label(main_frame, text="URL", fg='white', bg='grey25')
url_box_label.place(relx='0.5', rely='0.2', anchor='n')
url_box = tk.Entry(main_frame)
url_box.place(relx='0.5', rely='0.25', anchor='n')

saved_websites_menu = tk.Menu(main_frame)
#saved_websites_menu.place(relx=0.75, rely=0.25, anchor='n')

optimal_length_label = tk.Label(main_frame, text="Optimal Password Length", fg='white', bg='grey25')
optimal_length_label.place(relx='0.5', rely='0.3', anchor='n')
optimal_length_box = tk.Entry(main_frame)
optimal_length_box.place(relx='0.5', rely='0.35', anchor='n')

optimal_characters_label = tk.Label(main_frame, text="Password Characters", fg='white', bg='grey25')
optimal_characters_label.place(relx='0.5', rely='0.4', anchor='n')
optimal_characters_box = tk.Entry(main_frame)
optimal_characters_box.place(relx='0.5', rely='0.45', anchor='n')

create_login_button = tk.Button(main_frame, text='Create Login', fg='white', bg='grey25', command=create_login_button_command)
create_login_button.place(relx='0.5', rely='0.55', anchor='n')

username_box_label = tk.Label(main_frame, text='Username', fg='white', bg='grey25')
username_box_label.place(relx='0.5', rely='0.65', anchor='n')
username_box = tk.Entry(main_frame)
username_box.place(relx='0.5', rely='0.7', anchor='n')
copy_username_button = tk.Button(main_frame, text='Copy', fg='white', bg='grey25', command=copy_username_button_command)
copy_username_button.place(relx='0.75', rely='0.69', anchor='n')

new_password_box_label = tk.Label(main_frame, text='New Password', fg='white', bg='grey25')
new_password_box_label.place(relx='0.5', rely='0.75', anchor='n')
new_password_box = tk.Entry(main_frame)
new_password_box.place(relx='0.5', rely='0.8', anchor='n')
new_password_copy_button = tk.Button(main_frame, text='Copy', fg='white', bg='grey25', command=copy_new_password_button_command)
new_password_copy_button.place(relx='0.75', rely='0.79', anchor='n')

websites_menu = tk.OptionMenu(main_frame, tk.StringVar(), *['clubpenguin.com'], command=create_login_button_command)
add_website_button = tk.Button(main_frame, text='Store Website', command=store_website)
remove_website_button = tk.Button(main_frame, text='Remove Website', command=remove_website)

goto_frame(login_frame)

root.mainloop()
