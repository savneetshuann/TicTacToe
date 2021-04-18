from tkinter import ttk
import tkinter as tk
import sqlite3


def connect():
    con1 = sqlite3.connect('player_info.db')
    cur1 = con1.cursor()
    cur1.execute("CREATE TABLE IF NOT EXISTS players(user_name text, no_of_wins integer, points integer)")

    con1.commit()
    con1.close()


def View():
    con1 = sqlite3.connect('player_info.db')
    cur1 = con1.cursor()
    cur1.execute("Select user_name,no_of_wins,points from players")
    rows = cur1.fetchall()

    for row in rows:
        print(row)

        tree.insert("", tk.END, values=row)

    con1.close()

connect()

root = tk.Tk()

tree = ttk.Treeview(root, column=("c1", "c2", "c3"), show='headings')

tree.column("#1", anchor=tk.CENTER)

tree.heading("#1", text="NAME")

tree.column("#2", anchor=tk.CENTER)

tree.heading("#2", text="WINS")

tree.column("#3", anchor=tk.CENTER)

tree.heading("#3", text="POINTS")

tree.pack()

button1 = tk.Button(text="Display data", command=View)

button1.pack(pady=10)

root.mainloop()





