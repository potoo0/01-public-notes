import tkinter as tk
from tkinter import messagebox


window = tk.Tk()
window.title('06-canvas')
window.geometry('200x200')


def hit_me():
    # 前三个都会返回 'ok'
    messagebox.showinfo(title='showinfo', message='info')
    # messagebox.showwarning(title='showwarning', message='warning')
    # messagebox.showerror(title='showerror', message='error')
    # return 'yes' , 'no'
    print(messagebox.askquestion(title='answer', message='yes or no？'))
    # 下面三个都会返回 True, False
    # print(messagebox.askyesno(title='Hi', message='hahahaha'))
    # print(messagebox.asktrycancel(title='Hi', message='hahahaha'))
    # print(messagebox.askokcancel(title='Hi', message='hahahaha'))
    # 返回 True, False, None
    # print(messagebox.askyesnocancel(title="Hi", message="haha"))


tk.Button(window, text='hit me', command=hit_me).pack()

window.mainloop()
