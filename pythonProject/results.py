import sqlite3
import tkinter as tk
from PIL import Image, ImageTk

def show_results(user_name, user_surname, score):

    result_window = tk.Tk()
    result_window.geometry("800x600")


    image_path = "image.jpg"
    try:
        print("Trying to load image...")
        image = Image.open(image_path)
        image = image.resize((800, 600), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        print("Image loaded successfully!")
    except Exception as e:
        print(f"Error loading image: {e}")
        result_window.destroy()
        return


    canvas = tk.Canvas(result_window, width=image.width, height=image.height)
    canvas.pack(fill=tk.BOTH, expand=True)


    canvas.create_image(0, 0, anchor="nw", image=photo)


    canvas.image = photo


    result_label = tk.Label(result_window, text=f"{user_name} {user_surname}\nScore: {score}",
                            font=("Arial", 16), fg="black", bg="white")
    result_label.place(relx=0.5, rely=0.1, anchor="n")


    exit_button = tk.Button(result_window, text="Exit", width=30, height=2, bg="#be66e3", fg="white", font=("Arial", 14), command=result_window.quit)
    exit_button.place(relx=0.5, rely=0.9, anchor="center")


    def show_top_scorers():
        top_scorers_window = tk.Toplevel(result_window)
        top_scorers_window.title("Top Scorer(s)")


        try:
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()

            cursor.execute(''' 
                SELECT DISTINCT p.first_name, p.last_name, g.score, ts.domain1
                FROM player p
                JOIN game g ON p.idgame = g.idgame
                JOIN test t ON g.idset = t.idset
                JOIN test_set ts ON t.idset = ts.idset
                WHERE g.score = (SELECT MAX(score) FROM game)
            ''')
            top_players = cursor.fetchall()
            conn.close()

            players_text = "Top Scorer(s):\n\n"
            if top_players:
                for player in top_players:
                    name, surname, score, domain = player
                    players_text += f"{name} {surname}\nScore: {score}\nDomain: {domain}\n\n"
            else:
                players_text = "No top scorers found."


            players_label = tk.Label(top_scorers_window, text=players_text, font=("Arial", 12), bg="white", fg="black")
            players_label.pack(padx=20, pady=20)


            close_button = tk.Button(top_scorers_window, text="Close", width=20, height=2, font=("Arial", 12), command=top_scorers_window.destroy)
            close_button.pack(pady=10)

        except Exception as e:
            print(f"Error fetching top scorers: {e}")


    def show_players():
        players_window = tk.Toplevel(result_window)
        players_window.title("Players List")

        try:
            print("Trying to load image in players window...")
            image = Image.open(image_path)
            image = image.resize((400, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            print("Image loaded successfully for players window!")
        except Exception as e:
            print(f"Error loading image for players window: {e}")
            players_window.destroy()
            return


        players_canvas = tk.Canvas(players_window, width=image.width, height=image.height)
        players_canvas.pack(fill=tk.BOTH, expand=True)
        players_canvas.create_image(0, 0, anchor="nw", image=photo)
        players_canvas.image = photo


        try:
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT first_name, last_name FROM player")
            players = cursor.fetchall()
            conn.close()

            players_text = "List of Players:\n\n"
            if players:
                for player in players:
                    players_text += f"{player[0]} {player[1]}\n"
            else:
                players_text = "No players found."

            players_label = tk.Label(players_window, text=players_text, font=("Arial", 12), bg="white", fg="black")
            players_label.place(relx=0.5, rely=0.4, anchor="center")
        except Exception as e:
            print(f"Error fetching players from the database: {e}")


        close_button = tk.Button(players_window, text="Close", width=20, height=2, font=("Arial", 12), command=players_window.destroy)
        close_button.place(relx=0.5, rely=0.85, anchor="center")


    def show_total_players():
        try:
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM player")
            total_players = cursor.fetchone()[0]
            conn.close()

            total_window = tk.Toplevel(result_window)
            total_window.title("Total Players")
            total_label = tk.Label(total_window, text=f"Total Number of Players: {total_players}", font=("Arial", 16), bg="white", fg="black")
            total_label.pack(padx=20, pady=20)

            close_total_button = tk.Button(total_window, text="Close", width=20, height=2, font=("Arial", 12), command=total_window.destroy)
            close_total_button.pack(pady=10)
        except Exception as e:
            print(f"Error fetching total players: {e}")


    def show_mathematics_section():
        mathematics_window = tk.Toplevel(result_window)
        mathematics_window.title("Mathematics Section Players")

        try:
            print("Trying to load image in mathematics window...")
            image = Image.open(image_path)
            image = image.resize((400, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            print("Image loaded successfully for mathematics section!")
        except Exception as e:
            print(f"Error loading image for mathematics section window: {e}")
            mathematics_window.destroy()
            return


        mathematics_canvas = tk.Canvas(mathematics_window, width=image.width, height=image.height)
        mathematics_canvas.pack(fill=tk.BOTH, expand=True)
        mathematics_canvas.create_image(0, 0, anchor="nw", image=photo)
        mathematics_canvas.image = photo

        try:
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            cursor.execute(''' 
                SELECT DISTINCT p.first_name, p.last_name
                FROM player p
                JOIN game g ON p.idgame = g.idgame
                JOIN test t ON g.idset = t.idset
                JOIN test_set ts ON t.idset = ts.idset
                WHERE ts.domain1 = 'mathematics'
            ''')
            players_in_mathematics = cursor.fetchall()
            conn.close()

            players_text = "Players who took the Mathematics test:\n\n"
            if players_in_mathematics:
                for player in players_in_mathematics:
                    players_text += f"{player[0]} {player[1]}\n"
            else:
                players_text = "No players found in Mathematics section."

            players_label = tk.Label(mathematics_window, text=players_text, font=("Arial", 12), bg="white", fg="black")
            players_label.place(relx=0.5, rely=0.4, anchor="center")
        except Exception as e:
            print(f"Error fetching mathematics players: {e}")


        close_button = tk.Button(mathematics_window, text="Close", width=20, height=2, font=("Arial", 12), command=mathematics_window.destroy)
        close_button.place(relx=0.5, rely=0.85, anchor="center")

    def show_informatics_section():
        informatics_window = tk.Toplevel(result_window)
        informatics_window.title("Informatics Section Players")

        try:
            print("Trying to load image in informatics window...")
            image = Image.open(image_path)
            image = image.resize((400, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            print("Image loaded successfully for informatics section!")
        except Exception as e:
            print(f"Error loading image for informatics section window: {e}")
            informatics_window.destroy()
            return


        informatics_canvas = tk.Canvas(informatics_window, width=image.width, height=image.height)
        informatics_canvas.pack(fill=tk.BOTH, expand=True)
        informatics_canvas.create_image(0, 0, anchor="nw", image=photo)
        informatics_canvas.image = photo


        try:
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            cursor.execute(''' 
                SELECT DISTINCT p.first_name, p.last_name
                FROM player p
                JOIN game g ON p.idgame = g.idgame
                JOIN test t ON g.idset = t.idset
                JOIN test_set ts ON t.idset = ts.idset
                WHERE ts.domain1 = 'informatics'
            ''')
            players_in_informatics = cursor.fetchall()
            conn.close()

            players_text = "Players who took the Informatics test:\n\n"
            if players_in_informatics:
                for player in players_in_informatics:
                    players_text += f"{player[0]} {player[1]}\n"
            else:
                players_text = "No players found in Informatics section."

            players_label = tk.Label(informatics_window, text=players_text, font=("Arial", 12), bg="white", fg="black")
            players_label.place(relx=0.5, rely=0.4, anchor="center")
        except Exception as e:
            print(f"Error fetching informatics players: {e}")


        close_button = tk.Button(informatics_window, text="Close", width=20, height=2, font=("Arial", 12), command=informatics_window.destroy,bg="#be66e3", fg="white")
        close_button.place(relx=0.5, rely=0.85, anchor="center")


    top_scorer_button = tk.Button(result_window, text="Top Scorer(s)", width=20, height=2, font=("Arial", 12), command=show_top_scorers,bg="#be66e3", fg="white")
    top_scorer_button.place(relx=0.5, rely=0.3, anchor="center")

    players_button = tk.Button(result_window, text="Players List", width=20, height=2, font=("Arial", 12), command=show_players,bg="#be66e3", fg="white")
    players_button.place(relx=0.5, rely=0.4, anchor="center")

    total_players_button = tk.Button(result_window, text="Total Players", width=20, height=2, font=("Arial", 12), command=show_total_players,bg="#be66e3", fg="white")
    total_players_button.place(relx=0.5, rely=0.5, anchor="center")

    mathematics_button = tk.Button(result_window, text="Mathematics Section", width=20, height=2, font=("Arial", 12), command=show_mathematics_section,bg="#be66e3", fg="white")
    mathematics_button.place(relx=0.5, rely=0.6, anchor="center")

    informatics_button = tk.Button(result_window, text="Informatics Section", width=20, height=2, font=("Arial", 12), command=show_informatics_section,bg="#be66e3", fg="white")
    informatics_button.place(relx=0.5, rely=0.7, anchor="center")


    result_window.mainloop()


