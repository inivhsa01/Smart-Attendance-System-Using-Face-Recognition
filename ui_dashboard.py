import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
import os
from attendance_system import add_student, start_camera

ATTENDANCE_FILE = "attendance.xlsx"

# ================= THEME =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Attendance System - ULTRA UI")
app.geometry("1050x600")
app.resizable(False, False)

# ================= TOP TITLE =================
title = ctk.CTkLabel(app,
                     text="SMART ATTENDANCE SYSTEM",
                     font=("Arial", 28, "bold"))
title.pack(pady=10)

# ================= MAIN LAYOUT =================
main = ctk.CTkFrame(app)
main.pack(fill="both", expand=True, padx=15, pady=10)

# ================= SIDEBAR =================
sidebar = ctk.CTkFrame(main, width=200)
sidebar.pack(side="left", fill="y", padx=10, pady=10)

# ================= CONTENT AREA =================
content = ctk.CTkFrame(main)
content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# ================= STATUS =================
status_label = ctk.CTkLabel(content,
                            text="Status: READY",
                            font=("Arial", 16),
                            text_color="lightgreen")
status_label.pack(pady=10)

def set_status(msg):
    status_label.configure(text=f"Status: {msg}")
    app.update()

# ================= COUNTERS =================
counter_frame = ctk.CTkFrame(content)
counter_frame.pack(pady=10)

student_count = ctk.CTkLabel(counter_frame, text="Students: 0", font=("Arial", 14))
student_count.grid(row=0, column=0, padx=20)

attendance_count = ctk.CTkLabel(counter_frame, text="Attendance: 0", font=("Arial", 14))
attendance_count.grid(row=0, column=1, padx=20)

def update_counters():
    if os.path.exists(ATTENDANCE_FILE):
        df = pd.read_excel(ATTENDANCE_FILE)
        attendance_count.configure(text=f"Attendance: {len(df)}")
    else:
        attendance_count.configure(text="Attendance: 0")

# ================= ADD STUDENT =================
def add_student_ui():
    win = ctk.CTkToplevel(app)
    win.title("Add Student")
    win.geometry("320x250")

    ctk.CTkLabel(win, text="Name").pack(pady=5)
    name_entry = ctk.CTkEntry(win)
    name_entry.pack()

    ctk.CTkLabel(win, text="Roll No").pack(pady=5)
    roll_entry = ctk.CTkEntry(win)
    roll_entry.pack()

    def submit():
        name = name_entry.get()
        roll = roll_entry.get()

        win.destroy()

        set_status("Capturing Face Data...")
        msg = add_student(name, roll)

        set_status(msg)
        messagebox.showinfo("Success", msg)

    ctk.CTkButton(win, text="Save", command=submit).pack(pady=20)

# ================= ATTENDANCE =================
def take_attendance():
    set_status("Starting Camera...")

    msg = start_camera()

    set_status(msg)
    messagebox.showinfo("Attendance", msg)

    update_counters()

# ================= RECORDS VIEW =================
def view_records():

    if not os.path.exists(ATTENDANCE_FILE):
        messagebox.showerror("Error", "No Records Found")
        return

    df = pd.read_excel(ATTENDANCE_FILE)

    win = ctk.CTkToplevel(app)
    win.title("Attendance Records")
    win.geometry("800x450")

    text = ctk.CTkTextbox(win, width=760, height=400)
    text.pack(pady=10)

    text.insert("0.0", df.to_string(index=False))

    set_status("Records Loaded ✔")

# ================= OPEN EXCEL =================
def open_excel():
    if os.path.exists(ATTENDANCE_FILE):
        os.startfile(ATTENDANCE_FILE)
        set_status("Opening Excel...")
    else:
        messagebox.showerror("Error", "File Not Found")

# ================= SIDEBAR BUTTONS =================
ctk.CTkButton(sidebar, text="➕ Add Student",
              command=add_student_ui).pack(pady=10)

ctk.CTkButton(sidebar, text="📸 Take Attendance",
              command=take_attendance).pack(pady=10)

ctk.CTkButton(sidebar, text="📊 View Records",
              command=view_records).pack(pady=10)

ctk.CTkButton(sidebar, text="📂 Open Excel",
              command=open_excel).pack(pady=10)

ctk.CTkButton(sidebar, text="🔄 Refresh",
              command=update_counters).pack(pady=10)

# ================= INITIAL LOAD =================
update_counters()

app.mainloop()