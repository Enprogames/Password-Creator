import tkinter as tk
#import pyperclip
import string
import hashlib
import base64
import os


class Login_Frame(tk.Frame):

    def __init__(self, parent, login_function, goto_register_function, width=600, height=400):
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
        self.changetoregisterbutton.place(relx=.43, rely=.85, anchor="center")

        self.loginbutton = tk.Button(self, text="login", font=('consolas', 10, 'bold'), bg="white", fg="black", command=login_function)
        self.loginbutton.place(relx=.58, rely=.85, anchor="center")


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
        self.registerusernamebox.insert(0, "xXBroccoliLoverXx")  # temporary for debugging

        self.registerpasswordlabel = tk.Label(self, text="Password", font=('consolas', 10, 'bold'), bg="grey25",
                                         fg="white")
        self.registerpasswordlabel.place(relx=.5, rely=.5, anchor="center")
        self.registerpasswordbox = tk.Entry(self)
        self.registerpasswordbox.place(relx=.5, rely=.55, anchor="center")
        self.registerpasswordbox.insert(0, "p2ssw0rd1")  # temporary for debugging

        self.confirmpasswordlabel = tk.Label(self, text="Confirm Password", font=('consolas', 10, 'bold'),
                                        bg="grey25", fg="white")
        self.confirmpasswordlabel.place(relx=.5, rely=.6, anchor="center")
        self.confirmpasswordbox = tk.Entry(self, width="20")
        self.confirmpasswordbox.place(relx=.5, rely=.65, anchor="center")
        self.confirmpasswordbox.insert(0, "p2ssw0rd1")  # temporary for debugging

        self.registerbutton = tk.Button(self, text="register", font=('consolas', 10, 'bold'), bg="white",
                                   fg="black", command=register_function)
        self.registerbutton.place(relx=.43, rely=.85, anchor="center")

        self.changetologinbutton = tk.Button(self, text="login", font=('consolas', 10, 'bold'), bg="white",
                                        fg="black", command=goto_login_function)
        self.changetologinbutton.place(relx=.58, rely=.85, anchor="center")


class File_Reader:
    def __init__(self, url):
        self.url = url

    def read_file_data(self):
        file = open(self.url, 'r', encoding='utf-8')
        contents = base64.b64decode(file.read()).decode('utf-8')
        #print(contents)
        file.close()
        if len(contents) == 0: return ""
        return contents

    def write_file_data(self, data):
        file = open(self.url, 'w', encoding='utf-8')
        #print(data, base64.b64encode(data))
        file.write(base64.b64encode(data.encode('utf-8')).decode('utf-8'))
        file.close()

    def append_line_file_data(self, data):
        contents = self.read_file_data()
        data = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        file = open(self.url, 'a', encoding='utf-8')
        if self.read_file_data() == None:
            file.write(data)
        else:
            file.write(base64.b64encode((contents + '\n' + data).encode('utf-8')).decode('utf-8'))
        file.close


class User:
    def __init__(self, username, password, websites = None):
        self.username = username  # encrypted username
        self.password = password  # hashed password
        self.websites = websites  # list of website data lists
        if self.websites == []:
            self.websites = None

    def new_password(self, website):
        if website in self.websites:
            pass
        return hashlib.md5(self.username + self.password + website)

    def get_username(self):
        return simple_decrypt(self.username)

    def __str__(self):
        return "Username: " + self.username + " Password: " + self.password + " Websites: " + str(self.websites)

    def encrypted_data(self):
        if self.websites is None:
            return str(simple_encrypt(self.username) + ', ' + hashlib.md5(self.password.encode('utf-8')).hexdigest())
        else:
            raw_website_data = "" # data in the websites as a string
            for website in self.websites: # loops through the array containing the data for the websites
                if len(website) == 1:
                    raw_website_data += website
                    print(website)

            return str(simple_encrypt(self.username) + ', ' + hashlib.md5(self.password.encode('utf-8')).hexdigest() + ' ,')
            

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
    if not file_contents == None:
        for i in range(len(file_contents.split('\n'))):  # loops through each line in file
            users.append([])
            for item in file_contents.split('\n')[i].split(','):
                if not '[' in item:
                    users[i].append(item.strip())
                else:
                    website_args = file_contents.split('\n')[i][file_contents.split('\n')[i].index(item) + 2:-1].split(',')
                    website_args = [x.strip() for x in website_args]
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
            output.append(User(username, password, websites))
        return output
    else:
        return []


