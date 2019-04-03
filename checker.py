import tkinter
import subprocess


def checkout(event):
    checkout_process = subprocess.run(
        ["git", "checkout", "задача-" + event.widget['text'].split(' ')[0]],
        stderr=subprocess.PIPE
    )
    text.insert(tkinter.END, checkout_process.stderr.decode('utf-8'))
    text.insert(tkinter.END, "-" * 50 + "\n")


def checkout_master():
    checkout_process = subprocess.run(
        ["git", "checkout", "master"],
        stderr=subprocess.PIPE
    )
    text.insert(tkinter.END, checkout_process.stderr.decode('utf-8'))
    text.insert(tkinter.END, "-" * 50 + "\n")


solvers = {
    "Никита Усатов": range(5),
    "Андрей": range(5, 9),
    "Никита Уткин": range(9, 13)
}


def get_solver(n):
    for s, r in solvers.items():
        if n in r:
            return s


tk = tkinter.Tk()

to_master = tkinter.Button(tk, text="(на master)", command=checkout_master)
to_master.grid(row=0, column=0)

for i in range(1, 13):
    b = tkinter.Button(tk, text=str(i) + " - " + get_solver(i), width=20)
    b.bind("<Button-1>", checkout)
    b.grid(row=i, column=0)

text = tkinter.Text(tk)
text.grid(row=0, column=1, rowspan=13)

tk.mainloop()
