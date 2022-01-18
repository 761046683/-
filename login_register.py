# -*- coding:utf-8 -*-
from tkinter import *
from tkinter import messagebox, ttk
import sqlite3

init = False  #判断是否登录
uid = -1
user_name = ''
is_super = False

def win_init(win):
    win.title('用户登录')
    user_height = win.winfo_screenheight()
    user_width = win.winfo_screenwidth()
    win.geometry('300x150+%d+%d' % ((user_width-300)/2, (user_height-150)/2))
    win.resizable(False, False)    #禁止改变大小
    win.maxsize(user_width, user_height)
    Label(win,text='用户登录').grid(row=0,column=0,columnspan=2)
    Label(win,text='用户名：').grid(row=1,column=0)
    name = Entry(win)
    name.grid(row=1,column=1)
    Label(win,text='密码：').grid(row=2,column=0)
    passwd = Entry(win,show='*')
    passwd.grid(row=2,column=1)
    def super_user_login():
        global uid, user_name, init,is_super
        try:
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            ans = c.execute("SELECT * FROM SUPERUSER WHERE NAME='%s'" % name.get())
            ans = ans.fetchall()
            count = 0
            for i in ans:
                count = count + 1
            if count == 0:
                messagebox.showerror(title='wrong', message='登录失败，用户名不存在')
            elif name.get() == ans[0][1] and passwd.get() == ans[0][2]:
                if ans[0][0] >= 0:
                    messagebox.showinfo(title='successful', message='登录成功')
                    uid = ans[0][0]
                    user_name = ans[0][1]
                    init = True
                    is_super = True
                    win.destroy()
                else:
                    messagebox.showerror(title='wrong', message='登录失败，用户id获取失败，请重试')
            else:
                messagebox.showerror(title='wrong', message='登录失败，用户名或密码错误')
            conn.commit()
            c.close()
            conn.close()
        except Exception as err:
            messagebox.showerror(title='wrong', message=err)
        else:
            pass
    def user_login():   #用户登录函数
        global uid,user_name,init
        try:
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            ans = c.execute("SELECT * FROM USER WHERE NAME='%s'" % name.get())
            ans = ans.fetchall()
            count = 0
            for i in ans:
                count = count + 1
            if count == 0:
                messagebox.showerror(title='wrong', message='登录失败，用户名不存在')
            elif name.get() == ans[0][1] and passwd.get() == ans[0][2]:
                if ans[0][0] >= 0:
                    messagebox.showinfo(title='successful', message='登录成功')
                    uid = ans[0][0]
                    user_name = ans[0][1]
                    init = True
                    win.destroy()
                else:
                    messagebox.showerror(title='wrong', message='登录失败，用户id获取失败，请重试')
            else:
                messagebox.showerror(title='wrong', message='登录失败，用户名或密码错误')
            conn.commit()
            c.close()
            conn.close()
        except Exception as err:
            messagebox.showerror(title='wrong', message=err)
        else:
            pass



    login1 = Button(win, text='仓储管理人员登录', width=20, command=user_login)    #command为关联函数
    login1.grid(row=3, column=0,columnspan=2)
    login2 = Button(win, text='超级成员登录', width=20, command=super_user_login)    #command为关联函数
    login2.grid(row=4, column=0,columnspan=2)
    win.mainloop()

def logout():
    global init,uid,user_name,is_super
    init = False
    uid = -1
    user_name = ''
    is_super = False

