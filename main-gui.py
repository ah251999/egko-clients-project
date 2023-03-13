import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import platform
import datetime as dt

# import arabic_reshaper
# from bidi.algorithm import get_display
# from awesometkinter.bidirender import add_bidi_support

def clear_search():

    frst_wrd_ent.delete(0,'end')

    sec_wrd_ent.delete(0,'end')

    if cli_n:
        inserting_records_data(cli_n,None,None)
    else:
        inserting_records_data(None,None,None)

def arng_client_by_latest_rowid():
    try:
        selected_row_from_tree = myt.item(myt.focus(), 'values')

        global cli_n
        cli_n = selected_row_from_tree[1]

        records_list(cli_n)
    except AttributeError:
        warning_msg()
    except IndexError:
        warning_msg()


def change_delay_to_paid():

    selected_row_from_tree = myt.item(myt.focus(), 'values')
    
    if selected_row_from_tree[-1] == "0":
        
        change_dely_cash(selected_row_from_tree[0])
        
        change_client_credit(1,selected_row_from_tree[1],selected_row_from_tree[5])
        
        conn.commit()
        
        inserting_records_data(None,None,None)
        
    else:
        messagebox.showinfo(message="Error")


def delete_from_recof_tknpro():

    selected_row_from_tree = myt.item(myt.focus(), 'values')

    if selected_row_from_tree[-1] == '0':
        change_client_credit(1, selected_row_from_tree[1], selected_row_from_tree[-3])
    
    c.execute('DELETE FROM recof_tknpro WHERE rowid = ?', (selected_row_from_tree[0],))
    
    conn.commit()
    
    inserting_records_data(None,None,None)


def add_recof_takenpro():
    try:
        # ﻓﻰ ﺻﻔﺤﺔ ﺗﺴﺠﻴﻞ ﺑﻨﺪ ﻋﻠﻰ اﻟﻌﻤﻴﻞ اﻟﻤﺴﻠﺴﻞ ﺑﺘﺎﻉ اﻟﺒﻨﺪ ﺑﻴﻀﺎﻑ ﻟﻮﺣﺪﻩ
