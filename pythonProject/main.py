import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import page1
from datetime import datetime


def fetch_options():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT domain1 FROM test_set")
    options = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return options

def next_page():
    name = name_entry.get()
    surname = surname_entry.get()
    selection = combo_box.get()
    print(selection)

    if not name or not surname or not selection:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
    else:

        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO player (first_name, last_name) VALUES (?, ?)", (name, surname))
        conn.commit()
        cursor.execute("SELECT idset FROM test_set WHERE domain1 = ?", (selection,))
        domain_idset = cursor.fetchone()

        if domain_idset:
            domain_idset = domain_idset[0]
            print(domain_idset)


            cursor.execute('''
                SELECT q.idint
                FROM question q
                JOIN test t ON q.idint = t.idint
                JOIN test_set ts ON ts.idset = t.idset
                WHERE ts.domain1 = ?
            ''', (selection,))

            questions = cursor.fetchall()
            if not questions:
                messagebox.showerror("Error", "No questions found for the selected category.")
                return
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_hour = datetime.now().strftime('%H:%M:%S')
            score = 0
            cursor.execute('''
                INSERT INTO game (idset, date1, hour1, score, idgame)
                VALUES (?, ?, ?, ?, ?)
            ''', (domain_idset, current_date, current_hour, score, cursor.lastrowid))
            conn.commit()
        cursor.close()
        conn.close()
        root.destroy()
        page1.start_game(name, surname, selection)


root = tk.Tk()
root.title("User Information with Image")


image_path = "image.jpg"
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)


canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=photo)

name_label = tk.Label(root, text="First Name:", bg="#be66e3", fg="white",)
name_label_window = canvas.create_window(150, 50, window=name_label)

name_entry = tk.Entry(root)
name_entry_window = canvas.create_window(150, 80, window=name_entry)

surname_label = tk.Label(root, text="Last Name:",   bg="#be66e3", fg="white",)
surname_label_window = canvas.create_window(150, 110, window=surname_label)

surname_entry = tk.Entry(root)
surname_entry_window = canvas.create_window(150, 140, window=surname_entry)

combo_label = tk.Label(root, text="Select Option:",   bg="#be66e3", fg="white",)
combo_label_window = canvas.create_window(150, 170, window=combo_label)

options = fetch_options()

combo_box = ttk.Combobox(root, values=options)
combo_box_window = canvas.create_window(150, 200, window=combo_box)


next_button = tk.Button(root, text="Next Page", command=next_page,   bg="#be66e3", fg="white",)
next_button_window = canvas.create_window(150, 230, window=next_button)


root.mainloop()