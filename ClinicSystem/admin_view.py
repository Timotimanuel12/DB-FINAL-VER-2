import tkinter as tk
from tkinter import ttk, messagebox
import database
import login_view


class AdminScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Header
        header = tk.Frame(self, bg="#222", height=50);
        header.pack(fill="x")
        tk.Label(header, text="ADMINISTRATION DASHBOARD", fg="white", bg="#222", font=("Arial", 16, "bold")).pack(
            side="left", padx=20)
        tk.Button(header, text="Logout", command=lambda: controller.show_view(login_view.LoginScreen)).pack(
            side="right", padx=20)

        # Tabs
        tabs = ttk.Notebook(self);
        tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_sched = tk.Frame(tabs);
        tabs.add(self.tab_sched, text="Master Schedule")
        self.tab_finance = tk.Frame(tabs);
        tabs.add(self.tab_finance, text="Transactions")
        self.tab_patients = tk.Frame(tabs);
        tabs.add(self.tab_patients, text="Manage Patients")  # NEW
        self.tab_doctors = tk.Frame(tabs);
        tabs.add(self.tab_doctors, text="Manage Doctors")  # NEW
        self.tab_staff = tk.Frame(tabs);
        tabs.add(self.tab_staff, text="Manage Staff")
        self.tab_rooms = tk.Frame(tabs);
        tabs.add(self.tab_rooms, text="Manage Rooms")

        self.setup_schedule()
        self.setup_finance()
        self.setup_patients()
        self.setup_doctors()
        self.setup_staff()
        self.setup_rooms()

    # --- TAB 1: SCHEDULE ---
    def setup_schedule(self):
        tools = tk.Frame(self.tab_sched, pady=10);
        tools.pack(fill="x")
        tk.Button(tools, text="Verify (Assign Staff)", bg="green", fg="white", command=self.verify_window).pack(
            side="left", padx=5)
        tk.Button(tools, text="Cancel Appt", bg="orange", command=self.cancel).pack(side="left", padx=5)
        tk.Button(tools, text="Delete Record", bg="red", fg="white", command=self.delete).pack(side="left", padx=5)

        cols = ("ID", "Date", "Time", "Patient", "Doctor", "Room", "Staff", "Status", "Treatment", "Notes")
        self.tree_appt = ttk.Treeview(self.tab_sched, columns=cols, show='headings', height=15)
        for c in cols: self.tree_appt.heading(c, text=c)
        self.tree_appt.column("ID", width=30);
        self.tree_appt.column("Room", width=50);
        self.tree_appt.column("Status", width=80)
        self.tree_appt.pack(fill="both", expand=True)
        self.refresh_schedule()

    # --- TAB 2: FINANCE ---
    def setup_finance(self):
        tk.Label(self.tab_finance, text="Payment History", font=("Arial", 12, "bold")).pack(pady=10)
        cols = ("Pay ID", "Appt Date", "Patient", "Amount", "Status")
        self.tree_fin = ttk.Treeview(self.tab_finance, columns=cols, show='headings')
        for c in cols: self.tree_fin.heading(c, text=c)
        self.tree_fin.pack(fill="both", expand=True)
        self.refresh_finance()

    # --- TAB 3: PATIENTS (NEW) ---
    def setup_patients(self):
        form = tk.Frame(self.tab_patients, pady=10);
        form.pack()

        tk.Label(form, text="Name:").pack(side="left")
        self.ent_p_name = tk.Entry(form, width=15);
        self.ent_p_name.pack(side="left", padx=2)

        tk.Label(form, text="Gender:").pack(side="left")
        self.ent_p_gen = tk.Entry(form, width=8);
        self.ent_p_gen.pack(side="left", padx=2)

        tk.Label(form, text="DOB (Y-M-D):").pack(side="left")
        self.ent_p_dob = tk.Entry(form, width=10);
        self.ent_p_dob.pack(side="left", padx=2)

        tk.Label(form, text="Phone:").pack(side="left")
        self.ent_p_phone = tk.Entry(form, width=12);
        self.ent_p_phone.pack(side="left", padx=2)

        tk.Button(form, text="Add", bg="#333", fg="white", command=self.add_patient).pack(side="left", padx=10)
        tk.Button(form, text="Remove Selected", bg="red", fg="white", command=self.del_patient).pack(side="left")

        self.tree_pat = ttk.Treeview(self.tab_patients, columns=("ID", "Name", "Gender", "Phone", "DOB"),
                                     show='headings')
        for c in ("ID", "Name", "Gender", "Phone", "DOB"): self.tree_pat.heading(c, text=c)
        self.tree_pat.pack(fill="both", expand=True)
        self.refresh_patients()

    # --- TAB 4: DOCTORS (NEW) ---
    def setup_doctors(self):
        form = tk.Frame(self.tab_doctors, pady=10);
        form.pack()

        tk.Label(form, text="Name:").pack(side="left")
        self.ent_d_name = tk.Entry(form, width=15);
        self.ent_d_name.pack(side="left", padx=5)

        tk.Label(form, text="Specialty:").pack(side="left")
        self.ent_d_spec = tk.Entry(form, width=15);
        self.ent_d_spec.pack(side="left", padx=5)

        tk.Label(form, text="Assign Room:").pack(side="left")
        # Fetch rooms for dropdown
        rooms = database.fetch_all("SELECT roomNumber FROM room")
        self.room_list = [r['roomNumber'] for r in rooms]
        self.cb_d_room = ttk.Combobox(form, values=self.room_list, width=5)
        self.cb_d_room.pack(side="left", padx=5)

        tk.Button(form, text="Add", bg="#333", fg="white", command=self.add_doctor).pack(side="left", padx=10)
        tk.Button(form, text="Remove Selected", bg="red", fg="white", command=self.del_doctor).pack(side="left")

        self.tree_doc = ttk.Treeview(self.tab_doctors, columns=("ID", "Name", "Specialty", "Room"), show='headings')
        for c in ("ID", "Name", "Specialty", "Room"): self.tree_doc.heading(c, text=c)
        self.tree_doc.pack(fill="both", expand=True)
        self.refresh_doctors()

    # --- TAB 5: STAFF ---
    def setup_staff(self):
        form = tk.Frame(self.tab_staff, pady=10);
        form.pack()
        tk.Label(form, text="Name:").pack(side="left")
        self.ent_s_name = tk.Entry(form);
        self.ent_s_name.pack(side="left", padx=5)
        tk.Label(form, text="Role:").pack(side="left")
        self.ent_s_role = tk.Entry(form);
        self.ent_s_role.pack(side="left", padx=5)
        tk.Button(form, text="Add", bg="#333", fg="white", command=self.add_staff).pack(side="left", padx=10)
        tk.Button(form, text="Remove", bg="red", fg="white", command=self.del_staff).pack(side="left")

        self.tree_staff = ttk.Treeview(self.tab_staff, columns=("ID", "Name", "Role"), show='headings')
        for c in ("ID", "Name", "Role"): self.tree_staff.heading(c, text=c)
        self.tree_staff.pack(fill="both", expand=True)
        self.refresh_staff()

    # --- TAB 6: ROOMS ---
    def setup_rooms(self):
        form = tk.Frame(self.tab_rooms, pady=10);
        form.pack()
        tk.Label(form, text="Room Number:").pack(side="left")
        self.ent_room = tk.Entry(form);
        self.ent_room.pack(side="left", padx=5)
        tk.Button(form, text="Add", bg="#333", fg="white", command=self.add_room).pack(side="left", padx=10)
        tk.Button(form, text="Remove", bg="red", fg="white", command=self.del_room).pack(side="left")

        self.tree_room = ttk.Treeview(self.tab_rooms, columns=("Number", "Status"), show='headings')
        for c in ("Number", "Status"): self.tree_room.heading(c, text=c)
        self.tree_room.pack(fill="both", expand=True)
        self.refresh_rooms()

    # --- REFRESHERS ---
    def refresh_schedule(self):
        for i in self.tree_appt.get_children(): self.tree_appt.delete(i)
        rows = database.fetch_all("""
            SELECT a.id, a.appointmentDate, a.appointmentTime, p.patientName, d.doctorName, 
                   a.roomNumber, a.appointmentStatus, t.treatment, a.doctorNotes, s.staffName
            FROM appointment a 
            JOIN patient p ON a.patientID=p.patientID 
            JOIN doctor d ON a.doctorID=d.doctorID
            LEFT JOIN treatment t ON a.treatmentID=t.treatmentID
            LEFT JOIN staff s ON a.staffID=s.staffID
            ORDER BY a.appointmentDate DESC
        """)
        for r in rows:
            treat = r['treatment'] or "-"
            note = r['doctorNotes'] or "-"
            room = r['roomNumber'] or "-"
            staff = r['staffName'] or "Unassigned"
            self.tree_appt.insert("", "end", values=(
            r['id'], r['appointmentDate'], r['appointmentTime'], r['patientName'], r['doctorName'], room, staff,
            r['appointmentStatus'], treat, note))

    def refresh_finance(self):
        for i in self.tree_fin.get_children(): self.tree_fin.delete(i)
        rows = database.fetch_all("""
            SELECT pay.paymentID, a.appointmentDate, pt.patientName, pay.paymentAmount, pay.paymentStatus
            FROM payment pay JOIN appointment a ON pay.paymentID = a.paymentID
            JOIN patient pt ON a.patientID = pt.patientID ORDER BY a.appointmentDate DESC
        """)
        for r in rows:
            self.tree_fin.insert("", "end", values=(
            r['paymentID'], r['appointmentDate'], r['patientName'], f"${r['paymentAmount']}", r['paymentStatus']))

    def refresh_patients(self):
        for i in self.tree_pat.get_children(): self.tree_pat.delete(i)
        for r in database.fetch_all("SELECT * FROM patient"): self.tree_pat.insert("", "end", values=(
        r['patientID'], r['patientName'], r['patientGender'], r['patientPhoneNumber'], r['patientBirthDate']))

    def refresh_doctors(self):
        # Also refresh room dropdown
        rooms = database.fetch_all("SELECT roomNumber FROM room")
        self.cb_d_room['values'] = [r['roomNumber'] for r in rooms]

        for i in self.tree_doc.get_children(): self.tree_doc.delete(i)
        for r in database.fetch_all("SELECT * FROM doctor"): self.tree_doc.insert("", "end", values=(
        r['doctorID'], r['doctorName'], r['doctorSpecialty'], r['assignedRoom']))

    def refresh_staff(self):
        for i in self.tree_staff.get_children(): self.tree_staff.delete(i)
        for r in database.fetch_all("SELECT * FROM staff"): self.tree_staff.insert("", "end", values=(
        r['staffID'], r['staffName'], r['staffRole']))

    def refresh_rooms(self):
        for i in self.tree_room.get_children(): self.tree_room.delete(i)
        for r in database.fetch_all("SELECT * FROM room"): self.tree_room.insert("", "end", values=(
        r['roomNumber'], r['roomStatus']))

    # --- ACTIONS ---
    def get_sel_id(self, tree):
        sel = tree.selection()
        if not sel: return None
        return tree.item(sel[0])['values'][0]

    # Adders
    def add_patient(self):
        database.execute_query(
            "INSERT INTO patient (patientName, patientGender, patientBirthDate, patientPhoneNumber) VALUES (%s, %s, %s, %s)",
            (self.ent_p_name.get(), self.ent_p_gen.get(), self.ent_p_dob.get(), self.ent_p_phone.get()))
        self.refresh_patients()

    def add_doctor(self):
        database.execute_query("INSERT INTO doctor (doctorName, doctorSpecialty, assignedRoom) VALUES (%s, %s, %s)",
                               (self.ent_d_name.get(), self.ent_d_spec.get(), self.cb_d_room.get()))
        self.refresh_doctors()

    def add_staff(self):
        database.execute_query("INSERT INTO staff (staffName, staffRole) VALUES (%s, %s)",
                               (self.ent_s_name.get(), self.ent_s_role.get()))
        self.refresh_staff()

    def add_room(self):
        database.execute_query("INSERT INTO room (roomNumber, roomStatus) VALUES (%s, 'Available')",
                               (self.ent_room.get(),))
        self.refresh_rooms()

    # Deleters
    def del_patient(self):
        id = self.get_sel_id(self.tree_pat)
        if id:
            if not database.execute_query("DELETE FROM patient WHERE patientID=%s", (id,)):
                messagebox.showerror("Error", "Cannot delete: Patient has records.")
            self.refresh_patients()

    def del_doctor(self):
        id = self.get_sel_id(self.tree_doc)
        if id:
            if not database.execute_query("DELETE FROM doctor WHERE doctorID=%s", (id,)):
                messagebox.showerror("Error", "Cannot delete: Doctor has records.")
            self.refresh_doctors()

    def del_staff(self):
        id = self.get_sel_id(self.tree_staff)
        if id: database.execute_query("DELETE FROM staff WHERE staffID=%s", (id,)); self.refresh_staff()

    def del_room(self):
        id = self.get_sel_id(self.tree_room)
        if id: database.execute_query("DELETE FROM room WHERE roomNumber=%s", (id,)); self.refresh_rooms()

    # Schedule Actions
    def verify_window(self):
        sel = self.tree_appt.selection()
        if not sel: return

        # 1. Get Appointment Details to check time
        item = self.tree_appt.item(sel[0])
        self.ver_id = item['values'][0]
        date = item['values'][1]
        time = item['values'][2]

        self.win = tk.Toplevel(self)
        self.win.title("Assign Staff")
        tk.Label(self.win, text=f"Select Staff (Available at {time}):", font=("bold")).pack(pady=10)

        # 2. SMART FILTER: Only get staff who are NOT busy at this Date/Time
        avail_staff = database.get_available_staff(date, time)

        if not avail_staff:
            tk.Label(self.win, text="No Staff Available!", fg="red").pack()
            return

        self.staff_map = {f"{s['staffName']} ({s['staffRole']})": s['staffID'] for s in avail_staff}
        self.cb_staff = ttk.Combobox(self.win, values=list(self.staff_map.keys()), width=30)
        self.cb_staff.pack(pady=5)

        tk.Button(self.win, text="Confirm", bg="green", fg="white", command=self.confirm_verify).pack(pady=10)

    def confirm_verify(self):
        if not self.cb_staff.get(): return messagebox.showerror("Error", "Select Staff")
        sid = self.staff_map[self.cb_staff.get()]

        database.execute_query("UPDATE appointment SET appointmentStatus='Scheduled', staffID=%s WHERE id=%s",
                               (sid, self.ver_id))
        self.win.destroy()
        self.refresh_schedule()

    def cancel(self):
        aid = self.get_sel_id(self.tree_appt)
        if not aid: return
        room_data = database.fetch_all("SELECT roomNumber FROM appointment WHERE id=%s", (aid,))
        if room_data and room_data[0]['roomNumber']:
            database.set_room_status(room_data[0]['roomNumber'], 'Available')
        self.update_status('Cancelled')

    def delete(self):
        aid = self.get_sel_id(self.tree_appt)
        if not aid: return
        status = self.tree_appt.item(self.tree_appt.selection()[0])['values'][7]  # Index 7 is Status
        if status != 'Cancelled':
            if not messagebox.askyesno("Warning", "Appointment active. Delete anyway?"): return

        database.execute_query("DELETE FROM appointment WHERE id=%s", (aid,))
        self.refresh_schedule()

    def update_status(self, stat):
        aid = self.get_sel_id(self.tree_appt)
        if aid:
            database.execute_query("UPDATE appointment SET appointmentStatus=%s WHERE id=%s", (stat, aid))
            self.refresh_schedule()