# ﻭاﺳﻢ اﻟﻌﻤﻴﻞ ﺑﻴﻜﻮﻥ ﺑﺘﺎﺧﺪ ﻣﻦ اﻟﺼﻔﺤﺔ اﻟﺮﺋﻴﺴﻴﺔ        
#اﻟﻤﻄﻠﻮﺏ ﻫﻨﺎ اﺩﺧﺎﻝ اﺳﻢ اﻟﺒﻨﺪ ﻭﻛﻤﻴﺘﻪ ﻭاﻟﺴﻌﺮ اﻻﺟﻤﺎﻟﻰ ﻭاﻟﺒﺮﻧﺎﻣﺞ ﻫﻴﺴﺠﻞ ﺳﻌﺮ اﻟﻮاﺣﺪ         

        def add_prorecord():
            price_per_unit = int(sum_ent.get()) // int(quantity_ent.get())
            add_record_values = (real_name, proname_ent.get(), price_per_unit,
                             quantity_ent.get(),
                             sum_ent.get(), dt.datetime.now().strftime("%d-%m-%Y %H:%M"),radi.get(),)
            c.execute('INSERT INTO recof_tknpro(client,product,price,quantity,sum,tkn_time,dely_cash) '
                  'VALUES (?,?,?,?,?,?,?)', add_record_values)

            if radi.get() == 0:
                change_client_credit(0, real_name, sum_ent.get())
            else:
                pass
        
            conn.commit()
        
            proname_ent.delete(0, 'end')
            quantity_ent.delete(0, 'end')
            sum_ent.delete(0, 'end')
        
            records_list(None)
        
            proname_ent.focus_set()
        
        real_name = myt.item(myt.focus(), 'values')[1]
        
        new_takenpro_win = tk.Tk()
        new_takenpro_win.title('ﺗﺴﺠﻴﻞ ﺑﻴﻊ ﺑﻨﺪ')
        
        clientname_lab = tk.Label(new_takenpro_win, text=':اﻟﻌﻤﻴﻞ', font=16)
        clientname_lab.grid(row=0,column=2,pady=5)
        clientname_real = tk.Label(new_takenpro_win, text=real_name, font=('bold',20), fg='green',justify='right')
        clientname_real.grid(row=0,column=1,pady=5)

        proname_lab = tk.Label(new_takenpro_win, text=':اﻟﻤﻨﺘﺞ', font=16, justify='right')
        proname_lab.grid(row=1,column=2,pady=5)
        proname_ent = tk.Entry(new_takenpro_win,font=15,width=25,justify='right')
        proname_ent.grid(row=1,column=1,pady=5)

        quantity_lab = tk.Label(new_takenpro_win, text=':اﻟﻜﻤﻴﺔ', font=16)
        quantity_lab.grid(row=2,column=2,pady=5)
        quantity_ent = tk.Entry(new_takenpro_win,font=15,justify='right',width=5)
        quantity_ent.grid(row=2,column=1,pady=5)

        sum_lab = tk.Label(new_takenpro_win, text=':اﻻﺟﻤﺎﻟﻰ', font=16)
        sum_lab.grid(row=3,column=2,pady=5)
        sum_ent = tk.Entry(new_takenpro_win,font=15,justify='right',width=5)
        sum_ent.grid(row=3,column=1,pady=5)

        radi = tk.IntVar(new_takenpro_win)

        radio_delay = tk.Radiobutton(new_takenpro_win, text='ﺁﺟﻞ', variable=radi, value=0,font=18)
        radio_delay.grid(row=4,column=2,pady=5)

        radio_cash = tk.Radiobutton(new_takenpro_win, text='ﻧﻘﺪا', variable=radi, value=1,font=18)
        radio_cash.grid(row=4,column=1,pady=5)
        
        reg_record_but = tk.Button(new_takenpro_win, text='ﺗﺴﺠﻴﻞ', command=add_prorecord,width=5,font=('Bold',16),height=2)
        reg_record_but.grid(row=5,column=2,pady=5,padx=12)

        cancel_but = tk.Button(new_takenpro_win, text='ﺇﻟﻐﺎء', command=new_takenpro_win.destroy,width=5,font=('Bold',16),height=2)
        cancel_but.grid(row=5,column=1,pady=5)

        # add_bidi_support(proname_ent)
        proname_ent.focus_set()
    except AttributeError:
        warning_msg()
    except IndexError:
        warning_msg()



def add_new_client():
    def add_record():
        add_record_values = (name_ent.get(), money_ent.get(),)
        c.execute('INSERT INTO clients VALUES (?,?)', add_record_values)
        conn.commit()
        name_ent.delete(0, 'end')
        money_ent.delete(0, 'end')
        # success_msg()
        clients_list()
        name_ent.focus_set()

    new_client_win = tk.Tk()
    new_client_win.title('New client')
    new_client_win.geometry('360x90')

    name_lab = tk.Label(new_client_win, text='Name:', font=16)
    name_lab.grid(column=0, row=1, padx=5, pady=5)
    name_ent = tk.Entry(new_client_win,justify='right')
    name_ent.grid(column=1, row=1, padx=5, pady=5)

    money_lab = tk.Label(new_client_win, text='Money:', font=16)
    money_lab.grid(column=0, row=2, padx=5, pady=5)
    money_ent = tk.Entry(new_client_win,justify='right')
    money_ent.grid(column=1, row=2, padx=5, pady=5)

    reg_record_but = tk.Button(new_client_win, text='Register', command=add_record, width=7)
    reg_record_but.grid(column=3, row=1, padx=5, pady=5)

    cancel_but = tk.Button(new_client_win, text='Cancel', command=new_client_win.destroy, width=7)
    cancel_but.grid(column=3, row=2, padx=5, pady=5)

    name_ent.focus_set()


