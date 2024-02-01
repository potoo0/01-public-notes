import tkinter as tk

window = tk.Tk()
window.title('06-canvas')
window.geometry('200x200')

tk.Label(window, text='on the window').pack()

# 在`window`上创建一个`frame`
frm = tk.Frame(window)
frm.pack()
# 在刚刚创建的`frame`上创建两个`frame`，我们可以把它理解成一个
# 大容器里套了一个小容器，即`frm`上有两个`frame` ，`frm_l`和`frm_r`
frm_l = tk.Frame(frm)
frm_r = tk.Frame(frm)
# 这里是控制小的`frm`部件在大的`frm`的相对位置，
# 此处`frm_l`就是在`frm`的左边，`frm_r`在`frm`的右边
frm_l.pack(side='left')
frm_r.pack(side='right')

# 这里的三个label就是在我们创建的frame上定义的label部件
tk.Label(frm_l, text='on the frm_l1').pack()
# 这个`label`长在`frm_l`上，显示为`on the frm_l2`
tk.Label(frm_l, text='on the frm_l2').pack()
tk.Label(frm_r, text='on the frm_r1').pack()

window.mainloop()
