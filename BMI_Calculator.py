# Importing Library
import hashlib
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import json
import os

# Global login status and username
logged_in = False
current_user = None

# Hashing function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Checking user information (password hashed with hashlib)
def check_credentials(username, password):
    if os.path.exists("users.json"):
        with open("users.json", "r", encoding="utf-8") as file:
            users = json.load(file)
            for user in users:
                if user["username"] == username and user["password"] == hash_password(password):
                    return True
    return False

# Saving user (password hashed with hashlib)
def save_user(username, password, security_question, security_answer):
    users = []
    if os.path.exists("users.json"): # Checking if there is a file
        with open("users.json", "r", encoding="utf-8") as file:
            users = json.load(file)
    hashed_password = hash_password(password)
    users.append({
        "username": username,
        "password": hashed_password,
        "security_question": security_question,
        "security_answer": security_answer
    })
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

# Checking security answer
login_counter = 0
def check_security_answer(username, answer):
    global login_counter
    if os.path.exists("users.json"):
        with open("users.json", "r", encoding="utf-8") as file:
            users = json.load(file)
            for user in users:
                if user["username"] == username and user["security_answer"] == answer:
                    return True
    return False

password_counter = 0
time_counter = 0
cooldown_time = 0
time_of = 0
time_left = 0
# Login screen
def login_screen():
    global logged_in, current_user, time_counter, time_of
    login_window = Tk()
    login_window.title("Login")
    login_window.geometry("300x300")
    login_window.config(bg="black")

    Label(login_window, text="Username", bg="black", fg="white").pack(pady=5)
    username_entry = Entry(login_window)
    username_entry.pack(pady=5)

    Label(login_window, text="Password", bg="black", fg="white").pack(pady=5)
    password_entry = Entry(login_window, show="*")
    password_entry.pack(pady=5)

    time_label = Label(login_window, text="", bg="black", fg="white", font=("Arial", 7, "italic"))
    time_label.pack(pady=5)

    check_state = IntVar(value=0)

    def reset_cooldown_login():
        password_entry.config(state="normal")
        time_label.config(text="")
        messagebox.showinfo("Info", "Cooldown is over")
        checkbox.pack_forget()

    def update_counter():
        global time_left
        if time_left > 0:
            if check_state.get() == 1:
                display_time = ( time_left / 1000 ) // 60
                time_label.config(text=f"{display_time} minute(s) left")
            else:
                display_time = time_left / 1000
                time_label.config(text=f"{display_time} second(s) left")
            time_left -= 1000
            login_window.after(1000, update_counter)
        else:
            reset_cooldown_login()

    def login():
        global logged_in, current_user, password_counter, time_counter, cooldown_time, time_left

        if time_left > 0:
            messagebox.showwarning("Warning", f"Please wait {time_left} second(s) for cooldown")
            return

        if not password_counter == 3:
            username = username_entry.get()
            password = password_entry.get()

            if not username or not password:
                messagebox.showerror("Error", "Username and Password fields must be filled.")
                return
            if check_credentials(username, password):
                logged_in = True
                current_user = username
                messagebox.showinfo("Success", "Login successful!")
                login_window.destroy()
                password_counter = 0
            else:
                password_counter += 1
                if password_counter >= 3:
                    time_left = 300000 # 300 saniye
                    password_entry.config(state="disabled")
                    messagebox.showwarning("Warning", "5 Minutes Cooldown")
                    checkbox.pack(side=BOTTOM, pady=5)
                    update_counter()
                    password_counter = 0
                else:
                    messagebox.showerror("Error", f"Invalid username or password. Remaining attempts: {3 - password_counter}")
    checkbox = Checkbutton(login_window, text="Show time in minutes", variable=check_state, bg="black", fg="orange")
    checkbox.pack_forget()

    def register():
        register_window = Toplevel(login_window)
        register_window.title("Register")
        register_window.geometry("300x400")
        register_window.config(bg="black")

        Label(register_window, text="Username", bg="black", fg="white").pack(pady=5)
        reg_username_entry = Entry(register_window)
        reg_username_entry.pack(pady=5)

        Label(register_window, text="Password", bg="black", fg="white").pack(pady=5)
        reg_password_entry = Entry(register_window, show="*")
        reg_password_entry.pack(pady=5)

        Label(register_window, text="Security Question", bg="black", fg="white").pack(pady=5)
        security_question_entry = Entry(register_window)
        security_question_entry.pack(pady=5)

        Label(register_window, text="Security Answer", bg="black", fg="white").pack(pady=5)
        security_answer_entry = Entry(register_window)
        security_answer_entry.pack(pady=5)

        def save_registration():
            username = reg_username_entry.get()
            password = reg_password_entry.get()
            security_question = security_question_entry.get()
            security_answer = security_answer_entry.get()
            if username and password and security_question and security_answer:
                save_user(username, password, security_question, security_answer)
                messagebox.showinfo("Success", "Registration successful! Please login.")
                register_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        Button(register_window, text="Register", command=save_registration, bg="black", fg="white").pack(pady=10)

    def forgot_password():
        forgot_window = Toplevel(login_window)
        forgot_window.title("Forgot Password")
        forgot_window.geometry("300x300")
        forgot_window.config(bg="black")

        Label(forgot_window, text="Username", bg="black", fg="white").pack(pady=5)
        forgot_username_entry = Entry(forgot_window)
        forgot_username_entry.pack(pady=5)

        Label(forgot_window, text="Security Answer", bg="black", fg="white").pack(pady=5)
        forgot_answer_entry = Entry(forgot_window)
        forgot_answer_entry.pack(pady=5)

        def reset_password():
            username = forgot_username_entry.get()
            answer = forgot_answer_entry.get()

            if check_security_answer(username, answer):
                new_password_window = Toplevel(forgot_window)
                new_password_window.title("Set New Password")
                new_password_window.geometry("300x200")
                new_password_window.config(bg="black")

                Label(new_password_window, text="New Password", bg="black", fg="white").pack(pady=5)
                new_password_entry = Entry(new_password_window, show="*")
                new_password_entry.pack(pady=5)

                def save_new_password():
                    new_password = new_password_entry.get()
                    if new_password:
                        with open("users.json", "r", encoding="utf-8") as file:
                            users = json.load(file)
                        for user in users:
                            if user["username"] == username:
                                user["password"] = hash_password(new_password)
                                break
                        with open("users.json", "w", encoding="utf-8") as file:
                            json.dump(users, file, indent=4)
                        messagebox.showinfo("Success", "Password reset successful!")
                        new_password_window.destroy()
                        forgot_window.destroy()
                    else:
                        messagebox.showerror("Error", "Please enter a new password")

                Button(new_password_window, text="Save", command=save_new_password, bg="black", fg="white").pack(pady=10)
            else:
                messagebox.showerror("Error", "Invalid username or security answer.")


        Button(forgot_window, text="Reset Password", command=reset_password, bg="black", fg="white").pack(pady=10)

    def skip():
        login_window.destroy()
        main_screen()

    Button(login_window, text="Login", command=login, bg="black", fg="white").pack(side=LEFT, padx=10, pady=10)
    Button(login_window, text="Register", command=register, bg="black", fg="white").pack(side=RIGHT, padx=10, pady=10)
    Button(login_window, text="Forgot Password", command=forgot_password, bg="black", fg="white").pack(side=BOTTOM, padx=10, pady=10)
    Button(login_window, text="Skip", command=skip, bg="black", fg="white").pack(side=BOTTOM, padx=10, pady=10)

    login_window.mainloop()

