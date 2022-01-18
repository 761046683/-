from tkinter import *
from tkinter import Tk,ttk,messagebox
import sqlite3
import time

is_here = False #判断是否有二级窗口
pages = 1

class user:
    name: str
    uid: int


    def __init__(self, name, uid):
        self.name = name
        self.uid = uid     #创建员工所需的窗口

    def sqlite_secelect(self, something, where):
        #返回需要搜索的内容 仅适用于下拉框
        codes = []
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("SELECT %s FROM %s" % (something, where))
        anses = c.fetchall()[1:]
        conn.commit()
        conn.close()
        for j in anses:
            codes.append(j[0])
        codes = list(set(codes))
        codes.sort()
        codes = tuple(codes)
        return codes

    """def sqlite_in(self, where, somethings,nums):
        #somethings为（数据库表头名1，数据库表头名2，数据库表头名3... 插入值1，插入值2，插入值3...）
        length = int(len(somethings)/2) #获取需要添加的表头/值数量
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        text = "INSERT INTO " + where + '('
        for i in range(length):
            text = text + somethings[i]
            if i != length-1:
                text = text + ','
        text = text+(") VALUES (%d," % somethings[length])
        for i in range(length-1):
            if i == nums-2 and nums != 0:
                text = text + somethings[i+1+length]
            else:
                text = text + "'" + somethings[i+1+length] + "'"
            if i != length-2:
                text = text + ','
        text = text + ');'
        print(text)
        c.execute(text)
        conn.commit()
        conn.close()
        return True"""


    def in_warehouse(self):
        #入库操作
        global is_here
        if is_here:
            messagebox.showerror(title='wrong', message='请先关闭其他二级窗口！')
        else:
            is_here = True
            user_wins = Tk()
            user_wins.title('增加货物')
            user_height = user_wins.winfo_screenheight()
            user_width = user_wins.winfo_screenwidth()
            user_wins.geometry('350x150+%d+%d' % ((user_width-350)/2, (user_height-150)/2))
            Label(user_wins, text='请输入货物的名称：').grid(row=1, column=0)
            goods_name = Entry(user_wins)
            goods_name.grid(row=1, column=1)
            Label(user_wins, text='入库数量：').grid(row=2, column=0)
            nums = Entry(user_wins)
            nums.grid(row=2, column=1)
            Label(user_wins, text='货物来源：').grid(row=3, column=0)
            wheres = Entry(user_wins)
            wheres.grid(row=3, column=1)
            def customized_function():  # 窗口关闭绑定函数
                global is_here
                is_here = False
                user_wins.destroy()
            user_wins.protocol('WM_DELETE_WINDOW', customized_function)
            def sure_in():
                if not nums.get().isalnum():
                    messagebox.showerror(title='wrong', message='请输入正确的数量')
                else:
                    conn = sqlite3.connect('test.db')
                    c = conn.cursor()
                    id = c.execute("SELECT MAX(ID) FROM GOODS")
                    id = id.fetchall()
                    cs = conn.cursor()
                    cs.execute("SELECT NUM FROM GOODS WHERE NAME = '%s'" % goods_name.get())
                    anss = cs.fetchall()
                    count = 0
                    for i in anss:
                        count = count + 1
                    conn.commit()
                    conn.close()
                    if count == 0:
                        conn = sqlite3.connect('test.db')
                        c = conn.cursor()
                        c.execute("INSERT INTO GOODS(ID,NAME,TIMES,NUM,USERS) VALUES (%d,'%s','%s',%d,'%s');" % (id[0][0]+1, goods_name.get(),
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), int(nums.get()), self.name))
                        c.close()
                        conn.commit()
                        conn.close()
                    else:
                        gnum = anss[0][0]
                        conn = sqlite3.connect('test.db')
                        cc = conn.cursor()
                        cc.execute("UPDATE GOODS set NUM = %d WHERE NAME = '%s'" % (gnum+int(nums.get()),goods_name.get()))
                        conn.commit()
                        cc.close()
                        conn.close()

                    conn = sqlite3.connect('test.db')
                    c = conn.cursor()
                    id = c.execute("SELECT MAX(ID) FROM GOODS_RECORD")
                    id = id.fetchall()
                    c.close()
                    conn.commit()
                    conn.close()
                    conn = sqlite3.connect('test.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO GOODS_RECORD(ID,GNAME,TIMES,GNUM,USERS,GWHERE,GGO) VALUES (%d,'%s','%s',%d,'%s','%s',' ');" % (
                    id[0][0]+1, goods_name.get(),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), int(nums.get()), self.name, wheres.get()))
                    c.close()
                    conn.commit()
                    conn.close()
                    messagebox.showinfo(title='successful', message='添加成功！')
                    user_wins.destroy()
                    global is_here
                    is_here = False

            Button(user_wins, text='添加', command=sure_in).grid(row=4, column=0, columnspan=2)
            user_wins.mainloop()

    def out_warehouse(self):
        #出库操作
        global is_here
        if is_here:
            messagebox.showerror(title='wrong', message='请先关闭其他二级窗口！')
        else:
            is_here = True
            user_wins = Tk()
            user_height = user_wins.winfo_screenheight()
            user_width = user_wins.winfo_screenwidth()
            user_wins.geometry('350x150+%d+%d' % ((user_width-350)/2, (user_height-150)/2))
            user_wins.title('货物出库')
            Label(user_wins, text='请输入需要出库的货物名称：').grid(row=1, column=0, sticky=E)
            names = Entry(user_wins)
            names.grid(row=1, column=1)
            Label(user_wins, text='请输入需要出库的货物数量：').grid(row=2, column=0, sticky=E)
            nums = Entry(user_wins)
            nums.grid(row=2, column=1)
            Label(user_wins, text='请输入出库的货物去向：').grid(row=3, column=0, sticky=E)
            gos = Entry(user_wins)
            gos.grid(row=3, column=1)
            def customized_function():  # 窗口关闭绑定函数
                global is_here
                is_here = False
                user_wins.destroy()
            user_wins.protocol('WM_DELETE_WINDOW', customized_function)

            def seek_user():
                conn = sqlite3.connect('test.db')
                c = conn.cursor()
                c.execute("SELECT NUM FROM GOODS WHERE NAME='%s'" % names.get())
                ans = c.fetchall()
                count1 = 0
                conn.commit()
                c.close()
                conn.close()
                for i in ans:
                    count1 = count1 + 1
                if count1 != 0:
                    # 查询成功
                    gnum = ans[0][0]
                    if int(nums.get()) > gnum:
                        text = '库存数量不足，库存仅剩' + str(gnum) +'!'
                        messagebox.showerror(title='wrong', message=text)
                    else:
                        conn = sqlite3.connect('test.db')
                        c = conn.cursor()
                        c.execute("UPDATE GOODS set NUM = %d WHERE NAME = '%s'" % (gnum-int(nums.get()),names.get()))
                        conn.commit()
                        c.close()
                        conn.close()
                        conn = sqlite3.connect('test.db')
                        c = conn.cursor()
                        id = c.execute("SELECT MAX(ID) FROM GOODS_RECORD")
                        id = id.fetchall()
                        conn.commit()
                        conn.close()
                        conn = sqlite3.connect('test.db')
                        c = conn.cursor()
                        c.execute(
                            "INSERT INTO GOODS_RECORD(ID,GNAME,TIMES,GNUM,USERS,GWHERE,GGO) VALUES (%d,'%s','%s',%d,'%s',' ','%s');" % (
                                id[0][0]+1,names.get(),
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), int(nums.get()), self.name, gos.get()))
                        c.close()
                        conn.commit()
                        conn.close()
                        messagebox.showinfo(title='successful', message='已成功出库！')

                else:
                    # 查询失败
                    messagebox.showerror(title='successful', message='查找货物失败！请检查货物名称是否正确！')
                global is_here
                is_here = False
                user_wins.destroy()

            def backs():
                user_wins.destroy()


            Button(user_wins, text='货物出库', command=seek_user).grid(row=4, column=0, columnspan=2)
            user_wins.mainloop()

    def seek_goods(self):
        #查询仓储物品记录
        global pages,is_here
        if is_here:
            messagebox.showerror(title='wrong', message='请先关闭其他二级窗口！')
        else:
            is_here = True
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            c2 = conn.cursor()
            c.execute("SELECT * FROM GOODS WHERE ID=0")
            c2.execute("SELECT MAX(ID) FROM GOODS")
            ans = c.fetchall()
            num = c2.fetchall()[0][0] + 1
            conn.commit()
            c.close()
            conn.close()

            count = 0
            for i in ans:
                count = count + 1
            srecord = Tk(className="仓储物品信息")
            user_height = srecord.winfo_screenheight()
            user_width = srecord.winfo_screenwidth()
            srecord.geometry('1000x700+%d+%d' % ((user_width - 1000) / 2, (user_height - 700) / 2))

            def customized_function():  # 窗口关闭绑定函数
                global pages,is_here
                pages = 1
                is_here = False
                srecord.destroy()

            srecord.protocol('WM_DELETE_WINDOW', customized_function)
            if count == 0:
                messagebox.showerror(title='wrong', message='数据库数据为空！')
                is_here = False
                srecord.destroy()
            else:
                data = {'id': ans[0][0],'gname':ans[0][2],'gnum':ans[0][3],'ntime':ans[0][1],'user':ans[0][4]}
                Label(srecord, text="仓储物品id").grid(row=0, column=0, padx=20, pady=20)
                Label(srecord, text="仓储物品名称").grid(row=0, column=1, padx=20, pady=20)
                Label(srecord, text="仓储物品数量").grid(row=0, column=2, padx=20, pady=20)
                Label(srecord, text="上次修改时间").grid(row=0, column=3, padx=20, pady=20)
                Label(srecord, text="上次修改人员").grid(row=0, column=4, padx=20, pady=20)
                def print_form(data, num):
                    for i in range(5):
                        Label(srecord, text=data['id']).grid(row=i + 1, column=0, padx=20, pady=20)
                        Label(srecord, text=data['gname']).grid(row=i + 1, column=1, padx=20, pady=20)
                        Label(srecord, text=data['gnum']).grid(row=i + 1, column=2, padx=20, pady=20)
                        Label(srecord, text=data['ntime']).grid(row=i + 1, column=3, padx=20, pady=20)
                        Label(srecord, text=data['user']).grid(row=i + 1, column=4, padx=20, pady=20)
                        if pages == int((num - 1) / 5) + 1:
                            if i == (num - 1) % 5:
                                break
                        conn = sqlite3.connect('test.db')
                        c = conn.cursor()
                        ans = c.execute(
                            "SELECT * FROM GOODS WHERE ID=%d" % ((pages-1)*5+i+1))
                        ans = ans.fetchall()
                        conn.commit()
                        conn.close()
                        data = {'id': ans[0][0], 'gname': ans[0][2], 'gnum': ans[0][3], 'ntime': ans[0][1],
                                'user': ans[0][4]}
                print_form(data,num)  # 初始化显示第一页默认数据
                def previous_page():
                    global pages
                    if pages == 1:
                        messagebox.showerror(title='wrong', message='当前已经是第一页了！')
                    else:
                        pages -= 1
                        print_form(data, num)

                def next_page():
                    global pages
                    if pages == int((num - 1) / 5) + 1:
                        messagebox.showerror(title='wrong', message='当前已经是最后一页了！')
                    else:
                        pages += 1
                        print_form(data, num)
                pre_page = Button(srecord, text='上一页', width=15, command=previous_page)
                pre_page.grid(row=6, column=0, padx=20, pady=20)
                Label(srecord, text="%d/%d" % (pages, int((num - 1) / 5) + 1)).grid(row=6, column=1, padx=20, pady=20)
                nex_page = Button(srecord, text='下一页', width=15, command=next_page)
                nex_page.grid(row=6, column=2, padx=20, pady=20)
                back = Button(srecord, text='返回', width=15, command=customized_function)
                back.grid(row=6, column=3, padx=20, pady=20)