def change_client_credit(add_remove, client_name, credit_change):
    
    #ﺑﻴﺰﻭﺩ اﻟﻘﻴﻤﺔ اﻟﻤﺪﺧﻠﺔ ﻋﻠﻰ ﺣﺴﺎﺏ اﻟﻌﻤﻴﻞ
    if add_remove == 0:
        
        c.execute('SELECT credit FROM clients WHERE name = ?', (client_name,))
        current_credit = c.fetchone()

        new_credit = current_credit[0] + int(credit_change)
        
        c.execute('UPDATE clients SET credit = ? WHERE name = ?', (new_credit, client_name,))

    #ﺑﻴﻄﺮﺡ اﻟﻘﻴﻤﺔ اﻟﻤﺪﺧﻠﺔ ﻣﻦ ﺣﺴﺎﺏ اﻟﻌﻤﻴﻞ
    elif add_remove == 1:
        
        c.execute('SELECT credit FROM clients WHERE name = ?', (client_name,))
        current_credit = c.fetchone()
        
        new_credit = current_credit[0] - int(credit_change.replace(',', ''))
        
        c.execute('UPDATE clients SET credit = ? WHERE name = ?', (new_credit, client_name,))


def clients_list():

    myt['columns'] = ('id', 'name', 'money')
    myt.column('#0', width=0, stretch=False)
    myt.column('id', width=35, anchor='center')
    myt.column('name', width=150, anchor='center')
    myt.column('money', width=100, anchor='center')

    myt.heading('#0', text='')
    myt.heading('id', text='ID', anchor='center')
    myt.heading('name', text='Name', anchor='center')
    myt.heading('money', text='Money', anchor='center')

    inserting_clients_data()

    myt_frame.place(x=5, y=5, height=570, width=550)
    myt_scrollbar.pack(side='right',fill='y')
    myt.pack(side='left',fill='both')

    show_current_table_lab.config(text='اﻟﻌﻤﻼء')
    add_new_product_but.config(text='ﺗﺴﺠﻴﻞ ﺑﻴﻊ ﺑﻨﺪ',command=add_recof_takenpro)
    clients_and_rec_but.config(text='ﺟﺪﻭﻝ اﻟﺒﻨﻮﺩ', command=lambda: records_list(None))
    clients_record_but.config(state='normal')
    add_new_client_but.config(state='normal')
    remove_record_but.config(state='disabled')
    search_frame.place_forget()
    global cli_n
    cli_n = None



def records_list(vari_for_insert):
    myt['columns'] = ('id', 'client', 'product', 'price', 'quantity', 'pricesum', 'tkn_time')
    myt.column('#0', width=0, stretch=False)
    myt.column('id', width=35, anchor='center')
    myt.column('client', width=120, anchor='center')
    myt.column('product', width=230, anchor='center')
    myt.column('price', width=60, anchor='center')
    myt.column('quantity', width=60, anchor='center')
    myt.column('pricesum', width=70, anchor='center')
    myt.column('tkn_time', width=220, anchor='center')

    myt.heading('#0', text='')
    myt.heading('id', text='ID', anchor='center')
    myt.heading('client', text='Client', anchor='center')
    myt.heading('product', text='Product', anchor='center')
    myt.heading('price', text='PPU', anchor='center')
    myt.heading('quantity', text='Qnt', anchor='center')
    myt.heading('pricesum', text='Sum', anchor='center')
    myt.heading('tkn_time', text='Time', anchor='center')

    inserting_records_data(vari_for_insert,None,None)

    myt_frame.place(x=5, y=5, height=570, width=695)
    myt_scrollbar.pack(side='right',fill='y')
    myt.pack(side='left',fill='both')

    show_current_table_lab.config(text='اﻟﺒﻨﻮﺩ')
    add_new_product_but.config(text='ﺩﻓﻊ ﺃﺟﻞ',command=change_delay_to_paid)
    clients_and_rec_but.config(text='ﺟﺪﻭﻝ اﻟﻌﻤﻼء',command=clients_list)
    clients_record_but.config(state='disabled')
    add_new_client_but.config(state='disabled')
    remove_record_but.config(state='normal')
    search_frame.place(x=750,y=400)


