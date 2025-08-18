from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import results


def fetch_questions(selected_category):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT q.question, q.var1, q.var2, q.var3, q.var4, q.correct
        FROM question q
        JOIN test t ON q.idint = t.idint
        JOIN test_set ts ON ts.idset = t.idset
        WHERE ts.domain1 = ?
    ''', (selected_category,))

    questions = cursor.fetchall()
    cursor.close()
    conn.close()

    return questions


def save_game_score_to_db(name, surname, selected_category, score):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()


    cursor.execute('''
        SELECT idgame FROM player WHERE first_name = ? AND last_name = ?
    ''', (name, surname))
    player = cursor.fetchone()

    if not player:
        cursor.execute('''
            INSERT INTO player (first_name, last_name) VALUES (?, ?)
        ''', (name, surname))
        conn.commit()
        player_id = cursor.lastrowid
    else:
        player_id = player[0]


    cursor.execute('''
        SELECT idset FROM test_set WHERE domain1 = ?
    ''', (selected_category,))
    category = cursor.fetchone()

    if not category:
        messagebox.showerror("Error", "Category not found.")
        conn.close()
        return

    category_id = category[0]

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    cursor.execute('''
        INSERT INTO game (idgame, idset, date1, hour1, score) 
        VALUES (?, ?, ?, ?, ?)
    ''', (player_id, category_id, current_date, current_time, score))

    conn.commit()
    cursor.close()
    conn.close()


def start_game(name, surname, selected_category):
    global user_name, user_surname, user_category, score, current_question_index, questions
    user_name = name
    user_surname = surname
    user_category = selected_category
    score = 0
    current_question_index = 0

    questions = fetch_questions(selected_category)

    if not questions:
        messagebox.showerror("Error", "No questions found for the selected category.")
        return

    root = tk.Tk()
    root.title("Trivia Game - Question 1")

    image_path = "image.jpg"
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    canvas = tk.Canvas(root, width=image.width, height=image.height)
    canvas.pack()

    canvas.create_image(0, 0, anchor="nw", image=photo)


    score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 14), bg="white", fg="black")
    score_label_window = canvas.create_window(50, 30, window=score_label)  # Position at top left

    def update_score():

        score_label.config(text=f"Score: {score}")

    def check_answer():
        global score
        selected_answer = selected_answer_var.get()

        if selected_answer == "":
            return

        correct_answer = questions[current_question_index][5]
        if selected_answer == correct_answer:
            score += 5

            messagebox.showinfo("Correct", "Your answer is correct!")
        else:

            messagebox.showinfo("Wrong", "Your answer is incorrect!")

        update_score()

    def next_question():
        global current_question_index

        check_answer()

        current_question_index += 1

        if current_question_index < len(questions):
            show_question()
        else:

            messagebox.showinfo("Game Over", f"Your final score is: {score}")
            save_game_score_to_db(user_name, user_surname, user_category, score)
            root.destroy()
            results.show_results(user_name,user_surname,score)

    def show_question():
        if current_question_index < len(questions):
            question_data = questions[current_question_index]
            question_text = question_data[0]
            options = question_data[1:5]
            question_label.config(text=question_text)

            for i, option in enumerate(options):
                radio_buttons[i].config(text=option, value=option)
            selected_answer_var.set("")

    question_label = tk.Label(root, text="", font=("Arial", 14), bg="white", fg="black")
    question_label_window = canvas.create_window(300, 50, window=question_label)

    selected_answer_var = tk.StringVar()
    selected_answer_var.set("")

    radio_buttons = []
    for i in range(4):
        radio_button = tk.Radiobutton(root, text="", variable=selected_answer_var, value="",
                                      font=("Arial", 12), bg="#be66e3", fg="white", activebackground="#be66e3",
                                      activeforeground="white", indicatoron=False)
        radio_button_window = canvas.create_window(150, 120 + (i * 40), window=radio_button)
        radio_buttons.append(radio_button)

    next_button = tk.Button(root, text="Next", width=20, height=2, command=next_question,  bg="#be66e3", fg="white",)
    next_button_window = canvas.create_window(image.width - 150, 250, window=next_button)

    show_question()

    root.mainloop()
