from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
from pyperclip import copy
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generates random password with numbers, characters and symbols
    and copies the generated password to the clipboard"""

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for letter in range(randint(8, 10))]
    password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    password_numbers = [choice(numbers) for number in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    copy(password)


def find_password():
    website = website_entry.get()
    try:
        with open("data.json", 'r') as data_file:
            # Reading old data
            data = json.load(data_file)
            if website in [key for key in data]:
                messagebox.showinfo(title=website, message=f'{data[website]["email"]}\n{data[website]["password"]}')
            else:
                messagebox.showerror(title="Oops", message="No details for the website exists")
    except:
        messagebox.showerror(title="Oops", message="No Data File Found")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """Saves the password data into a text file in the project folder"""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields blank!")
    else:
        try:
            with open("data.json", 'r') as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", 'w') as data_file:
                # Creating new data
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", 'w') as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo1.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:", font=("Arial", 12, "bold"))
website_label.grid(column=0, row=1)
website_entry = Entry(width=30)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_label = Label(text="Email/Username:", font=("Arial", 12, "bold"))
email_label.grid(column=0, row=2)
email_entry = Entry(width=50)
email_entry.grid(columnspan=2, column=1, row=2)
email_entry.insert(0, "aakasaramann")
''' inserts default username that is stored as system environment variable.
You can just replace the entire second argument with your default username/email'''

password_label = Label(text="Password:", font=("Arial", 12, "bold"))
password_label.grid(column=0, row=3)
password_entry = Entry(width=30)
password_entry.grid(column=1, row=3)

search_button = Button(text="Search", command=find_password, font=("Arial", 8, "bold"), width=16)
search_button.grid(column=2, row=1)

generate_button = Button(text="Generate Password", command=generate_password, font=("Arial", 8, "bold"), width=16)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=42, command=save)
add_button.grid(columnspan=2, column=1, row=4)

window.mainloop()
