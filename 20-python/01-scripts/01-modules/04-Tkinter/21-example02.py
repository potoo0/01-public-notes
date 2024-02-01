import tkinter as tk
import pickle
import tkinter.messagebox

window = tk.Tk()
window.title('Welcome to Mofan Python')
window.geometry('450x300')

# welcome image  画布
canvas = tk.Canvas(window, height=200, width=500)
image_file = tk.PhotoImage(file='welcome.gif')
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

# user information
tk.Label(window, text='User name:').place(x=50, y=150)
tk.Label(window, text='Password:').place(x=50, y=190)

# entry
var_usr_name = tk.StringVar()    # 定义变量
var_usr_name.set('example@python.com')    # 变量赋值'example@python.com'
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)

var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)


def usr_login():
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    try:
        # 这里设置异常捕获，第一次访问用户信息文件时是不存在的
        # 下面的两行就是我们的匹配，即程序将输入的信息和文件中的信息匹配。
        with open('usr_info.pickle', 'rb') as usr_file:
            usrs_info = {'admin': 'admin'}
    except FileNotFoundError:
        # 这里就是我们在没有读取到`usr_file`的时候，程序会创建一个`usr_file`这个文件，
        # 并将管理员的用户和密码写入，即用户名为`admin`密码为`admin`。
        with open('usr_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)

    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title='Welcome',
                                   message='hello?' + usr_name)
        else:
            tk.messagebox.showerror(title='Error',
                                    message='your passwd is wrong, try again!')
    else:
        mes = 'You have not sign up yet. Sign up now?'
        is_sign_up = tk.messagebox.askyesno(title='Welcome',
                                            message=mes)

        if is_sign_up:
            usr_sign_up()


def usr_sign_up():
    pass


# button
btn_login = tk.Button(window, text='Login', command=usr_login)
btn_login.place(x=170, y=230)

btn_sign_up = tk.Button(window, text='sign up', command=usr_sign_up)
btn_sign_up.place(x=270, y=230)

window.mainloop()
