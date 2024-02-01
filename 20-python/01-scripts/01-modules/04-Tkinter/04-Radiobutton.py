import tkinter as tk

window = tk.Tk()
window.title('04-Radiobutton')
window.geometry('200x200')

var = tk.StringVar()
la = tk.Label(window, bg='yellow', width=20)
la.pack()


def print_selection():
    la.config(text='you have selection ' + var.get())


r1 = tk.Radiobutton(window,
                    text='Option A',
                    variable=var, value='A',
                    command=print_selection)
r1.pack()
r2 = tk.Radiobutton(window,
                    text='Option B',
                    variable=var, value='B',
                    command=print_selection)
r2.pack()
r3 = tk.Radiobutton(window,
                    text='Option C',
                    variable=var, value='C',
                    command=print_selection)
r3.pack()
r4 = tk.Radiobutton(window,
                    text='Option D',
                    variable=var, value='D',
                    command=print_selection)
r4.pack()

window.mainloop()
