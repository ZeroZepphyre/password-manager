from tkinter import *
from tkinter import messagebox
import json
from pass_gen import pass_return
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def random_pass():
    password = pass_return()
    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def clear_entries():
    site_input.delete(0, END)
    password_input.delete(0, END)
    address_input.delete(0, END)


def search_data():
    try:
        with open('passwords.json', 'r') as data_file:
            data = json.load(data_file)
            try:
                messagebox.showinfo(f"{site_input.get()}", f" e-mail: {data[site_input.get()]['email']}\n password: {data[site_input.get()]['password']}")
                password_input.insert(0, data[site_input.get()]['password'])
            except KeyError:
                messagebox.showinfo("Invalid website", f'"{site_input.get()}" not found, try a different site.')
    except FileNotFoundError:
        messagebox.showinfo("Data File not Found", "There is no data file saved in this machine.")


def save_file():
    site = site_input.get()
    email = address_input.get()
    password = password_input.get()
    new_data = {site: {'email': email, 'password': password}}
    if site == '' or email == '' or password == '':
        popup = Toplevel(window)
        popup.title('Missing something?')
        popup.config(padx=20, pady=20)
        warning_label = Label(popup, text='You are missing some data, try again.')
        warning_label.pack()
    else:
        try:
            with open("passwords.json", 'r') as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            # Cria um Json caso não exista.
            with open("passwords.json", 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("passwords.json", 'w') as data_file:
                json.dump(data, data_file, indent=4)
        clear_entries()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('myPass')
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

site_label = Label(text='Website:')
site_label.grid(row=1, column=0, sticky='e')
site_input = Entry(width=32)
site_input.grid(row=1, column=1, columnspan=2, sticky='w')
site_input.focus()

address_label = Label(text='E-mail:')
address_label.grid(row=2, column=0, sticky='e')
address_input = Entry(width=52)
address_input.grid(row=2, column=1, columnspan=2, sticky='w')

password_label = Label(text='Password:')
password_label.grid(row=3, column=0, sticky='e')
password_input = Entry(width=32)
password_input.grid(row=3, column=1, sticky='w')

random_pass_button = Button(text='Generate Password', command=random_pass)
random_pass_button.grid(row=3, column=2, sticky='w')

add_button = Button(text='Add', width=44, command=save_file)
add_button.grid(row=4, column=1, columnspan=2, sticky='w')

search_button = Button(text='Search', command=search_data)
search_button.grid(row=1, column=2, sticky='w')


window.mainloop()
