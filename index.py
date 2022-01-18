import login_register
import staff
from tkinter import *
from tkinter import messagebox
import sqlite3
import os

is_login = False
uid = -1
user_name = ''
is_super = False

def begin():
    global is_login,uid,user_name,is_super
    win = Tk()
    while not is_login:
        login_register.win_init(win)
        is_login = login_register.init
        uid = login_register.uid
        user_name = login_register.user_name
        is_super = login_register.is_super

    if is_super:
        user = staff.super_user(user_name, uid)
    else:
        user = staff.user(user_name, uid)


    wins = Tk(className="仓库管理系统")  # 创建窗口类
    user_height = wins.winfo_screenheight()
    user_width = wins.winfo_screenwidth()
    wins.geometry('%dx%d' % ((user_width), (user_height)))
    Label(wins, text="仓库管理系统").grid(row=0, column=0, columnspan=6, padx=500, pady=20)
    Label(wins, text="欢迎你！%s" % user_name, anchor="e").grid(row=1, column=0, padx=500, pady=20)
    Button(wins, text='入库', width=60, command=user.in_warehouse).grid(row=2, column=0, padx=500, pady=20)
    Button(wins, text='出库', width=60, command=user.out_warehouse).grid(row=3, column=0, padx=500, pady=20)
    Button(wins, text='查看仓储物品数量', width=60, command=user.seek_goods).grid(row=4, column=0, padx=500, pady=20)
    if is_super:
        Button(wins, text='增加仓储管理人员', width=60, command=user.user_add).grid(row=5, column=0, padx=500, pady=20)
        Button(wins, text='删除仓储管理人员', width=60, command=user.user_del).grid(row=6, column=0, padx=500, pady=20)
        Button(wins, text='查看仓储物品修改记录', width=60, command=user.seek_record).grid(row=7, column=0, padx=500, pady=20)

    def user_logout():  # 用户注销
        if staff.is_here:
            messagebox.showerror(title='wrong', message='请先关闭其他二级窗口！')
        else:
            global uid,user_name,is_super,is_login
            login_register.logout()
            uid = login_register.uid
            user_name = login_register.user_name
            is_super = login_register.is_super
            is_login = False
            wins.destroy()
            begin()  # 重新调用主函数完成回到注册登录界面

    Button(wins, text='注销用户', width=60, command=user_logout).grid(row=8, column=0, padx=500, pady=20)  # command为关联函数
    wins.mainloop()

def init():
    #系统刚刚创建的时候负责创建数据库
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE USER
                               (ID         INT     NOT NULL ,
                               NAME         TEXT     NOT NULL,
                               PASSWORD     TEXT    NOT NULL,
                               TEL     TEXT    NOT NULL, 
                               STRESS     TEXT    NOT NULL);''')
    c.execute("INSERT INTO USER (ID,NAME,PASSWORD,TEL,STRESS) \
                                VALUES ( 0, '张三', 'admin', '12345678910', '幸福路28号');")

    ans = c.execute("SELECT * FROM USER")
    ans = ans.fetchall()
    c.execute('''CREATE TABLE SUPERUSER
                               (ID         INT     NOT NULL ,
                               NAME         TEXT     NOT NULL,
                               PASSWORD     TEXT    NOT NULL,
                               TEL     TEXT    NOT NULL, 
                               STRESS     TEXT    NOT NULL);''')
    c.execute("INSERT INTO SUPERUSER (ID,NAME,PASSWORD,TEL,STRESS) \
                                VALUES ( 0, 'admin', 'admin', '21345678910', '幸福路26号');")
    c.execute('''CREATE TABLE GOODS
                           (ID         INT     NOT NULL ,
                           TIMES         TEXT    NOT NULL,
                           NAME         TEXT     NOT NULL,
                           NUM          INT    NOT NULL,
                           USERS       TEXT     NOT NULL);''')
    c.execute("INSERT INTO GOODS (ID,NAME,TIMES,NUM,USERS) \
                            VALUES ( 0, '薯片','2021-12-28 21:43:48', 0, '张三');")
    c.execute('''CREATE TABLE GOODS_RECORD
                               (ID         INT     NOT NULL ,
                               TIMES         TEXT    NOT NULL,
                               GNAME         TEXT     NOT NULL,
                               GNUM          INT    NOT NULL,
                               USERS       TEXT     NOT NULL,
                               GWHERE       TEXT      NOT NULL, 
                               GGO          TEXT     NOT NULL );''')
    c.execute("INSERT INTO GOODS_RECORD (ID,GNAME,TIMES,GNUM,USERS,GWHERE,GGO) \
                                VALUES ( 0, '薯片','2021-12-28 21:43:48', 0, '张三','武当','少林');")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    if not os.path.exists('.\\test.db'):
        init()
    begin()





