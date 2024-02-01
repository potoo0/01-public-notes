# import os
from tkinter import *
from tkinter import TclError
from tkinter import messagebox


class extractSubtitle():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("求和")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width=FALSE, height=FALSE)

        self.num1 = DoubleVar()
        self.num2 = DoubleVar()
        self.numSum = DoubleVar()

        Label(self.frame, text="加数1:",
              width=15, height=2).grid(row=0, column=0)
        Entry(self.frame, textvariable=self.num1,
              width=20).grid(row=0, column=1, columnspan=6)
        self.num1.set(0)

        Label(self.frame, text="加数2:",
              width=15, height=2).grid(row=1, column=0)
        Entry(self.frame, textvariable=self.num2,
              width=20).grid(row=1, column=1, columnspan=6)
        self.num2.set(0)

        Label(self.frame, text="和:",
              width=15, height=2).grid(row=2, column=0)
        Entry(self.frame, textvariable=self.numSum,
              width=20).grid(row=2, column=1, columnspan=6)
        self.numSum.set(0)

        Button(self.frame, text="计算",
               width=15, height=2,
               command=self.sums).grid(row=3, column=4)

        Button(self.frame, text="关闭",
               width=15, height=2,
               command=self.close_window).grid(row=3, column=5)

    def sums(self):
        try:
            num1 = self.num1.get()
            num2 = self.num2.get()
        except TclError as e:
            messages = str(e) + '\n' + '请输入数值！'
            messagebox.showinfo(title='showinfo', message=messages)
            return
        self.numSum.set(num1 + num2)

    def close_window(self):
        self.parent.destroy()


if __name__ == '__main__':
    root = Tk()
    tool = extractSubtitle(root)
    root.mainloop()

# pyinstaller -F -w py_path
# pyinstaller -F -w -i ico_path  py_path
