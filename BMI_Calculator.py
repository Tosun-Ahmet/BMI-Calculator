#Importing Library
from tkinter import *
from tkinter import messagebox

# Screen
screen = Tk()
screen.title("BMI Calculator")
screen.config(background="black")
screen.geometry("400x500")

# Define Frame for Layout
frame = Frame(screen, bg="black")
frame.pack(fill=BOTH, expand=True)

# Name Section
name_frame = Frame(frame, bg="black")
name_frame.pack(pady=10)

# Gender Section
gender_frame = Frame(frame, bg="black")
gender_frame.pack(pady=10)

# Weight and Height Section
data_frame = Frame(frame, bg="black")
data_frame.pack(pady=10)

# Button Section
button_frame = Frame(frame, bg="black")
button_frame.pack(pady=20)

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
            messagebox.showerror("Error", "Please fill in both username and surname.")
            return
        if boy_value < 1 or boy_value > 3:
            messagebox.showerror("Error", "Please enter a valid height.")
            return

        # BMI Calculation
        bmi = int((kg_value / (boy_value * boy_value)))

        # BMI Categories
        if bmi <= 20:
            bmi_name = "Underweight"
            color = "#3498db"
        elif bmi > 20 and bmi <= 25:
            bmi_name = "Normal"
            color = "#2ecc71"
        elif bmi > 25 and bmi <= 30:
            bmi_name = "Overweight"
            color = "#f1c40f"
        elif bmi > 30 and bmi <= 35:
            bmi_name = "Obese"
            color = "#e67e22"
        else:
            bmi_name = "Severely Obese"
            color = "#e74c3c"

        # Ideal BMI
        if age_value >= 19 and age_value <= 24:
            ideal_bmi = "19-24"
        elif age_value >= 25 and age_value <= 34:
            ideal_bmi = "20-25"
        elif age_value >= 35 and age_value <= 44:
            ideal_bmi = "21-26"
        elif age_value >= 45 and age_value <= 54:
            ideal_bmi = "22-27"
        elif age_value >= 55 and age_value <= 65:
            ideal_bmi = "23-28"
        else:
            ideal_bmi = "24-29"

        #2nd Screen so result window
        result_window = Toplevel(screen)
        result_window.title("BMI Result Window")
        result_window.geometry("400x300")
        result_window.config(bg=color)

        #Info screen
        result_label = Label(result_window, text=f"Name: {username}\nSurname: {surname}\nAge: {age_value}\nGender: {gender}\nBMI: {bmi} >> {bmi_name}\nIdeal BMI: {ideal_bmi}", bg=color, font=("Arial", 14), anchor="w", fg="white")
        result_label.pack(padx=20, pady=20)

        #BACK and EXIT screen
        back_button = Button(result_window, text="Back", command=result_window.destroy)
        back_button.pack(side=LEFT, padx=10, pady=10)
        exit_button = Button(result_window, text="Exit", command=screen.quit)
        exit_button.pack(side=RIGHT, padx=10, pady=10)

    except ValueError:
        messagebox.showerror("Error", "Empty spaces need to be filled")

general_button = Button(button_frame, text="Calculate", command=button_selected)
general_button.pack()

# END
screen.mainloop()