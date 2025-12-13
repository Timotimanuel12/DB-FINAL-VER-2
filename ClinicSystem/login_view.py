import tkinter as tk
from tkinter import messagebox
import database
import patient_view, doctor_view, admin_view


class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Clinic Management Portal", font=("Arial", 26, "bold"), fg="#333").pack(pady=30)

        # --- LOGIN ---
        login_frame = tk.Frame(self, padx=20, pady=20, relief="groove", borderwidth=2)
        login_frame.pack(pady=10)

        tk.Label(login_frame, text="Login", font=("Arial", 14, "bold")).pack()

        btn_frame = tk.Frame(login_frame)
        btn_frame.pack(pady=10)
        self.make_role_btn(btn_frame, "Patient", "patient")
        self.make_role_btn(btn_frame, "Doctor", "doctor")
        tk.Button(btn_frame, text="Admin", width=12, bg="#555", fg="white",
                  command=lambda: controller.show_view(admin_view.AdminScreen)).pack(side="left", padx=5)

        self.input_frame = tk.Frame(login_frame)
        self.lbl_prompt = tk.Label(self.input_frame, text="ID:", font=("Arial", 10))
        self.lbl_prompt.pack()
        self.ent_id = tk.Entry(self.input_frame, font=("Arial", 12))
        self.ent_id.pack(pady=5)
        tk.Button(self.input_frame, text="Sign In", bg="green", fg="white", width=15, command=self.login).pack(pady=10)

        # --- REGISTER ---
        tk.Label(self, text="New Patient?", font=("Arial", 10)).pack(pady=(30, 5))
        tk.Button(self, text="Create Account", bg="blue", fg="white", command=self.toggle_register).pack()

        self.reg_frame = tk.LabelFrame(self, text="New Patient Registration", padx=20, pady=20)

        tk.Label(self.reg_frame, text="Full Name:").grid(row=0, column=0, sticky="e")
        self.r_name = tk.Entry(self.reg_frame);
        self.r_name.grid(row=0, column=1)
        tk.Label(self.reg_frame, text="Gender:").grid(row=1, column=0, sticky="e")
        self.r_gender = tk.Entry(self.reg_frame);
        self.r_gender.grid(row=1, column=1)
        tk.Label(self.reg_frame, text="DOB (Y-M-D):").grid(row=2, column=0, sticky="e")
        self.r_dob = tk.Entry(self.reg_frame);
        self.r_dob.grid(row=2, column=1)
        tk.Label(self.reg_frame, text="Phone:").grid(row=3, column=0, sticky="e")
        self.r_phone = tk.Entry(self.reg_frame);
        self.r_phone.grid(row=3, column=1)

        tk.Button(self.reg_frame, text="Sign Up", bg="green", fg="white", command=self.register).grid(row=4,
                                                                                                      columnspan=2,
                                                                                                      pady=15)

        self.role = ""

    def make_role_btn(self, parent, text, role):
        tk.Button(parent, text=text, width=12, command=lambda: self.show_input(role)).pack(side="left", padx=5)

    def show_input(self, role):
        self.role = role
        self.input_frame.pack(pady=10)
        self.lbl_prompt.config(text=f"Enter {role.capitalize()} ID:")

    def toggle_register(self):
        if self.reg_frame.winfo_ismapped():
            self.reg_frame.pack_forget()
        else:
            self.reg_frame.pack(pady=10)

    def register(self):
        name = self.r_name.get()
        if not name: return messagebox.showerror("Error", "Name Required")
        sql = "INSERT INTO patient (patientName, patientGender, patientBirthDate, patientPhoneNumber) VALUES (%s, %s, %s, %s)"
        new_id = database.execute_query(sql, (name, self.r_gender.get(), self.r_dob.get(), self.r_phone.get()))
        if new_id:
            messagebox.showinfo("Success", f"Account Created!\n\nIMPORTANT: Your Patient ID is {new_id}.")
            self.reg_frame.pack_forget()

    def login(self):
        uid = self.ent_id.get()
        if not uid.isdigit(): return messagebox.showerror("Error", "ID must be a number")
        table = "patient" if self.role == "patient" else "doctor"
        col = "patientID" if self.role == "patient" else "doctorID"
        user = database.fetch_all(f"SELECT * FROM {table} WHERE {col}=%s", (uid,))
        if user:
            self.controller.current_user_id = uid
            if self.role == 'patient':
                self.controller.show_view(patient_view.PatientScreen)
            else:
                self.controller.show_view(doctor_view.DoctorScreen)
        else:
            messagebox.showerror("Failed", "ID Not Found")