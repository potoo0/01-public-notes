import os
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import messagebox


class reNameFiles():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("文件批量重命名")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width=FALSE, height=FALSE)

        self.filePath = StringVar()
        self.fileName = StringVar()
        self.startNum = IntVar()
        self.fileExt = StringVar()
        self.prev = BooleanVar()

        Label(self.frame, text="待重命名文件路径:").grid(row=0, column=0)
        Entry(self.frame, textvariable=self.filePath,
              width=25).grid(row=0, column=1, columnspan=3)
        Button(self.frame, text="路径选择",
               command=self.selectPath).grid(row=0, column=4)

        Label(self.frame, text="文件名:").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.fileName,
              width=20).grid(row=1, column=1)

        Label(self.frame, text="起始序号:").grid(row=2, column=0)
        Entry(self.frame, textvariable=self.startNum,
              width=5).grid(row=2, column=1)
        self.startNum.set(1)

        Label(self.frame, text="限定格式:").grid(row=2, column=2)
        Entry(self.frame, textvariable=self.fileExt,
              width=8).grid(row=2, column=3)

        Button(self.frame, text="说明",
               command=self.instruction).grid(row=3, column=4)

        Button(self.frame, text="预览结果",
               command=self.preview).grid(row=3, column=0)
        self.prev.set(False)

        Button(self.frame, text="重命名",
               command=self.reName).grid(row=3, column=1)

        Button(self.frame, text="关闭",
               command=self.close_window).grid(row=3, column=3)

        self.info = Text(self.frame, height=5, width=60)
        self.info.grid(row=4, column=0, columnspan=6)

    def selectPath(self):
        path = askdirectory()
        self.filePath.set(path)
        self.fileName.set(os.path.split(path)[1] + ' ')

    def nameConstruct(self):
        path = self.filePath.get()
        names = self.fileName.get()
        st = self.startNum.get()
        fileExt = self.fileExt.get()

        if not os.path.exists(path):
            messagebox.showerror(title='error', message='请输入正确的路径')
            return 0
        if names == '':
            messagebox.showerror(title='error', message='请输入正确的命名规则')
            return 0
        if st < 0:
            messagebox.showerror(title='error', message='起始数字不能小于0')
            return 0

        fileNames = list(os.walk(path))[0][2]
        fileNames.sort(key=len)
        if fileExt == '':
            fileExt = os.path.splitext(fileNames[0])[1]
            self.fileExt.set(fileExt)

        fileNums = len(fileNames)
        cnt = 1
        nums = fileNums + st - 1
        
        maxLen = 6
        if nums % maxLen >= 9:
            cnt += 1
        while True:
            div = nums // maxLen
            if div != 0:
                nums = div
                cnt += 1
            else:
                break

        nameConstructed = []
        for (fileName, index) in zip(fileNames, range(st, fileNums + st)):
            if fileName.endswith(fileExt):
                newName = names + '%0.{}d'.format(cnt) % index + fileExt
                nameConstructed.append((fileName, newName))
        return nameConstructed

    def preview(self):
        nameConstructed = self.nameConstruct()
        if nameConstructed == 0:
            return 0
        self.info.insert('insert', '\n预览结果:\n')
        while True:
            try:
                fileName, newName = nameConstructed.pop(0)
                self.info.insert('insert', '%s --> %s\n' % (fileName, newName))
            except IndexError:
                break
        self.prev.set(1)

    def reName(self):
        path = self.filePath.get()
        nameConstructed = self.nameConstruct()
        if nameConstructed == 0:
            return 0
        if not self.prev.get():
            askyesno = messagebox.askyesno(
                title='Sure?',
                message='重命名后不可恢复, 是否预先查看效果再确认重命名?')
            if askyesno:
                self.info.insert(
                    'insert',
                    'prev: ' + str(self.prev.get()) +
                    '\n askyesno: ' + str(askyesno))
                return 0
        self.info.insert('insert', '\n开始重命名ing...\n')
        while True:
            try:
                fileName, newName = nameConstructed.pop(0)
                origPath = os.path.join(path, fileName)
                newPath = os.path.join(path, newName)
                self.info.insert('insert',
                                 '%s --> %s\n' % (fileName, newName))
                os.rename(origPath, newPath)
            except IndexError:
                break
        # os.rename(origPath, newPath)

    def instruction(self):
        intro = '- 重命名选定目录下所有文件，只命令同一格式的文件。\n'
        description = '''\n说明: \n\t1. 重命名的规则为在输入的文件名后追加序号, 默认为文件夹的名字;
        \t2. 可设置起始序号自定义, 如从 4 开始;
        \t3. 可指定文件格式，默认为第一个文件的格式。\n'''
        warning = '\n注意: 重命名后不能还原, 故推荐先预览结果再重命名。\n'
        version = '\n\t\t\t\t\t ----2019.2.10'
        messagebox.showinfo(title='说明',
                            message=intro + description + warning + version)

    def close_window(self):
        self.parent.destroy()


if __name__ == '__main__':
    root = Tk()
    tool = reNameFiles(root)
    root.mainloop()

# pyinstaller -F -w py_path
# pyinstaller -F -w -i ico_path  py_path