counter = 0
user_data = []
user_specific_data = []
# Main screen
def main_screen():
    screen = Tk()
    screen.title("BMI Calculator")
    screen.config(background="black")
    screen.geometry("400x500")

    frame = Frame(screen, bg="black")
    frame.pack(fill=BOTH, expand=True)

    name_frame = Frame(frame, bg="black")
    name_frame.pack(pady=10)

    gender_frame = Frame(frame, bg="black")
    gender_frame.pack(pady=10)

    data_frame = Frame(frame, bg="black")
    data_frame.pack(pady=10)

    button_frame = Frame(frame, bg="black")
    button_frame.pack(pady=20)

    name_label = Label(name_frame, text="Name", bg="black", fg="white")
    name_label.grid(row=0, column=0, padx=10, pady=5)
    name_entry = Entry(name_frame, width=15)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    surname_label = Label(name_frame, text="Surname", bg="black", fg="white")
    surname_label.grid(row=1, column=0, padx=10, pady=5)
    surname_entry = Entry(name_frame, width=15)
    surname_entry.grid(row=1, column=1, padx=10, pady=5)

    age_label = Label(name_frame, text="Age", bg="black", fg="white")
    age_label.grid(row=2, column=0, padx=10, pady=5)
    age_entry = Entry(name_frame, width=15)
    age_entry.grid(row=2, column=1, padx=10, pady=5)

    weight_label = Label(data_frame, text="Enter Your Weight (KG)", bg="black", fg="white")
    weight_label.grid(row=0, column=0, padx=10, pady=5)
    weight_entry = Entry(data_frame, width=15)
    weight_entry.grid(row=0, column=1, padx=10, pady=5)

    height_label = Label(data_frame, text="Enter Your Height (cm)", bg="black", fg="white")
    height_label.grid(row=1, column=0, padx=10, pady=5)
    height_entry = Entry(data_frame, width=15)
    height_entry.grid(row=1, column=1, padx=10, pady=5)

    radio_state = StringVar()
    gender_radio_male = Radiobutton(gender_frame, text="Male", value="Male", variable=radio_state, bg="black", fg="blue")
    gender_radio_male.pack(side=LEFT, padx=10)
    gender_radio_female = Radiobutton(gender_frame, text="Female", value="Female", variable=radio_state, bg="black", fg="purple")
    gender_radio_female.pack(side=LEFT, padx=10)

    counter = 0
    user_data = []

    def load_counter():
        global counter, user_data
        if os.path.exists("user_data.json"):
            try:
                with open("user_data.json", "r", encoding="utf-8") as file:
                    user_data = json.load(file)
                if user_data:
                    counter = max(item["Id"] for item in user_data) if user_data else 0
            except (json.JSONDecodeError, FileNotFoundError):
                counter = 0
        else:
            counter = 0

    load_counter()

    def calculate_bmi():
        try:
            name = str(name_entry.get())
            surname = str(surname_entry.get())
            age = int(age_entry.get())
            height = int(height_entry.get()) / 100
            weight = int(weight_entry.get())
            gender = radio_state.get()

            if not name or not surname:
                messagebox.showinfo("Info", "Please fill in both name and surname.")
                return
            if height < 1 or height > 3:
                messagebox.showinfo("Info", "Please enter a valid height.")
                return
            if age < 19:
                messagebox.showinfo("Info", "Age under 19 is not accepted!")
                return

            bmi = int((weight / (height * height)))
            if bmi <= 20:
                bmi_category = "Underweight"
                color = "#3498db"
            elif 20 < bmi <= 25:
                bmi_category = "Normal"
                color = "#2ecc71"
            elif 25 < bmi <= 30:
                bmi_category = "Overweight"
                color = "#f1c40f"
            elif 30 < bmi <= 35:
                bmi_category = "Obese"
                color = "#e67e22"
            else:
                bmi_category = "Severely Obese"
                color = "#e74c3c"

            if 19 <= age <= 24:
                ideal_bmi = "19-24"
            elif 25 <= age <= 34:
                ideal_bmi = "20-25"
            elif 35 <= age <= 44:
                ideal_bmi = "21-26"
            elif 45 <= age <= 54:
                ideal_bmi = "22-27"
            elif 55 <= age <= 65:
                ideal_bmi = "23-28"
            else:
                ideal_bmi = "24-29"

            result_window = Toplevel(screen)
            result_window.title("BMI Result")
            result_window.geometry("400x300")
            result_window.config(bg=color)

            result_label = Label(result_window, text=f"Name: {name}\nSurname: {surname}\nAge: {age}\nGender: {gender}\nBMI: {bmi} >> {bmi_category}\nIdeal BMI: {ideal_bmi}", bg=color, font=("Arial", 14), fg="white")
            result_label.pack(padx=20, pady=20)

            def save_history():
                global logged_in, counter, user_data, current_user
                if not logged_in:
                    if messagebox.askyesno("Question", "You need to be logged in to save your BMI data.Do you want to register?"):
                        result_window.destroy()
                        screen.destroy()
                        login_screen()
                    else:
                        result_window.destroy()
                    return
                counter += 1
                new_user = {
                    "Id": counter,
                    "Username": current_user,
                    "Name": name,
                    "Surname": surname,
                    "Age": age,
                    "Gender": gender,
                    "BMI": bmi,
                    "BMI Category": bmi_category,
                    "Ideal BMI": ideal_bmi,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                user_data.append(new_user)
                with open("user_data.json", "w", encoding="utf-8") as data:
                    json.dump(user_data, data, ensure_ascii=False, indent=4)
                messagebox.showinfo("Success", "User data saved")
                result_window.destroy()

            save_button = Button(result_window, text="Save", command=save_history, bg="black", fg="green")
            save_button.pack(side=RIGHT, padx=10, pady=10)
            back_button = Button(result_window, text="Back", command=result_window.destroy, bg="black", fg="white")
            back_button.pack(side=LEFT, padx=10, pady=10)

            name_entry.delete(0, END)
            surname_entry.delete(0, END)
            age_entry.delete(0, END)
            weight_entry.delete(0, END)
            height_entry.delete(0, END)

        except ValueError:
            messagebox.showerror("Error", "Please fill in all fields")

    def history_screen():
        global user_data, current_user, user_specific_data
        if not logged_in:
            messagebox.showwarning("Warning", "You need to be logged in to view history.")
            return
        user_specific_data = [data for data in user_data if data["Username"] == current_user]
        if not user_specific_data:
            messagebox.showinfo("Info", "No records found for this user.")
            return
        history_window = Toplevel(screen)
        history_window.title("User History")
        history_window.geometry("400x300")
        history_window.config(bg="black")

        history_listbox = Listbox(history_window, bg="black", fg="white", width=50)
        for data in user_specific_data:
            history_listbox.insert(END, f"ID: {data['Id']}, Name: {data['Name']}, Surname: {data['Surname']}")
        history_listbox.pack()

        # Delete User
        delete_user_id = Label(history_window, text="ID number of the person you want to delete", font=("Verdana", 7, "italic"), bg="black", fg="white")
        delete_user_id.pack()

        delete_user_entry = Entry(history_window, bg="white", fg="black")
        delete_user_entry.pack()

        def delete_user_with_id():
            id_to_delete = delete_user_entry.get()
            if not id_to_delete:
                messagebox.showerror("Error", "Please enter a valid ID.")
                return

            try:
                id_to_delete = int(id_to_delete)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric ID.")
                return

            global user_data
            original_length = len(user_data)
            user_data = [shadow_data for shadow_data in user_data if shadow_data["Id"] != id_to_delete]

            with open("user_data.json", "w", encoding="utf-8") as file:
                json.dump(user_data, file, indent=4)

            if len(user_data) < original_length:
                messagebox.showinfo("Successfully", f"ID {id_to_delete} has been deleted.")
            else:
                messagebox.showerror("Error", "User not found")
            history_window.destroy()

        def listbox_selected(_):
            selected_index = history_listbox.curselection()
            if not selected_index:
                return
            selected_text = history_listbox.get(selected_index)
            selected_id = int(selected_text.split(",")[0].split(":")[1].strip())
            selected_user = next((d for d in user_specific_data if d["Id"] == selected_id), None)
            if selected_user:
                user_info = f"ID: {selected_user['Id']}\nName: {selected_user['Name']}\nSurname: {selected_user['Surname']}\nAge: {selected_user['Age']}\nGender: {selected_user['Gender']}\nBMI: {selected_user['BMI']}\nBMI Category: {selected_user['BMI Category']}\nIdeal BMI: {selected_user['Ideal BMI']}\nTimestamp: {selected_user['Timestamp']}"
                messagebox.showinfo("User Info", user_info)

        history_listbox.bind('<<ListboxSelect>>', listbox_selected)
        back_button = Button(history_window, text="Back", command=history_window.destroy, bg="black", fg="white")
        back_button.pack(pady=10)

        # Delete Button
        delete_user_button = Button(history_window, text="Delete", bg="black", fg="red", command=delete_user_with_id)
        delete_user_button.pack(pady=10)

    def reset_data():
        global counter, user_data
        if messagebox.askyesno("Reset Data", "All data will be deleted. Are you sure?"):
            if os.path.exists("user_data.json"):
                with open('user_data.json', 'r', encoding='utf-8') as file:
                    user_data = json.load(file)

                user_data = [data for data in user_data if data["Username"] != current_user]

                with open("user_data.json", "w", encoding="utf-8") as file:
                    json.dump(user_data, file, indent=4)

                messagebox.showinfo("Reset", "Your data has been reset")
            else:
                messagebox.showinfo("Info", "No data found to reset")
    # Buttons
    calculate_button = Button(button_frame, text="Calculate", command=calculate_bmi, bg="black", fg="white")
    calculate_button.pack(side=LEFT, padx=10, pady=5)
    history_button = Button(button_frame, text="History", command=history_screen, bg="black", fg="white")
    history_button.pack(side=LEFT, padx=10, pady=5)
    reset_button = Button(button_frame, text="Reset Data", command=reset_data, bg="black", fg="red")
    reset_button.pack(side=LEFT, padx=10, pady=5)
    exit_button = Button(button_frame, text="Exit", command=screen.quit, bg="black", fg="white")
    exit_button.pack(side=LEFT, padx=10, pady=5)

    screen.mainloop()

# Start the application
login_screen()
main_screen()