import win32ui
from tkinter.filedialog import *

# win32ui
dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
dlg.DoModal()
filename1 = dlg.GetPathName()  # 获取选择的文件名称
print(filename1)

# tkinter
filename2 = askopenfilename(initialdir='E:/')
print(filename2)