# check if the selected record has been bought in cash or delay
def delay_cash(record_id):
    c.execute('SELECT dely_cash FROM recof_tknpro WHERE rowid = ?', (record_id,))
    return c.fetchone()[0]


#ﺗﻐﻴﻴﺮ اﻟﺼﻒ(اﻟﺴﺠﻞ) ﻣﻦ اﺟﻞ اﻟﻰ ﻣﺪﻓﻮﻉ
#ﻋﻦ ﻃﺮﻳﻖ ﺗﻐﻴﻴﺮ ﻗﻴﻤﺔ اﺧﺮ ﻋﻤﻮﺩ ﻣﻦ 0 اﻟﻰ 1
def change_dely_cash(record_id):
    c.execute('UPDATE recof_tknpro SET dely_cash = ? WHERE rowid = ?', (1,record_id,))

def inserting_records_data(client_name,frst_wrd,sec_wrd):
    for item in myt.get_children():
        myt.delete(item)


    if client_name and frst_wrd:
        c.execute("select rowid, * from recof_tknpro where client = ?"
                  " and product like ? and product like ?",(client_name,'%' + frst_wrd + '%','%' + sec_wrd + '%',))
    elif not client_name and frst_wrd:
        c.execute("select rowid, * from recof_tknpro where product like ? and product like ?",
                  ('%' + frst_wrd + '%','%' + sec_wrd + '%',))
    elif client_name and not frst_wrd:
        c.execute('select rowid,* from recof_tknpro where client = ? order by rowid desc', (client_name,))
    else:
        c.execute('select rowid,* from recof_tknpro order by rowid desc')

    for rec_num, rec_rows in enumerate(c.fetchall()):
        rec_mylist = list(rec_rows)
        rec_mylist[-3] = "{:,}".format(rec_mylist[-3])

        # ca2c2c:red----Blue----ffffff:grey
        myt.tag_configure('delay_strip1', foreground='#ca2c2c', background='white')
        myt.tag_configure('delay_strip2', foreground='#ca2c2c', background='#d9d9d9')
        myt.tag_configure('cash_strip1', foreground='blue', background='white')
        myt.tag_configure('cash_strip2', foreground='blue', background='#d9d9d9')

        if delay_cash(rec_mylist[0]) == 0:
            if rec_num % 2 == 0:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='delay_strip1')
            else:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='delay_strip2')
        if delay_cash(rec_mylist[0]) == 1:
            if rec_num % 2 == 0:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='cash_strip1')
            else:
                myt.insert(parent='', index=rec_num, text='', values=rec_mylist, tags='cash_strip2')


def inserting_clients_data():
    for item in myt.get_children():
        myt.delete(item)

    c.execute('select rowid,* from clients')

    for cli_num, cli_rows in enumerate(c.fetchall()):
        cli_mylist = list(cli_rows)
        cli_mylist[-1] = "{:,}".format(cli_mylist[-1])
        myt.insert(parent='', index=cli_num, text='', values=cli_mylist)


def warning_msg():
    # get_arabic_display = arabic_reshaper.reshape('ﺗﻤﺖ اﻟﻌﻤﻠﻴﺔ ﺑﻨﺠﺎﺡ')
    # messagebox.showinfo(title='good', message=get_display(get_arabic_display))
    tk.messagebox.showwarning(title='!اﻧﺘﺒﻪ', message='.اﻟﺮﺟﺎء اﺧﺘﻴﺎﺭ ﻋﻤﻴﻞ ﻣﻦ اﻟﺠﺪﻭﻝ')


# sqlite3 activator
conn = sqlite3.connect("clients-database.db")

c = conn.cursor()
c.execute('select rowid,* from clients')

