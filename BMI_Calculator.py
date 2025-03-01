#Importing Library
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import turtle
import json
import os

#Opening Screen With Turtle Library

#Screen
open_screen = turtle.Screen()
open_screen.bgcolor("black")

#Turtles
star = turtle.Turtle()
star.color("yellow")
star.speed(0)

star2 = turtle.Turtle()
star.color("yellow")
star.speed(0)

#Turtle Movements
def draw_star(size):
    for _ in range(5):
        star.forward(size)
        star.right(144)
        star2.forward(size)
        star2.right(144)

star.penup()
star.goto(-50, 0)
star.pendown()
draw_star(100)

star2.penup()
star2.goto(-50, 0)
star2.pendown()
draw_star(100)

#Screen and Turtle Closing
star.hideturtle()
turtle.bye()

# Screen
screen = Tk()
screen.title("BMI Calculator")
screen.config(background="black")
screen.geometry("400x500")


# Define Frame for Layout
frame = Frame(screen, bg="black")
frame.pack(fill=BOTH, expand=True)

# Logo
try:
    logo_img = PhotoImage(file="bmi_logo.png")
    logo_label = Label(frame, image=logo_img, bg="black")
    logo_label.pack(pady=10)
except Exception as e:
    print("Logo uninstalled", e)

# Name Section
name_frame = Frame(frame, bg="black")
name_frame.pack(pady=10)

# Gender Section
gender_frame = Frame(frame, bg="black")
gender_frame.pack(pady=10)

# Weight and Height Section
data_frame = Frame(frame, bg="black")
data_frame.pack(pady=10)

# Calculate Button Section
calculate_button_frame = Frame(frame, bg="black")
calculate_button_frame.pack(pady=20)

# Save History Button Frame Section
save_history_frame = Frame(frame, bg="black")
save_history_frame.pack(pady=20)


#Labels
username_label = Label(name_frame, text="Name", bg="black", fg="white")
username_label.grid(row=0, column=0, padx=10, pady=5)
username_entry = Entry(name_frame, width=15)
username_entry.grid(row=0, column=1, padx=10, pady=5)

surname_label = Label(name_frame, text="Surname", bg="black", fg="white")
surname_label.grid(row=1, column=0, padx=10, pady=5)
surname_entry = Entry(name_frame, width=15)
surname_entry.grid(row=1, column=1, padx=10, pady=5)

age_label = Label(name_frame, text="Age", bg="black", fg="white")
age_label.grid(row=2, column=0, padx=10, pady=5)
age_entry = Entry(name_frame, width=15)
age_entry.grid(row=2, column=1, padx=10, pady=5)

kg_label = Label(data_frame, text="Enter Your KG", bg="black", fg="white")
kg_label.grid(row=0, column=0, padx=10, pady=5)
kg_entry = Entry(data_frame, width=15)
kg_entry.grid(row=0, column=1, padx=10, pady=5)

boy_label = Label(data_frame, text="Enter Your Size(cm)", bg="black", fg="white")
boy_label.grid(row=1, column=0, padx=10, pady=5)
boy_entry = Entry(data_frame, width=15)
boy_entry.grid(row=1, column=1, padx=10, pady=5)

#RadioButton for Gender
radio_state = StringVar()

#Male
genderRadio = Radiobutton(gender_frame, text="Male", value="Male", variable=radio_state, bg="black", fg="white")
genderRadio.pack(side=LEFT, padx=10)

#Female
genderRadio2 = Radiobutton(gender_frame, text="Female", value="Female", variable=radio_state, bg="black", fg="white")
genderRadio2.pack(side=LEFT, padx=10)

counter = 0 # counter for registration id
user_data = []

def load_counter():
    global counter, user_data
    if os.path.exists("user_data.json"):
        try:
            with open("user_data.json", "r", encoding="utf-8") as file:
                user_data = json.load(file)
            if user_data:
                counter = max(item["Id"] for item in user_data)
            else:
                counter = 0
        except (json.JSONDecodeError, FileNotFoundError):
            counter = 0
    else:
        counter = 0

load_counter()

def reset_data():
    global counter, user_data
    if messagebox.askyesno("Reset Data", "All data will be deleted. Are you sure?"):
        if os.path.exists("user_data.json"):
            os.remove("user_data.json")
        user_data = []
        counter = 0
        messagebox.showinfo("Reset", "All data has been reset.")

