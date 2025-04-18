import tkinter as tk
from tkinter import messagebox, ttk
from gui.pages.admin_dashboard import show_admin_interface
from gui.pages.employee_dashboard import show_karyawan_interface
from gui.pages.admin_dashboard import show_admin_interface
from gui.controllers.employee_data_management import add_employee
# from gui.widgets.employee_widgets import go_back_to_admin1, go_back_to_admin2
from gui.configs.db_connection import load_data, save_data

class EmployeeManagementApp:
    def __init__(self, root):
            self.root = root
            self.root.title("WorkNest")
            self.root.geometry("500x400")
            self.root.configure(bg='#ffffff')
            
            self.karyawan_data, self.attendance_records = load_data()
            print("Loaded attendance records:", self.attendance_records) #debug
            self.current_user = None
            
            
            self.login_frame = tk.Frame(self.root, bg='#ffffff', padx=20, pady=20)
            self.login_frame.pack(pady=80)
            
            tk.Label(self.login_frame, text="Username", foreground='#333', bg='#ffffff', font=("Poppins", 10, "bold")).grid(row=0, column=0, sticky="e", pady=(0,10))
            self.username_entry = tk.Entry(self.login_frame, bg='#e0e0e0', width=25, font=("Poppins", 10))
            self.username_entry.grid(row=0, column=1, pady=(0,10), padx=10)
            
            tk.Label(self.login_frame, text="Password", foreground='#333', bg='#ffffff', font=("Poppins", 10, "bold")).grid(row=1, column=0, sticky="e", pady=(0,20))
            self.password_entry = tk.Entry(self.login_frame, show='*', bg='#e0e0e0', width=25, font=("Poppins", 10))
            self.password_entry.grid(row=1, column=1, pady=(0,20), padx=10)
            
            self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, bg='#2596be', fg='#ffffff', font=("Poppins", 10, "bold"), width=20)
            self.login_button.grid(row=2, columnspan=2, pady=10)
            
            self.admin_frame = None
            self.karyawan_frame = None
            self.access_profile = None
    
        
    def login(self):
            username = self.username_entry.get()
            password = self.password_entry.get()
            
            # print(f"Attempting to login with Username: {username} 
            #       and Password: {password}")
            
            if username == "admin" and password == "admin123":
                self.current_user = "admin"
                show_admin_interface(self)
                print("Logged in as \'Admin\'")
                
            elif any(emp['email'] == username and 
                     emp['password'] == password for emp in self.karyawan_data):
                
                self.current_user = username
                show_karyawan_interface(self)
                print("Logged in as \'Karyawan\'")
            else:
                messagebox.showerror("Error", "Username atau password salah.")

    def go_back_to_admin1(self): # go back for "manage employees"
        self.manage_frame.destroy()
        show_admin_interface(self)
        
    def go_back_to_admin2(self): # go back for "tracking  employees"
        self.tracking_frame.destroy()
        show_admin_interface(self)
    
    def manage_employees(self):
        if self.admin_frame is not None:
            self.admin_frame.destroy()
        self.manage_frame = tk.Frame(self.root)
        self.manage_frame.pack(pady=50)
        self.manage_frame.configure(bg='#ffffff')

        title_label = tk.Label(
        self.manage_frame, 
        text="Manajemen Data Karyawan", 
        foreground='#2596be', 
        bg='#ffffff', 
        font=("Poppins", 14, "bold")
        )
            
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        tk.Label(self.manage_frame, text="Nama", foreground='#333', bg='#ffffff', font=("Poppins", 10)).grid(row=1, column=0, sticky="e", padx=(0, 10), pady=(0, 10))
        self.name_entry = tk.Entry(self.manage_frame, bg='#e0e0e0', font=("Poppins", 10), width=30, relief="flat")
        self.name_entry.grid(row=1, column=1, pady=(0, 10))

        tk.Label(self.manage_frame, text="Username", foreground='#333', bg='#ffffff', font=("Poppins", 10)).grid(row=2, column=0, sticky="e", padx=(0, 10), pady=(0, 10))
        self.username_entry = tk.Entry(self.manage_frame, bg='#e0e0e0', font=("Poppins", 10), width=30, relief="flat")
        self.username_entry.grid(row=2, column=1, pady=(0, 10))

        tk.Label(self.manage_frame, text="Password", foreground='#333', bg='#ffffff', font=("Poppins", 10)).grid(row=3, column=0, sticky="e", padx=(0, 10), pady=(0, 10))
        self.password_entry = tk.Entry(self.manage_frame, show='*', bg='#e0e0e0', font=("Poppins", 10), width=30, relief="flat")
        self.password_entry.grid(row=3, column=1, pady=(0, 10))

        add_button = tk.Button(
        self.manage_frame, 
        text="Tambah Karyawan", 
        command=add_employee(self), 
        foreground='#ffffff', 
        bg='#2596be', 
        font=("Poppins", 10, "bold"), 
        relief="flat", 
        width=20,
        pady=5
        )
        add_button.grid(row=4, column=0, columnspan=2, pady=(10, 20))

        self.employee_listbox = tk.Listbox(
        self.manage_frame, 
        width=40, 
        height=10, 
        foreground='#333333', 
        bg='#e0e0e0', 
        font=("Poppins", 10), 
        relief="flat", 
        selectbackground="#2596be"
        )
        self.employee_listbox.grid(row=5, column=0, columnspan=2, pady=(10, 10), padx=(5, 5))

        back_button = tk.Button(
        self.manage_frame, 
        text="Kembali", 
        command=self.go_back_to_admin1, 
        foreground='#ffffff', 
        bg='#b90000', 
        font=("Poppins", 10, "bold"),         # BACK BUTTON
        relief="flat", 
        width=20,
        pady=5
        )
        back_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))
            
        # self.update_employee_list()

    def employee_tracking(self):
        self.admin_frame.destroy()
        self.tracking_frame = tk.Frame(self.root)
        self.tracking_frame.pack(pady=20)
        self.tracking_frame.configure(bg='#ffffff')
            
        tk.Label(self.tracking_frame, text="Pelacak Kehadiran Karyawan", foreground='#ffffff' , bg='#2596be').grid(row=0, columnspan=2)
            
        self.employee_listbox = tk.Listbox(self.tracking_frame, width=50, foreground='#ffffff' , bg='#2596be')
        self.employee_listbox.grid(row=2, columnspan=2, pady=20)
            
        for emp in self.karyawan_data:
            self.employee_listbox.insert(tk.END, f"{emp['name']}")

        tk.Button(self.tracking_frame, text="Tandai Kehadiran", command=self.mark_attendance, foreground='#ffffff' , bg='#2596be').grid(row=3, columnspan=2)
        tk.Button(self.tracking_frame, text="Tampilkan Kehadiran", command=self.show_attendance, foreground='#ffffff' , bg='#2596be').grid(row=5, columnspan=2)
        tk.Button(self.tracking_frame, text="Kembali", command=self.go_back_to_admin2, foreground='#ffffff' , bg='#b90000').grid(row=7, columnspan=2)
            
        names = [emp['name'] for emp in self.karyawan_data]
        ttk.Combobox(self.tracking_frame, values=names).grid(row=9, columnspan=2)

    def mark_attendance(self):
            selected_employee_index = self.employee_listbox.curselection()
            if not selected_employee_index:
                messagebox.showerror("Error", "Silakan pilih karyawan untuk menandai kehadiran.")
                return
            
            selected_employee = self.karyawan_data[selected_employee_index[0]]
            name = selected_employee['name']
            
            if name not in self.attendance_records:
                self.attendance_records[name] = []
            
            # Mark attendance with the current date
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            self.attendance_records[name].append(today)
            
            save_data(self.karyawan_data, self.attendance_records)
            
            messagebox.showinfo("Success", f"Kehadiran untuk {selected_employee['name']} telah ditandai.")
            
            #debug 
            print(f"Attendance marked for {selected_employee['name']} on {today}.")
            print("Current attendance records:", self.attendance_records)  # Debug print

    def show_attendance(self):
            attendance_window = tk.Toplevel(self.root)
            attendance_window.title("Rekaman Kehadiran")
            attendance_window.configure(bg='#ffffff')
            
            tk.Label(attendance_window, text="Rekaman Kehadiran Karyawan", foreground='#ffffff' , bg='#2596be').pack(pady=10)

            for emp in self.karyawan_data:
                name = emp['name']
                email = emp['email']
                attendance_dates = self.attendance_records.get(name,[])
                attendance_info = f"{emp['name']} ({email}): {', '.join(attendance_dates) if attendance_dates else 'Tidak Ada Kehadiran'}"
                tk.Label(attendance_window, text=attendance_info, foreground='#ffffff' , bg='#2596be').pack(pady=5)

            print("Attendace succefully showed") if attendance_info else  print("No attendance recorded for this employee")  # Debug print