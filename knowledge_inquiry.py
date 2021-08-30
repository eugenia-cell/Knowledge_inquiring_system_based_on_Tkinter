from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class inquiry():
    def __init__(self):
        self.inquiry_window=Toplevel()
        self.inquiry_window.title('python知识查询系统')
        width=640
        height=480
        #获取屏幕尺寸易计算布局参数，使窗口位于屏幕中央
        screenwidth=self.inquiry_window.winfo_screenwidth()
        screenheight=self.inquiry_window.winfo_screenheight()
        alignstr='%dx%d+%d+%d' %(width,height,(screenwidth-width)/2,(screenheight-height)/2)
        self.inquiry_window.geometry(alignstr)
        self.inquiry_window.resizable(width=False,height=True)
        self.linetext=StringVar()
        self.filemenu=StringVar()

        self.createpage()
        
    def createpage(self):
        
        logo=PhotoImage(file='source\search.png')
        self.search_logo=Label(self.inquiry_window,image=logo)
        self.search_logo.place(x=30, y=10, width=40, height=40)
        
        self.line_text=Entry(self.inquiry_window,textvariable=self.linetext) #单行文本输入
        self.line_text.place(x=80, y=10, width=300, height=30) 
        self.s_button = Button(self.inquiry_window,text='搜索', command=self.search)  
        self.s_button.place(x=390, y=10, width=60, height=30)

        
        self.file_menu=ttk.Combobox(self.inquiry_window, width=45, textvariable=self.filemenu)
        #下拉列表内容
        self.file_menu['values'] = ('概述与入门基础', '高级数据类型',
                                    '文件操作', '异常处理')
        self.file_menu.place(x=460, y=10, width=120, height=30)
        self.file_menu.current(0)  
        
        self.label2 = Label(self.inquiry_window,text='查询结果:')
        self.label2.place(x=10, y=100, width=80, height=20)
        
        self.text = Text(self.inquiry_window)  # 多行文本显示
        self.text.place(x=80, y=80, width=480, height=240)
        self.inquiry_window.mainloop()

    def search(self):
        if self.file_menu.current()==0:
            classfication='概述与入门基础'
        elif self.file_menu.current()==1:
            classfication= '高级数据类型'
        elif self.file_menu.current()==2:
            classfication= '文件操作'
        elif self.file_menu.current()==3:
            classfication= '异常处理'
        
        context=self.line_text.get()
        if context=='':
            messagebox.showinfo("warning",'查询内容不能为空')
            return
        conn=sqlite3.connect("knowledge_point.db")
        c=conn.cursor()
        c.execute("select * from knowledge where category=? and content like '%"+context+"%'",(classfication,)) 
        conn.commit()
        
        output=c.fetchall()
        if self.text.get(1.0,"end")!=' ':
            self.text.delete(1.0, "end")
        if output==[]:
            self.text.insert('insert','没有与之对应的知识点')
        else:
            self.text.insert('insert',output)
        conn.close()
        
class add_knowledge():
    def __init__(self):
        self.add_Window=Toplevel()
        self.add_Window.title('录入知识点')
        screenwidth=self.add_Window.winfo_screenwidth()
        screenheight=self.add_Window.winfo_screenheight()
        width=620
        height=370
        alignstr='%dx%d+%d+%d' %(width,height,(screenwidth-width)/2,(screenheight-height)/2)
        self.add_Window.geometry(alignstr)
        self.createpage()

    def createpage(self):

        self.category_label=Label(self.add_Window,text='请选择录入类别')
        self.category_label.place(x=145, y=10, width=300, height=30)
        self.entry_category=Entry(self.add_Window)
        self.entry_category.place(x=145, y=40, width=300, height=30)

        self.content_label=Label(self.add_Window,text='请输入新增知识点')
        self.content_label.place(x=145,y=80,width=300,height=30)
        self.entry_content=Entry(self.add_Window)
        self.entry_content.place(x=145,y=120,width=300,height=120)

        self.reserved_label=Label(self.add_Window,text='附件信息')
        self.reserved_label.place(x=145,y=240,width=300,height=30)
        self.entry_reserved=Entry(self.add_Window)
        self.entry_reserved.place(x=145,y=280,width=300,height=50)

        self.click_button=Button(self.add_Window,text="确认",command=self.add_point)
        self.click_button.place(x=250,y=340,width=80,height=20)
        self.add_Window.mainloop()

    def add_point(self):
        classfication=self.entry_category.get()
        context=self.entry_content.get()
        appendix=self.entry_reserved.get()
        conn=sqlite3.connect("knowledge_point.db")
        c=conn.cursor()
        c.execute('select count(id) FROM knowledge')

        id=int(c.fetchall()[0][0])+1
        sql="insert into knowledge values(?,?,?,?)"
        c.execute(sql,(id,classfication,context,appendix))

        '''
        以下语句可用于测试新知识点是否添加成功，根据屏幕的输出可以进行判断
        c.execute('select * FROM knowledge')
        print(c.fetchall())
        '''

        conn.commit()
        conn.close()

