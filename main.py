from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0,END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    chars_list = [random.choice(letters) for j in range(nr_letters)]
    numbers_list = [random.choice(numbers) for i in range(nr_numbers)]
    symbols_list = [random.choice(symbols) for j in range(nr_symbols)]

    password_list = chars_list + numbers_list + symbols_list
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_entry():
    email = email_username_entry.get()
    passw = password_entry.get()
    website = website_entry.get()
    pass_dict = {
        website:
            {"email": email,
             "password": passw
             }
    }
    if len(email) == 0 or len(passw) == 0 or len(website) ==0:
        messagebox.showinfo(message="One or more fields are empty")
    else:
        continyou = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}\nPassword:{passw}")
        if continyou:
            try:
                with open("passwords.json", "r") as pswfile:
                    loaded_pass = json.load(pswfile)
                    loaded_pass.update(pass_dict)
            except FileNotFoundError:
                with open("passwords.json","w") as pswfile:
                    # pswfile.write(f"{email} | {passw} | {website} \n")
                    json.dump(pass_dict, pswfile, indent=4)
                    pswfile.close()
            else:
                with open("passwords.json", "w") as pswfile:
                    json.dump(loaded_pass, pswfile, indent=4)
            finally:
                pswfile.close()
                password_entry.delete(0,END)
                website_entry.delete(0,END)
                messagebox.showinfo(message= "Credentials Saved.")


# ---------------------------- FIND PASSWORD ------------------------------- #
def search_password():
    website = website_entry.get()
    try:
        with open("passwords.json", "r") as pswfile:
            loaded_pass = json.load(pswfile)
    except FileNotFoundError:
        messagebox.showinfo(title = "Error", message="No Password File Exists")
    else:
        if website not in loaded_pass:
            messagebox.showinfo(title = "Error",message="Website Not Found")

        else:
            password = loaded_pass[website]["password"]
            email = loaded_pass[website]["email"]
            messagebox.showinfo(message=f"Website: {website}\nEmail:{email}\nPassword: {password}")
    finally:
        pswfile.close()






# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(window, height=202, width=191)
img = PhotoImage(file="logo.png")
image = canvas.create_image(100,95, image=img)
canvas.grid(column=1,row=0)
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_entry = Entry(width=31)
website_entry.grid(column=1,row=1)
website_entry.focus()
website_search = Button(text="Search", width=15, command=search_password)
website_search.grid(column=2, row=1)
email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)
email_username_entry = Entry(width=50)
email_username_entry.grid(column=1,row=2,columnspan=2)
email_username_entry.insert(0,"dummyemail@gmail.com")
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_entry = Entry(width=31)
password_entry.grid(column=1,row=3)
generate_pass = Button(text="Generate Password", command=generate_password)
generate_pass.grid(column=2,row=3)
add_btn = Button(text="Add", width=44, command=save_entry)
add_btn.grid(column=1, row=4, columnspan=2)
window.mainloop()