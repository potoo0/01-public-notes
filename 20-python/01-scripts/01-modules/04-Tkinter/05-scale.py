import tkinter as tk

window = tk.Tk()
window.title('05-checkbutton')
window.geometry('200x200')

la = tk.Label(window, bg='yellow', width=20)    # 此处width计量单位是字符的长宽
la.pack()


def print_selection():
    if((var1.get() == 1) & (var2.get() == 0)):
        la.config(text='I love only Python')
    elif((var1.get() == 0) & (var2.get() == 1)):
        la.config(text='I love only C++')
    elif((var1.get() == 0) & (var2.get() == 0)):
        la.config(text='I do not love either')
    elif((var1.get() == 1) & (var2.get() == 1)):
        la.config(text='I love both')


var1 = tk.IntVar()
var2 = tk.IntVar()
c1 = tk.Checkbutton(window, text='Python',
                    variable=var1,
                    onvalue=1, offvalue=0,      # 选定这个选项var1等于1，否则等于0
                    command=print_selection
                    )
c2 = tk.Checkbutton(window, text='C++',
                    variable=var2,
                    onvalue=1, offvalue=0,      # 选定这个选项var2等于1，否则等于0
                    command=print_selection
                    )
c1.pack()
c2.pack()

window.mainloop()
