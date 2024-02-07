import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter.scrolledtext import ScrolledText
from time import strftime

todos = {}

def detailTodo(cb=None):
    win = tk.Toplevel()
    win.wm_title("Detail Todo")
    win.configure(bg='blue')
    tanggal = str(cal.selection_get())
    selectedItem = treev.focus()
    selectedIndex = treev.item(selectedItem)['text']
    selectedTodo = todos[tanggal][selectedIndex]
    judul = tk.StringVar(value=selectedTodo['judul'])
    tk.Label(win, text="Tanggal:", bg='blue', fg='white', font='bold').grid(row=0, column=0, sticky='N')
    tk.Label(win, text="{} | {}".format(tanggal, selectedTodo['waktu']), bg='blue', font='Arial 11', fg='white').grid(row=0, column=1, sticky='E')
    tk.Label(win, text="Judul:", bg='blue', fg='white', font='bold').grid(row=1, column=0, sticky='N')
    tk.Entry(win, state="disabled", textvariable=judul).grid(row=1, column=1, sticky="E")
    tk.Label(win, text="Keterangan:", bg='blue', fg='white', font='bold').grid(row=2, column=0, sticky='N')
    keterangan = ScrolledText(win, width=12, height=5)
    keterangan.grid(row=2, column=1, sticky='E')
    keterangan.insert(tk.INSERT, selectedTodo['keterangan'])
    keterangan.configure(state='disabled')

def LoadTodos():
    global todos
    f = open('mytodo.dat','r')
    data = f.read()
    f.close()
    todos = eval(data)
    ListTodo()

def SaveTodos():
    f = open('mytodo.dat','w')
    f.write(str(todos))
    f.close()

def delTodo():
    tanggal = str(cal.selection_get())
    selectedItem = treev.focus()
    todos[tanggal].pop(treev.item(selectedItem)['text'])
    ListTodo()

def ListTodo(cb=None):
    for i in treev.get_children():
        treev.delete(i)
    tanggal = str(cal.selection_get())
    if tanggal in todos:
        for i in range(len(todos[tanggal])):
            treev.insert("","end", text=i, values=(todos[tanggal][i]['waktu'], todos[tanggal][i]['judul']))

def addTodo(win, key, jam, menit, judul, keterangan):
    newTodo = {
        'waktu':'{}:{}'.format(jam.get(), menit.get()),
        'judul': judul.get(),
        'keterangan': keterangan.get('1.0', tk.END)
    }
    if key in todos:
        todos[key].append(newTodo)
    else:
        todos[key] = [newTodo]
    win.destroy()
    ListTodo()   

def AddForm():
    win = tk.Toplevel()
    win.wm_title("+")
    win.configure(bg='blue')
    jam = tk.IntVar(value=10)
    menit = tk.IntVar(value=30)
    judul = tk.StringVar(value="")
    tk.Label(win, text="Waktu:",bg='blue', fg='white', font='bold').grid(row=0, column=0)
    tk.Spinbox(win, from_=0, to=23, textvariable=jam, width=3).grid(row=0, column=1)
    tk.Spinbox(win, from_=0, to=59, textvariable=menit, width=3).grid(row=0, column=2)
    tk.Label(win, text="Judul:",bg='blue', fg='white', font='bold').grid(row=1, column=0)
    tk.Entry(win, textvariable=judul).grid(row=1, column=1, columnspan=2)
    tk.Label(win, text="Keterangan:",bg='blue', fg='white', font='bold').grid(row=2, column=0)
    keterangan = ScrolledText(win, width=12, height=5)
    keterangan.grid(row=2, column=1, columnspan=2, rowspan=4)
    tanggal = str(cal.selection_get())
    tk.Button(win, text="Tambah", bg='green', fg='yellow', font='Arial 9 bold', command=lambda: addTodo(win, tanggal, jam, menit, judul, keterangan)).grid(row=6, column=0)

def title():
    waktu = strftime('%H:%M')
    tanggal = str(cal.selection_get())
    root.title(tanggal + " | " + waktu + " | My Todo")
    root.after(1000, title)

root = tk.Tk()
s = ttk.Style()
s.configure('Treeview', rowheight=16)
s.configure('Treeview.Heading', font=('Arial', 13,'bold'))
root.title("Calenderku")

cal = Calendar(root, font='Arial 14 italic bold', selectmode='day', locale='id_ID', cursor='hand2',background='blue', foreground='white', headersbackground='yellow',headersforeground='red', weekendforeground='red', weekendbackground='white', selectbackground='cyan', selectforeground='black')
cal.grid(row=0, column=0, sticky='N', rowspan=7, columnspan=2)
cal.bind("<<CalendarSelected>>", ListTodo)
tanggal = str(cal.selection_get())
treev = ttk.Treeview(root)
treev.grid(row=17, column=0, sticky="WNE", rowspan=4, columnspan=2)
scrollBar = tk.Scrollbar(root, orient='vertical', command=treev.yview)
scrollBar.grid(row=17, column=1, sticky="ENS", rowspan=4)
treev.configure(yscrollcommand=scrollBar.set)
treev.bind("<Double-1>", detailTodo)
treev['columns'] = ("1","2")
treev['show'] = 'headings'
treev.column("1", width=100)
treev.heading("1", text="Jam")
treev.heading("2", text="Judul")

btnAdd = tk.Button(root, text="Tambah", width=12, command=AddForm, bd=3, bg='green', fg='yellow', font='Arial 9 bold')
btnAdd.grid(row=21, column=0, sticky="WN")

btnDel = tk.Button(root, text="Hapus", width=11, command=delTodo, bd=3, bg='green', fg='yellow', font='Arial 9 bold')
btnDel.grid(row=21, column=0, sticky="NE")

btnLoad = tk.Button(root, text="Load", width=12, command=LoadTodos, bd=3, bg='green', fg='yellow', font='Arial 9 bold')
btnLoad.grid(row=21, column=1, sticky="WN")

btnSave = tk.Button(root, text="Save", width=11, command=SaveTodos, bd=3, bg='green', fg='yellow', font='Arial 9 bold')
btnSave.grid(row=21, column=1, sticky="NE")

title()
root.mainloop()