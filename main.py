from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import json

from password import GeneratePassword

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password(): 
    generated_password = GeneratePassword().generated_password
    password_entry.delete(0,END)
    password_entry.insert(0, generated_password)
    password_entry.clipboard_clear()
    password_entry.clipboard_append(password_entry.get())

    messagebox.showinfo(title="You're welcome!!!", 
                        message="New password has been generated and copied to your clipboard")

# ---------------------------- SAVE PASSWORD ------------------------------- #
data_path = "data/data.json"

def upload_new_data(account, user_id, password, data):
    new_data = {
        account: {
            1: {
                "user_id" : user_id,
                "password": password,
            }
        }
    }

    if data:
        if account not in data:
            data.update(new_data)
        else:
            entry_numbers = [int(key) for key in list(data[account].keys())]
            entry_number = entry_numbers[-1]
            entry_number += 1
            data[account][entry_number] = {
                "user_id" : user_id,
                "password": password,
            }
    else:
        return new_data

def save():
    account = account_entry.get().lower()
    user_id = username_entry.get()
    password = password_entry.get()
    
    
    if account=="" or user_id=="" or password=="" :
        messagebox.showinfo(title="Something is missing!", message="You should know, None of the field can be empty ;)")
    
    else:
        confirmation = messagebox.askokcancel(title="A'ight, u sure bruh?", 
                            message=f"So, this is your account for '{account}',\n username/email: {user_id}\n password: {password}")

        if confirmation:   
            #Try to open .json file
            try:    
                with open(data_path, "r") as f:
                    data = json.load(f)
                    upload_new_data(account, user_id, password, data)
                    
                    #Sort the data
                    account_list = list(data.keys())
                    account_list.sort()
                    new_data = {account: data[account] for account in account_list}
                    data = new_data
                    
            #If there is no .json or no data in .json, then create a new one
            except (FileNotFoundError, json.JSONDecodeError):
                data = upload_new_data(account=account, user_id=user_id, password=password, data={})

            finally:  
                with open(data_path, "w") as f:      
                    json.dump(data, f, indent=4)
                  

            messagebox.showinfo(title="Noice!", message="Yup your account information has been saved!")
            
            account_entry.delete(0,END)
            username_entry.delete(0,END)
            password_entry.delete(0,END)

# ---------------------------- SHOW CREDENTIAL ------------------------------- #
def search_data():
    try:
        with open(data_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showinfo(title="No data", message="No data was stored!")
    else:
        popup = Toplevel(wd)
        popup.title('Stored credential')
        popup.resizable(width=False, height=False)
        popup.geometry(f'+{win_x+490}+{win_y}')

        '''Result '''
        result_label = Label(popup, text="Result list: ", bd=0)
        result_label.config(padx=20, pady=20)
        result_label.grid(row=0, column=2)

        result_list = Text(popup)
        result_list.insert(END, "Select Account")
        result_list.config(height=10, width=50)
        result_list.grid(row=1, column=2,sticky='ns')

        result_scrollbar = Scrollbar(popup, orient='vertical', command=result_list.yview)
        result_scrollbar.set = result_list['yscrollcommand']
        result_scrollbar.grid(
            column=3,
            row=1,
            sticky='ns')
        

        '''Account list'''
        account_label = Label(popup, text="Account list: ", bd=0)
        account_label.config(padx=20, pady=20)
        account_label.grid(row=0, column=0)
        
        #Account data
        account_data = list(data.keys())
        list_var = StringVar(value=account_data)

        account_list = Listbox(popup, height=20, selectmode='browse', listvariable=list_var)
        account_list.grid(row=1, column=0, sticky='ns')

        account_scrollbar = Scrollbar(popup, orient='vertical', command=account_list.yview)
        account_scrollbar.set = account_list['yscrollcommand']
        account_scrollbar.grid(
            column=1,
            row=1,
            sticky='ns')

        #Even handler
        def items_selected(event):
            result_list.config(state='normal')
            result_list.delete('1.0', END)
            selected_account = account_list.get(ANCHOR)
            result = data[selected_account]

            for keys in result.keys():
                first_part = f"Account no. {keys}:\n"
                second_part = f"    user_id = {result[keys]['user_id']}\n"
                third_part =  f"    password = {result[keys]['password']}\n\n"
                result_list.insert(END, first_part) 
                result_list.insert(END, second_part)
                result_list.insert(END, third_part)
            result_list.config(state='disabled')
        
        account_list.bind('<<ListboxSelect>>', items_selected)





# ---------------------------- UI SETUP ------------------------------- #
wd = Tk()
wd.title("Kuncung's Password Manager")
wd.resizable(width=False, height=False)
wd.config(padx = 50, pady = 50)
win_x = wd.winfo_rootx() + 300
win_y = wd.winfo_rooty() +200
wd.geometry(f'+{win_x}+{win_y}')


'''logo creation'''
canvas = Canvas(height=200, width=200)
logo = Image.open('padlock.png')
logo = logo.resize((150,150))
logo = ImageTk.PhotoImage(logo)
canvas.create_image( 100, 100, image=logo)
canvas.grid(row= 0, column= 1)
'''---------------------------------------------------------------------'''

'''First row'''
account_label = Label(text= "For accout: ", bd=0)
account_label.config(padx=30, pady= 30)
account_label.grid(row = 1, column = 0)

account_entry = Entry()
account_entry.grid(row= 1, column=1, sticky='ew')

#Search button
search_button = Button(text="Search", command=search_data)
search_button.grid(row = 1, column = 2, sticky='ew')

'''---------------------------------------------------------------------'''

'''Email/username row'''
username_label = Label(text= "Email / Username: ", bd=0)
username_label.grid(row = 2, column = 0)

username_entry = Entry()
username_entry.grid(row= 2, column=1, columnspan= 2, sticky='ew')
'''---------------------------------------------------------------------'''

'''Password row'''
password_label = Label(text= "Password: ", bd=0)
password_label.grid(row = 3, column = 0)

password_entry = Entry()
password_entry.grid(row= 3, column=1, sticky= 'ew')

generate_button = Button(text= "Generate Password", command= generate_password)
generate_button.grid(row=3, column= 2)
'''---------------------------------------------------------------------'''

'''Confirm row'''
confirm_button = Button(text= "Save credential", command= save)
confirm_button.grid(row=4, column= 1, columnspan=2, sticky='ew')
'''---------------------------------------------------------------------'''


wd.mainloop()