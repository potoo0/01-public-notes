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
            usrs_info = pickle.load(usr_file)
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
    def sign_to_Mofanpy():
        # 以下三行就是获取我们注册时所输入的信息
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()

        # 这里是打开我们记录数据的文件，将注册信息读出
        with open('usr_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)

        if np != npf:
            # 这里判断，如果两次密码输入不一致，则提示
            mes = 'Password and confirm password must be the same!'
            tk.messagebox.showerror('Error', mes)
        elif nn in exist_usr_info:
            # 如果用户名已经在我们的数据文件中，则提示
            tk.messagebox.showerror('Error', 'The user has already signed up')
        else:
            # 如果输入无以上错误，则将注册输入的信息记录到文件当中，并提示注册成功
            exist_usr_info[nn] = np
            with open('usr_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tk.messagebox.showinfo('Welcome', 'You has successfully signed up')
            window_sign_up.destroy()

    # 在主体窗口的window上创建一个Sign up window窗口
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('Sign up window')

    new_name = tk.StringVar()
    new_name.set('example@python.com')
    tk.Label(window_sign_up, text='User name:').place(x=10, y=10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password:').place(x=10, y=50)
    entry_new_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_new_pwd.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Password:').place(x=10, y=90)
    entry_new_pwd_confirm = tk.Entry(window_sign_up,
                                     textvariable=new_pwd_confirm, show='*')
    entry_new_pwd_confirm.place(x=150, y=90)

    btn_confirm_sign_up = tk.Button(window_sign_up, text='Sign up',
                                    command=sign_to_Mofanpy)
    btn_confirm_sign_up.place(x=150, y=130)


# login and sign up button
btn_login = tk.Button(window, text='Login', command=usr_login)
btn_login.place(x=170, y=230)

btn_sign_up = tk.Button(window, text='sign up', command=usr_sign_up)
btn_sign_up.place(x=270, y=230)

window.mainloop()