def create_schema():
    conn=sqlite3.connect("knowledge_point.db") #打开或创建数据库
    c=conn.cursor()
    sql=['' for x in range(16)]
    sql[0]='drop table  if exists knowledge'
    sql[1]='''
        
        CREATE TABLE knowledge
            (id int primary key not null,
            category text,
            content text,
            reserved text);
    '''
    sql[2]='''
        insert into knowledge(id,category,content,reserved)
        values(1,'概述与入门基础','Python是著名的“龟叔”Guido van Rossum在1989年圣诞节期间,为了打发无聊的圣诞节而编写的一个编程语言。',null);
        '''
    sql[3]='''
        insert into knowledge(id,category,content,reserved)
        values(2,'概述与入门基础','Python语言的特点 优点一：优雅、简单、明确;优点二：强大的标准库;优点三：良好的可扩展性;优点四：使用面向对象的方式',null);
        '''
    sql[4]='''
        insert into knowledge(id,category,content,reserved)
        values(3,'概述与入门基础','在Python中，等号=是赋值语句，可以把任意数据类型赋值给变量，同一个变量可以反复赋值，而且可以是不同类型的变量',null);
        '''
    sql[5]='''
        insert into knowledge(id,category,content,reserved)
        values(4,'概述与入门基础','python有五个标准数据类型：Number(数字)，String(字符串)，List(列表)， Tuple(组),dictionary(字典)。',null);
        '''
    sql[6]='''
        insert into knowledge(id,category,content,reserved)
        values(5,'高级数据类型','Python中的列表是有序可变序列，使用[]表示。由于列表是可变类型，所以可以对列表元素 进行一般的增删查改操作。',null);
        '''
    sql[7]='''
        insert into knowledge(id,category,content,reserved)
        values(6,'高级数据类型','Python中的tuple是不可变序列，使用()表示。由于元组是不可变类型，即元组一旦创建， 其中元素不能修改',null);
        '''
    sql[8]='''
        insert into knowledge(id,category,content,reserved)
        values(7,'高级数据类型','Python中的字典是无序可变序列，使用花括号表示。每个元素用一对“键-值”表示，即一个关键字和一个对应值，且由冒号(:)将键和值分隔。关键字在字典中是唯一的，每个关键字唯一地匹配一个值。',null);
        '''
    sql[9]='''
        insert into knowledge(id,category,content,reserved)
        values(8,'文件操作','最早的字符编码是美国信息交换码ASCII，只对大小写英文字母、数字和一些符号进行了编码。',null);
        '''
    sql[10]='''
        insert into knowledge(id,category,content,reserved)
        values(9,'文件操作','文件的一般操作过程：打开文件、读/写文 件、关闭文件。',null);
        '''
    sql[11]='''
        insert into knowledge(id,category,content,reserved)
        values(10,'文件操作','文件被打开后，其对象保存在变量中，它会记住文件的当前位置以便于执行读、写操作这个位置称为文件的指针。',null);
        '''
    sql[12]='''
        insert into knowledge(id,category,content,reserved)
        values(11,'文件操作','csv文件是用文本文件形式存储的表格数据， 逗号分隔值，任何编辑器都可打开；可以进行文件的一般操作过程。',null);
        '''
    sql[13]='''
        insert into knowledge(id,category,content,reserved)
        values(12,'异常处理','以高级语言通常都内置了一套 try...except...finally...的错误处理机制，Python也不例外。',null);
        '''
    sql[14]='''
        insert into knowledge(id,category,content,reserved)
        values(13,'异常处理','第一种方式没有except块,执行<body>代码,不管有没有异常执行finally块 • 第二种方式至少有except块，else和finally可选 • expression应该为 • 异常类 • 或者异常类的元组，表示其中任一异常出现',null);
        '''
    sql[15]='''
        insert into knowledge(id,category,content,reserved)
        values(14,'异常处理','如果错误没有被捕获，它就会一直往上抛，最后被Python解释器捕获，打印一个错误信息，然后程序退出。',null);
  
    '''

    for i in range(len(sql)):
        c.execute(sql[i])
    c.execute('select * from knowledge')   
    conn.commit()
    conn.close()
    print("succelfully create schema!")
    
if __name__ == '__main__':

    create_schema()
    root=Tk()
    root.title('python知识点系统')
    root.geometry("580x310")
    m=Menu(root)
    querymenu=Menu(m)
    addmenu=Menu(m)
    helpmenu=Menu(m)
    root.config(menu=m)
    root.iconbitmap('source\py.ico')
    m.add_command(label='查询',command=inquiry)
    m.add_command(label='新增',command=add_knowledge)
    m.add_command(label='退出',command=quit)
    
    homelogo=PhotoImage(file='source\python_home.png')
    home_logo=Label(root,image=homelogo)
    home_logo.place(x=10, y=10, width=480, height=270)
    
    greetings = "点 击 左 上 角 进 行: \n \n知 识 点 查 询 \n \n新 增 知 识 点 \n \n退 出 系 统 "
    msg = Message(root, text = greetings)
    msg.place(x=450,y=60,width=120,height=180)
    root.mainloop()

