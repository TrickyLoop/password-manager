# PASSWORD MANAGER by TrickyLoop

from tkinter import *
from random import choice, randint, shuffle
from tkinter import messagebox
import json
import pyperclip


# Updates (04/28/26):
# Implemented JSON file
# Implemented Exception Handling
# Implemented Search Function for searching existing entry

# ---------------------------- OTHER FUNCTIONS ------------------------------- #
def read_json_file():
    with open("output/data.json", mode="r") as data_file:
        # Reading old data
        return json.load(data_file)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters = [choice(letters) for _ in range(randint(8, 10))]
    symbols = [choice(symbols) for _ in range(randint(2, 4))]
    numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letters + symbols + numbers
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    #Get data from entries
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please enter both fields")
    else:
        try:
            data = read_json_file()
        except FileNotFoundError:
            with open("output/data.json", mode="w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("output/data.json", mode="w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            # Reset Entry
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND ENTRY ------------------------------- #
def find_password():
    try:
        data = read_json_file()
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No Data File Found")
    else:
        website = website_entry.get()
        email = ""
        password = ""
        try:
            if website in list(data.keys()):
                email = data[website]["email"]
                password = data[website]["password"]
            else:
                raise KeyError
        except KeyError:
            messagebox.showinfo(title="Oops", message="No details for the website exists")
        else:
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    finally:
        website_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager by TrickyLoop")
window.config(padx=50, pady=50)

#Logo
canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="assets/logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=0, columnspan=3)

#Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky=E)

email_or_username_label = Label(text="Email / Username:")
email_or_username_label.grid(row=2, column=0, sticky=E)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky=E)

#Entries
website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(row=1, column=1, sticky=EW)

email_entry = Entry(width=35)
email_entry.insert(0, "username@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2, sticky=EW)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky=EW)

#Buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky=EW)

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2, sticky=EW)

add_button = Button(text="Add", width=32, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky=EW)

window.mainloop()