def simple_encrypt(x):
    x = list(str(x))
    output = ""
    for i in x:
        num = str(printable_chars.index(i))
        if len(num) == 1:
            output += '00' + num
        elif len(num) == 2:
            output += '0' + num
        else:
            output += num
    return output


def simple_decrypt(x):
    output = ""
    a = []
    for i in range(len(x)):
        if i % 3 == 0 and i > 0:
            a.append(x[i-3:i])
    for i in a:
        output += printable_chars[int(i)]
    return output


def goto_frame(frame):
    login_frame.pack_forget()
    register_frame.pack_forget()
    main_frame.pack_forget()
    frame.pack()


def login_button():
    username = login_frame.usernamebox.get()
    password = login_frame.passwordbox.get()

    goto_frame(main_frame)


def add_to_file(user_to_append):
    text_file.append_line_file_data(user_to_append.encrypted_data())


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
        register_frame.registermessagelabel.config(text='user already exists', fg='grey25')
        for user in users:
            if simple_decrypt(user.username) == username and user.password == hashlib.md5(password.encode('utf-8')).hexdigest():

                register_frame.registermessagelabel.config(fg='white')
                return # ends function if user exists

        current_user = User(username, password)
        users.append(current_user)
        goto_frame(main_frame)
        add_to_file(current_user)
        print(current_user)
        #print(current_user.encrypted_data())

def create_login_button():

    username = current_user.get_username()
    website = url_box.get()
    password = current_user.new_password(website)
    print(username)


def copy(s):
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        subprocess.Popen(['clip'], stdin=subprocess.PIPE).communicate(s)
    else:
        raise Exception('Platform not supported')


def copy_username_button_command():
    #pyperclip.copy(username_box.get())
    copy(s)
    os.system("echo '{}' | xclip -selection clipboard".format(username_box.get()))


def copy_new_password_button_command():
    #pyperclip.copy(new_password_box.get())
    os.system("echo '{}' | xclip -selection clipboard".format(new_password_box.get()))


printable_chars = []
[printable_chars.append(chr(i)) for i in range(0,128)]

text_file = File_Reader('text.txt')
file_contents = text_file.read_file_data()

users = get_users() # All of the users in the text file
current_user = None

root = tk.Tk()
width = 400
height = 400
root.geometry("{}x{}".format(width, height))
root.title("Password Hider")

login_frame = Login_Frame(root, login_button, lambda: goto_frame(register_frame), width, height)
register_frame = Register_Frame(root, register_button, lambda: goto_frame(login_frame), width, height)

comic_sans=('Comic Sans MS', 12, 'bold italic')
main_frame = tk.Frame(root, bg='grey25', width=width, height=height)
main_frame_title_label = tk.Label(main_frame, text='Enter Website URL\n', fg='white', bg='grey25', font=comic_sans)
main_frame_title_label.place(relx='0.5', rely='0.1', anchor='n')

url_box_label = tk.Label(main_frame, text="URL", fg='white', bg='grey25')
url_box_label.place(relx='0.5', rely='0.3', anchor='n')
url_box = tk.Entry(main_frame)
url_box.place(relx='0.5', rely='0.35', anchor='n')

create_login_button = tk.Button(main_frame, text='Create Login', fg='white', bg='grey25')
create_login_button.place(relx='0.5', rely='0.45', anchor='n')

username_box_label = tk.Label(main_frame, text='Username', fg='white', bg='grey25')
username_box_label.place(relx='0.5', rely='0.55', anchor='n')
username_box = tk.Entry(main_frame)
username_box.place(relx='0.5', rely='0.6', anchor='n')
copy_username_button = tk.Button(main_frame, text='Copy', fg='white', bg='grey25', command=copy_username_button_command)
copy_username_button.place(relx='0.75', rely='0.59', anchor='n')

new_password_box_label = tk.Label(main_frame, text='New Password', fg='white', bg='grey25')
new_password_box_label.place(relx='0.5', rely='0.65', anchor='n')
new_password_box = tk.Entry(main_frame)
new_password_box.place(relx='0.5', rely='0.7', anchor='n')
new_password_copy_button = tk.Button(main_frame, text='Copy', fg='white', bg='grey25', command=copy_new_password_button_command)
new_password_copy_button.place(relx='0.75', rely='0.69', anchor='n')


goto_frame(login_frame)

root.mainloop()