cli_n = None

root = tk.Tk()
root.title('Main')
root.geometry('1100x580')

myst = ttk.Style()

#mytst.


myt_frame = tk.Frame(root)

myt_scrollbar = tk.Scrollbar(myt_frame,width=18)

myt = ttk.Treeview(myt_frame,yscrollcommand=myt_scrollbar.set)
myt_scrollbar.config(command=myt.yview)

clients_and_rec_but = tk.Button(root, text='ﺟﺪﻭﻝ اﻟﺒﻨﻮﺩ',font=('Bold',25))
clients_and_rec_but.place(x=890,y=12)

clients_record_but = tk.Button(root, text='ﺳﺠﻞ اﻟﻌﻤﻴﻞ', command=arng_client_by_latest_rowid,font=('bold',20))
clients_record_but.place(x=720,y=23)

show_current_table_lab = tk.Label(root, text='اﻟﻌﻤﻼء', font=('Bold',45),fg='green',justify='right')
show_current_table_lab.place(x=840, y=110)


#records_but = tk.Button(root, text='Products list', command=records_list,font=25,width=20,height=7)
#records_but.place(x=710, y=70)

#ﻛﻮﺩ اﻹﻃﺎﺭ
#=======================================================================
search_frame = tk.LabelFrame(root,text='ﺑﺤﺚ ﺑﻜﻠﻤﺘﻴﻦ',labelanchor='ne',font=('Bold',15))

frst_wrd_lab = tk.Label(search_frame,text=':اﻟﻜﻠﻤﺔ اﻷﻭﻟﻰ',justify='right',font=('Bold',15))
frst_wrd_lab.grid(row=0,column=2,pady=3)

sec_wrd_lab = tk.Label(search_frame,text=':اﻟﻜﻠﻤﺔ اﻟﺜﺎﻧﻴﺔ',justify='right',font=('Bold',15))
sec_wrd_lab.grid(row=1,column=2,pady=3)

frst_wrd_ent = tk.Entry(search_frame,justify='right',font=('Bold',15),width=12)
frst_wrd_ent.grid(row=0,column=1,pady=3)

sec_wrd_ent = tk.Entry(search_frame,justify='right',font=('Bold',15),width=12)
sec_wrd_ent.grid(row=1,column=1,pady=3)

search_but = tk.Button(search_frame,text='ﺑﺤﺚ',font='Bold',width=3,command=lambda: inserting_records_data(cli_n,frst_wrd_ent.get()
                                                                                      ,sec_wrd_ent.get()))
search_but.grid(row=0,column=0,pady=3,padx=3)

clear_but = tk.Button(search_frame,text='ﻣﺴﺢ اﻟﻤﺪﺧﻼﺕ',font='Bold',command=clear_search)
clear_but.grid(row=1,column=0,pady=3,padx=3)
#=======================================================================

#اﻃﺎﺭ اﻟﺰﺭاﻳﺮ
#=======================================================================
but_frame = tk.Frame(root)
but_frame.place(x=840,y=200)

add_new_product_but = tk.Button(but_frame, text='ﺗﺴﺠﻴﻞ ﺑﻴﻊ ﺑﻨﺪ', command=add_recof_takenpro,font=('bold',15))
add_new_product_but.grid(row=1,column=0,pady=6)

add_new_client_but = tk.Button(but_frame, text='ﺇﺿﺎﻓﺔ ﻋﻤﻴﻞ ﺟﺪﻳﺪ', command=add_new_client,font=('bold',15))
add_new_client_but.grid(row=2,column=0,pady=6)

remove_record_but = tk.Button(but_frame, text='ﺇﺯاﻟﺔ(ﻣﺮﺗﺠﻊ) ﺑﻨﺪ',
            command=delete_from_recof_tknpro, fg='red',font=('bold',15))
remove_record_but.grid(row=3,column=0,pady=6)
#=======================================================================

clients_list()

root.mainloop()