class super_user(user):
    #超级用户


    def user_add(self):
        #增加员工信息
        global is_here
        if is_here:
            messagebox.showerror(title='wrong', message='请先关闭其他二级窗口！')
        else:
            is_here = True
            main_add = Tk()
            main_add.title('增加仓储管理人员')
            user_width = main_add.winfo_screenwidth()
            user_height = main_add.winfo_screenheight()
            main_add.geometry('350x150+%d+%d' % ((user_width-350)/2, (user_height-150)/2))
            Label(main_add, text='增加仓储管理人员').grid(row=0, column=0, columnspan=2)
            Label(main_add, text='真实姓名：').grid(row=1, column=0, sticky=E)
            names = Entry(main_add)
            names.grid(row=1, column=1)
            Label(main_add, text='联系电话：').grid(row=2, column=0, sticky=E)
            tels = Entry(main_add)
            tels.grid(row=2, column=1)
            Label(main_add, text='家庭住址：').grid(row=3, column=0)
            stress = Entry(main_add)
            stress.grid(row=3, column=1)
            def customized_function():  # 窗口关闭绑定函数
                global is_here
                is_here = False
                main_add.destroy()
            main_add.protocol('WM_DELETE_WINDOW', customized_function)
            def registeredes():
                conn = sqlite3.connect('test.db')
                c = conn.cursor()
                c.execute("SELECT * FROM USER WHERE NAME='%s'" % names.get())
                ans = c.fetchall()
                count1 = 0
                conn.commit()
                c.close()
                conn.close()
                for i in ans:
                    count1 = count1 + 1
                global is_here
                if count1 != 0:
                    messagebox.showerror(title='wrong', message='添加失败，已存在同姓名成员，请在姓名前加任意数字以保证唯一性！')
                    is_here = False
                    main_add.destroy()
                elif len(tels.get()) != 11:
                    messagebox.showerror(title='wrong', message='添加失败，请输入正确的电话号码！')
                    is_here = False
                    main_add.destroy()
                else:
                    try:
                        conn = sqlite3.connect('test.db')
                        c = conn.cursor()
                        uid = c.execute("SELECT MAX(ID) FROM  USER")
                        uid = uid.fetchall()
                        c.execute("INSERT INTO USER (ID,NAME,PASSWORD,TEL,STRESS) \
                                VALUES (%d, '%s', '%s', '%s', '%s');" % (uid[0][0]+1, names.get(), "123456", tels.get(), stress.get()))
                        messagebox.showinfo(title='successful', message='增加仓储管理人员成功！')
                        conn.commit()
                        conn.close()
                    except Exception as err:
                        messagebox.showerror(title='wrong', message=err)
                    else:
                        is_here = False
                        main_add.destroy()

            Button(main_add, text='添加', command=registeredes).grid(row=4, column=0, columnspan=2)
            main_add.mainloop()

    def user_del(self):
        #删除员工账号
        global is_here
        if is_here:
            messagebox.showerror(title='wrong', message='请先关闭其他二级窗口！')
        else:
            is_here = True
            main_del = Tk()
            main_del.title('删除仓储管理人员')
            user_width = main_del.winfo_screenwidth()
            user_height = main_del.winfo_screenheight()
            main_del.geometry('350x150+%d+%d' % ((user_width-350)/2, (user_height-150)/2))
            main_del.resizable(False, False)  # 禁止改变大小
            Label(main_del, text='删除仓储管理人员').grid(row=0, column=0, columnspan=2)
            Label(main_del, text='请输入需要删除的仓储管理人员姓名：').grid(row=1, column=0, sticky=E)
            names = Entry(main_del)
            names.grid(row=1, column=1)
            def customized_function():  # 窗口关闭绑定函数
                global is_here
                is_here = False
                main_del.destroy()
            main_del.protocol('WM_DELETE_WINDOW', customized_function)
            def seek_user():
                conn = sqlite3.connect('test.db')
                c = conn.cursor()
                c.execute("SELECT * FROM USER WHERE NAME='%s'" % names.get())
                ans = c.fetchall()
                count1 = 0
                conn.commit()
                c.close()
                conn.close()
                for i in ans:
                    count1 = count1 + 1
                if count1 != 0:
                    # 查询成功
                    asking = Tk()
                    asking.title('确认删除提醒')
                    asking.geometry("300x200+%d+%d" % ((user_width-300)/2, (user_height-200)/2))
                    texts = "已找到" + names.get() + "的相关信息"
                    Label(asking, text=texts).grid(row=0, column=0, columnspan=3)
                    for i in ans:
                        text1 = "姓名：" + i[1]
                        text2 = "联系电话：" + i[3]
                        text3 = "地址" + i[4]
                        Label(asking, text=text1).grid(row=1, column=0)
                        Label(asking, text=text2).grid(row=1, column=1)
                        Label(asking, text=text3).grid(row=1, column=2)
                    Label(asking, text='确定删除吗？').grid(row=2, column=0, columnspan=3)

                    def real_del():
                        conn = sqlite3.connect('test.db')
                        c = conn.cursor()
                        c.execute("delete from USER where NAME = '%s'" % names.get())
                        conn.commit()
                        c.close()
                        conn.close()
                        messagebox.showinfo(title='successful', message='已成功删除！')
                        global is_here
                        is_here = False
                        asking.destroy()
                        main_del.destroy()


                    Button(asking, text='确认', command=real_del).grid(row=3, column=0)

                else:
                    # 查询失败
                    messagebox.showinfo(title='successful', message='查找仓储管理人员失败！请检查仓储人员姓名是否正确！')
                    global is_here
                    is_here = False
                    main_del.destroy()


            Button(main_del, text='查询需要删除的仓储管理人员', command=seek_user).grid(row=2, column=0, columnspan=2)
            main_del.mainloop()

    def seek_record(self):
        #查询仓储物品记录
        global pages, is_here
        if is_here:
            messagebox.showerror(title='wrong', message='请先关闭其他二级窗口！')
        else:
            is_here = True
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            c2 = conn.cursor()
            c.execute("SELECT * FROM GOODS_RECORD WHERE ID=0")
            c2.execute("SELECT MAX(ID) FROM GOODS_RECORD")
            ans = c.fetchall()
            num = c2.fetchall()[0][0] + 1
            conn.commit()
            c.close()
            conn.close()

            count = 0
            for i in ans:
                count = count + 1
            srecord = Tk(className="仓储物品记录")
            user_height = srecord.winfo_screenheight()
            user_width = srecord.winfo_screenwidth()
            srecord.geometry('1000x700+%d+%d' % ((user_width - 1000) / 2, (user_height - 700) / 2))

            def customized_function():  # 窗口关闭绑定函数
                global pages,is_here
                pages = 1
                is_here = False
                srecord.destroy()

            srecord.protocol('WM_DELETE_WINDOW', customized_function)
            if count == 0:
                messagebox.showerror(title='wrong', message='数据库数据为空！')
                is_here = False
                srecord.destroy()
            else:
                data = {'id': ans[0][0],'gname':ans[0][2],'gnum':ans[0][3],'ntime':ans[0][1],'user':ans[0][4],
                        'where': ans[0][5], 'go': ans [0][6]}
                Label(srecord, text="仓储物品id").grid(row=0, column=0, padx=20, pady=20)
                Label(srecord, text="仓储物品名称").grid(row=0, column=1, padx=20, pady=20)
                Label(srecord, text="仓储物品数量").grid(row=0, column=2, padx=20, pady=20)
                Label(srecord, text="时间").grid(row=0, column=3, padx=20, pady=20)
                Label(srecord, text="人员").grid(row=0, column=4, padx=20, pady=20)
                Label(srecord, text="来源").grid(row=0, column=5, padx=20, pady=20)
                Label(srecord, text="去向").grid(row=0, column=6, padx=20, pady=20)
                def print_form(data, num):
                    for i in range(5):
                        Label(srecord, text=data['id']).grid(row=i + 1, column=0, padx=20, pady=20)
                        Label(srecord, text=data['gname']).grid(row=i + 1, column=1, padx=20, pady=20)
                        Label(srecord, text=data['gnum']).grid(row=i + 1, column=2, padx=20, pady=20)
                        Label(srecord, text=data['ntime']).grid(row=i + 1, column=3, padx=20, pady=20)
                        Label(srecord, text=data['user']).grid(row=i + 1, column=4, padx=20, pady=20)
                        Label(srecord, text=data['where']).grid(row=i + 1, column=5, padx=20, pady=20)
                        Label(srecord, text=data['go']).grid(row=i + 1, column=6, padx=20, pady=20)
                        if pages == int((num - 1) / 5) + 1:
                            if i == (num - 1) % 5:
                                break
                        conn = sqlite3.connect('test.db')
                        c = conn.cursor()
                        ans = c.execute("SELECT * FROM GOODS_RECORD WHERE ID=%d" % ((pages-1)*5+i+1))
                        ans = ans.fetchall()
                        conn.commit()
                        conn.close()
                        data = {'id': ans[0][0], 'gname': ans[0][2], 'gnum': ans[0][3], 'ntime': ans[0][1],
                                'user': ans[0][4], 'where': ans[0][5], 'go': ans [0][6]}

                print_form(data,num)  # 初始化显示第一页默认数据
                def previous_page():
                    global pages
                    if pages == 1:
                        messagebox.showerror(title='wrong', message='当前已经是第一页了！')
                    else:
                        pages -= 1
                        print_form(data, num)

                def next_page():
                    global pages
                    if pages == int((num - 1) / 5) + 1:
                        messagebox.showerror(title='wrong', message='当前已经是最后一页了！')
                    else:
                        pages += 1
                        print_form(data, num)
                pre_page = Button(srecord, text='上一页', width=15, command=previous_page)
                pre_page.grid(row=6, column=0, padx=20, pady=20)
                Label(srecord, text="%d/%d" % (pages, int((num - 1) / 5) + 1)).grid(row=6, column=1, padx=20, pady=20)
                nex_page = Button(srecord, text='下一页', width=15, command=next_page)
                nex_page.grid(row=6, column=2, padx=20, pady=20)
                back = Button(srecord, text='返回', width=15, command=customized_function)
                back.grid(row=6, column=3, padx=20, pady=20)