def button_selected():
    try:
        # Value Assignments
        username = str(username_entry.get())
        surname = str(surname_entry.get())
        age_value = int(age_entry.get())
        boy_value = int(boy_entry.get()) / 100
        kg_value = int(kg_entry.get())
        gender = radio_state.get()

        #Errors
        if username == "" or surname == "":
            messagebox.showinfo("Info", "Please fill in both username and surname.")
            return
        if boy_value < 1 or boy_value > 3:
            messagebox.showinfo("Info", "Please enter a valid height.")
            return
        if age_value <19:
            messagebox.showinfo("Info", "Age under 19 is not accepted!")
            return

        # BMI Calculation
        bmi = int((kg_value / (boy_value * boy_value)))

        # BMI Categories
        if bmi <= 20:
            bmi_name = "Underweight"
            color = "#3498db"
        elif 20 < bmi <= 25:
            bmi_name = "Normal"
            color = "#2ecc71"
        elif 25 < bmi <= 30:
            bmi_name = "Overweight"
            color = "#f1c40f"
        elif 30 < bmi <= 35:
            bmi_name = "Obese"
            color = "#e67e22"
        else:
            bmi_name = "Severely Obese"
            color = "#e74c3c"

        # Ideal BMI
        if 19 <= age_value <= 24:
            ideal_bmi = "19-24"
        elif 25 <= age_value <= 34:
            ideal_bmi = "20-25"
        elif 35 <= age_value <= 44:
            ideal_bmi = "21-26"
        elif 45 <= age_value <= 54:
            ideal_bmi = "22-27"
        elif 55 <= age_value <= 65:
            ideal_bmi = "23-28"
        else:
            ideal_bmi = "24-29"


        def data_add(add_user):
            global user_data
            if os.path.exists("user_data.json"):
                try:
                    with open("user_data.json", "r", encoding="utf-8") as file:
                        user_data = json.load(file)
                except (json.JSONDecodeError, FileNotFoundError):
                    user_data = []
            else:
                user_data = []

            user_data.append(add_user)

            with open("user_data.json", "w", encoding="utf-8") as data:
                json.dump(user_data, data, ensure_ascii=False, indent=4)  # type: ignore
            messagebox.showinfo("successfully","User data saved")

            result_window.destroy()

        def saving_history():
            global counter
            counter += 1
            global user_data
            new_user = \
            {
                "Id": counter,
                "Name": username,
                "Surname": surname,
                "Age": age_value,
                "Gender": gender,
                "BMI": bmi,
                "BMI Categories": bmi_name,
                "Ideal BMI": ideal_bmi,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            data_add(new_user)


        username_entry.delete(0, END)
        surname_entry.delete(0, END)
        age_entry.delete(0, END)

        kg_entry.delete(0, END)
        boy_entry.delete(0, END)

        #2nd Screen so result window
        result_window = Toplevel(screen)
        result_window.title("BMI Result Window")
        result_window.geometry("400x300")
        result_window.config(bg=color)

        #Info screen
        result_label = Label(result_window, text=f"Name: {username}\nSurname: {surname}\nAge: {age_value}\nGender: {gender}\nBMI: {bmi} >> {bmi_name}\nIdeal BMI: {ideal_bmi}", bg=color, font=("Arial", 14), anchor="w", fg="white")
        result_label.pack(padx=20, pady=20)

        #Saving History Button
        save_history_button = Button(result_window, text="Save", command=saving_history, bg="black", fg="green")
        save_history_button.pack(side=RIGHT, padx=10, pady=10)

        #BACK and EXIT screen
        back_button = Button(result_window, text="Back", command=result_window.destroy, bg="black", fg="white")
        back_button.pack(side=LEFT, padx=10, pady=10)

    except ValueError:
        messagebox.showerror("Error", "Empty spaces need to be filled")


def history_screen():
    global user_data
    if not user_data:
        messagebox.showinfo("Bilgi", "No registered users yet!")
        return
    else:
        history_window = Toplevel(screen)
        history_window.title("Users History")
        history_window.geometry("400x300")
        history_window.config(bg="black")

        with open("user_data.json", "r", encoding="utf-8") as data:
            try:
                user_data = json.load(data)
            except FileNotFoundError:
                messagebox.showerror("ERROR", "File not found!")

        def listbox_selected(_):
            try:
                selected_index = history_listbox.curselection()
                if not selected_index:
                    return

                selected_text = history_listbox.get(selected_index)

                selected_id = int(selected_text.split(",")[0].split(":")[1].strip())

                selected_user = next((shadow_data for shadow_data in user_data if shadow_data["Id"] == selected_id), None)

                if selected_user:
                    user_info = (
                        f"ID: {selected_user['Id']}\n"
                        f"Name: {selected_user['Name']}\n"
                        f"Surname: {selected_user['Surname']}\n"
                        f"Age: {selected_user['Age']}\n"
                        f"Gender: {selected_user['Gender']}\n"
                        f"BMI: {selected_user['BMI']}\n"
                        f"BMI Categories: {selected_user['BMI Categories']}\n"
                        f"Ideal BMI: {selected_user['Ideal BMI']}\n"
                        f"Timestamp: {selected_user['Timestamp']}"
                    )
                    messagebox.showinfo("User Info", user_info)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        history_listbox = Listbox(history_window, bg="black", fg="white", width=50)

        for data in user_data:
            if isinstance(data, dict):
                history_listbox.insert(END, f"ID: {data['Id']}, Name: {data['Name']}, Surname: {data['Surname']}")

        history_listbox.bind('<<ListboxSelect>>', listbox_selected)
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
            user_data = [shadow_data for shadow_data in user_data if shadow_data["Id"] != id_to_delete]

            with open("user_data.json", "w", encoding="utf-8") as file:
                json.dump(user_data, file, indent=4)  # type: ignore

            messagebox.showinfo("Successfully", f"ID {id_to_delete} the current user has been deleted.")
            history_window.destroy()

        #Delete Button
        delete_user_button = Button(history_window, text="Delete", bg="black", fg="red", command=delete_user_with_id)
        delete_user_button.pack(pady=20)
        #BACK Screen Button
        back_button = Button(history_window, text="Back", command=history_window.destroy, bg="black", fg="white")
        back_button.pack(side=LEFT, padx=5, pady=5)
        #Number of Users
        number_of_users = Label(history_window, text=f"{counter} there are data records", font=("Verdana",7,"bold"), bg="black", fg="white")
        number_of_users.pack(side=BOTTOM)

# Main Screen Buttons
general_button = Button(calculate_button_frame, text="Calculate", command=button_selected, bg="black", fg="white")
general_button.pack()
history_button = Button(text="History", command=history_screen, bg="black", fg="white")
history_button.pack(side=LEFT, padx=10, pady=5)
reset_button = Button(text="Reset Data", command=reset_data, bg="black", fg="red")
reset_button.pack(side=RIGHT, padx=10, pady=5)
exit_button = Button(text="Exit", command=screen.quit, bg="black", fg="white")
exit_button.pack(side=RIGHT, padx=10, pady=5)

# END
screen.mainloop()