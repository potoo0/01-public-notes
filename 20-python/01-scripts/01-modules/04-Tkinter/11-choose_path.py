import os
import tkinter as tk
from tkinter.filedialog import askdirectory
import tkinter.messagebox


def selectPath(dirph):
    path_ = askdirectory()
    # askdirectory()方法是返回文件夹路径不是文件路径
    if dirph is True:
        dirpath.set(path_)
    else:
        scriptpath.set(path_)


def trans():
    sp = scriptpath.get() + '/' + scriptname.get()
    dp = dirpath.get()
    if sp is '' or dp is '':
        tk.messagebox.showinfo(title='showinfo', message='请输入正确的路径')
    else:
        if os.path.exists(dp):
            for dirpath_, dirnames, filenames in os.walk(dp):
                for filename in filenames:
                    if filename.endswith('.py'):
                        fileFullName = os.path.join(dirpath_, filename)
                        print('Processing File:', fileFullName)
                        pycode2to3 = ("python " + sp + " -wn " +
                                      fileFullName)
                        print((os.popen(pycode2to3, 'r').read()))
        tk.messagebox.showinfo(title='showinfo', message='转化完成')


def close_window():
    root.destroy()


def instruction():
    messages1 = '注意: \n1. 本程序是通过调用官方所提供的2to3.py，故程序需要首先选择该文件的目录,以及输入它的文件名。'
    messages2 = '\n2. 在选择官方2to3文件目录后确认该目录名后无斜杠或者反斜杠。'
    message3 = '\n3. 选择需要python2转python3的文件所在目录。(该程序会转化目录下所有子目录及py文件)。'
    message4 = '\n\t\t\t\t\t ----2018.4.19'
    tk.messagebox.showinfo(title='说明',
                           message=messages1 + messages2 + message3 + message4)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('选择需要py2转py3的路径')
    scriptpath = tk.StringVar()
    scriptname = tk.StringVar()
    dirpath = tk.StringVar()

    tk.Label(root, text="官方2to3.py路径:").grid(row=0, column=0)
    tk.Entry(root, textvariable=scriptpath).grid(row=0, column=1, columnspan=3)
    scriptpath.set(r"D:/Anaconda3/Scripts")
    tk.Label(root, text="官方2to3文件名:").grid(row=1, column=0)
    tk.Entry(root, textvariable=scriptname).grid(row=1, column=1)
    scriptname.set(r"2to3-script.py")
    tk.Button(root, text="路径选择",
              command=lambda: selectPath(dirph=False)).grid(row=0, column=4)

    tk.Label(root, text="目标转化路径:").grid(row=2, column=0)
    tk.Entry(root, textvariable=dirpath).grid(row=2, column=1, columnspan=3)
    tk.Button(root, text="路径选择",
              command=lambda: selectPath(dirph=True)).grid(row=2, column=4)

    tk.Button(root, text="转换", command=trans).grid(row=3, column=1)

    tk.Button(root, text="关闭",
              command=close_window).grid(row=3, column=3)
    tk.Button(root, text="说明", command=instruction).grid(row=3, column=4)

    root.mainloop()
