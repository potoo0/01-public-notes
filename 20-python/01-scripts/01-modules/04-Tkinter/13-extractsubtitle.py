import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


class extractSubtitle():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("提取字幕")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width=FALSE, height=FALSE)

        self.filepath = StringVar()
#         self.dirpath = StringVar()
        self.line_begin = IntVar()
        self.line_end = IntVar()

        Label(self.frame, text="字幕文件路径:").grid(row=0, column=0)
        Entry(self.frame, textvariable=self.filepath,
              width=40).grid(row=0, column=1, columnspan=4)
        self.filepath.set(r"E:/Machine_learning/0-机器学习吴恩达/srt/" +
                          "1 - 4 - Unsupervised Learning (14 min).srt")
        Button(self.frame, text="选择字幕",
               command=self.getFile).grid(row=0, column=5)

        Label(self.frame, text="字幕起始位置:").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.line_begin,
              width=10).grid(row=1, column=1)
        self.line_begin.set(1)

        Label(self.frame, text="字幕结束位置:").grid(row=1, column=2)
        Entry(self.frame, textvariable=self.line_end,
              width=10).grid(row=1, column=3)
        self.line_end.set(10)

        Button(self.frame, text="提取", command=self.trans).grid(row=1, column=4)

        Button(self.frame, text="关闭",
               command=self.close_window).grid(row=1, column=5)

        self.txt_en = Text(self.frame, height=3, width=60)
        self.txt_en.grid(row=2, column=0, columnspan=6)

        self.txt_cn = Text(self.frame, height=3, width=60)
        self.txt_cn.grid(row=3, column=0, columnspan=6)

    def getFile(self):
        self.path_ = askopenfilename(
            initialdir='E:/Machine_learning/0-机器学习吴恩达/srt/')
        self.filepath.set(self.path_)

    def trans(self):
        filepath = self.filepath.get()
#         dp = self.dirpath.get()
        if not os.path.exists(filepath):
            messagebox.showinfo(title='showinfo', message='请输入正确的路径')
        else:
            # --------------提取范围内字幕------------------
            items = []
            with open(filepath, 'r', encoding='utf-8') as file:
                for index in range(self.line_end.get()):
                    if index >= self.line_begin.get() - 1:
                        items.append(file.readline())
                    else:
                        file.readline()

            # -----------------合并字幕--------------------
            subtitle_en = ''
            subtitle_cn = ''
            for i in range((len(items) + 1) // 5):
                subtitle_en += items[2 + 5 * i].strip() + ' '
                subtitle_cn += items[3 + 5 * i].strip() + '，'
            self.txt_en.delete('1.0', 'end')
            self.txt_cn.delete('1.0', 'end')
            self.txt_en.insert('insert', subtitle_en)
            self.txt_cn.insert('insert', subtitle_cn)

    def close_window(self):
        self.parent.destroy()


if __name__ == '__main__':
    root = Tk()
    tool = extractSubtitle(root)
    root.mainloop()

# pyinstaller -F -w py_path
# pyinstaller -F -w -i ico_path  py_path
