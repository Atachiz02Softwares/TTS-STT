import csv
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import *

from tkcalendar import DateEntry

# Database
conn = sqlite3.connect("npcregister.db")
c = conn.cursor()


def creatTable():
    c.execute(
        'CREATE TABLE IF NOT EXISTS userdata(FileNumber TEXT, DepartmentFrom TEXT, DepartmentTo TEXT, TransitionColumn TEXT, Date TEXT, '
        'SubjectMatter TEXT, StaffNumber REAL)')


def addDetails(fileNumber, departmentFrom, departmentTo, transitionColumn, date, subjectMatter, staffNumber):
    c.execute('INSERT INTO userdata(fileNumber, departmentFrom, departmentTo, transitionColumn, date, subjectMatter, '
              'staffNumber) VALUES (?,?,?,?,?,?,?)',
              (fileNumber, departmentFrom, departmentTo, transitionColumn, date, subjectMatter, staffNumber))
    conn.commit()


def viewAllUsers():
    c.execute('SELECT * FROM userdata')
    data = c.fetchall()
    for row in data:
        tree.insert("", tk.END, values=row)


def getSingleUser(fileNumber):
    c.execute(f'SELECT * FROM userdata WHERE fileNumber = "{fileNumber}"')
    # c.execute(f'SELECT * FROM userdata WHERE firstName = "{fileNumber}"'.format(fileNumber))
    data = c.fetchall()
    return data


def clearText():
    fileNumber.delete('0', END)
    departmentFrom.delete('0', END)
    departmentTo.delete('0', END)
    transitionColumn.delete('0', END)
    date.delete('0', END)
    subjectMatter.delete('0', END)
    staffNumber.delete('0', END)


def addData():
    fileN = str(fileNumber.get())
    deptF = str(departmentFrom.get())
    deptT = str(departmentTo.get())
    trans = str(transitionColumn.get())
    d = str(date.get())
    sub = str(subjectMatter.get(1.0, "end-1c"))
    num = str(staffNumber.get())
    addDetails(fileN, deptF, deptT, trans, d, sub, num)
    result = f"File Number:{fileN}, \nDepartment From:{deptF}, \nDepartment To:{deptT}, \nTransition Column:{trans}, \nDate:{d}, " \
             f"\nSubject Matter:{sub}, \nStaff Number:{num} "
    homeDisplay.insert(END, result)
    messagebox.showinfo("Success", "Record added to database successfully!")


def clearDisp():
    homeDisplay.delete("1.0", END)


def searchUser():
    fileNumber = str(seach.get())
    result = getSingleUser(fileNumber)
    # c.execute(f'SELECT * FROM userdata WHERE firstName = "{firstName}"')
    # data = c.fetchall()
    # print(data)
    searchDisplay.insert(END, result)


def clearSearch():
    seach.delete("0", END)


def clearResult():
    searchDisplay.delete("1.0", END)


def clearTable():
    for item in tree.get_children():
        tree.delete(item)
    messagebox.showinfo("Clear", "Table cleared!")


def exportCSV():
    file = str(fileName.get()) + ".csv"
    with open(file, 'w') as f:
        writer = csv.writer(f)
        c.execute('SELECT * FROM userdata')
        data = c.fetchall()
        writer.writerow(
            ['File Number', 'Department From', 'Department To', 'Transition Column', 'Date', 'Subject Matter',
             'Staff Number'])
        writer.writerows(data)
        messagebox.showinfo("Success", f"{file} exported successfully!")


def exportExcel():
    pass


# Structure and Layout
window = Tk()
window.title("NPC Register")
window.geometry("1080x600")

style = ttk.Style(window)
style.configure("lefttab.TNotebook", tabposition="wn")

# Tab layout
tabControl = ttk.Notebook(window, style="lefttab.TNotebook")
home = ttk.Frame(tabControl)
view = ttk.Frame(tabControl)
search = ttk.Frame(tabControl)
export = ttk.Frame(tabControl)
about = ttk.Frame(tabControl)

# Add Tabs to Notebook
tabControl.add(home, text=f'{"Home":^20s}')
tabControl.add(view, text=f'{"View":^20s}')
tabControl.add(search, text=f'{"Search":^20s}')
tabControl.add(export, text=f'{"Export":^20s}')
tabControl.add(about, text=f'{"About":^20s}')

tabControl.pack(expand=1, fill="both")

creatTable()

label1 = Label(home, text="Home", padx=5, pady=5)
label1.grid(row=0, column=0)

label2 = Label(view, text="View", padx=5, pady=5)
label2.grid(row=0, column=0)

label3 = Label(search, text="Search", padx=5, pady=5)
label3.grid(row=0, column=0)

label4 = Label(export, text="Export", padx=5, pady=5)
label4.grid(row=0, column=0)

label5 = Label(about, text="About", padx=5, pady=5)
label5.grid(row=0, column=0)

# Home page
fn = Label(home, text="File Number", padx=5, pady=5)
fn.grid(row=1, column=0)
fileNum = StringVar()
fileNumber = Entry(home, textvariable=fileNum, width=50)
fileNumber.grid(row=1, column=1)

df = Label(home, text="Department From", padx=5, pady=5)
df.grid(row=2, column=0)
deptFrom = StringVar()
departmentFrom = Entry(home, textvariable=deptFrom, width=50)
departmentFrom.grid(row=2, column=1)

yd = Label(home, text="Department To", padx=5, pady=5)
yd.grid(row=3, column=0)
deptTo = StringVar()
departmentTo = Entry(home, textvariable=deptTo, width=50)
departmentTo.grid(row=3, column=1)

tc = Label(home, text="Transition Column", padx=5, pady=5)
tc.grid(row=4, column=0)
transColumn = StringVar()
transitionColumn = Entry(home, textvariable=transColumn, width=50)
transitionColumn.grid(row=4, column=1)

dt = Label(home, text="Date", padx=5, pady=5)
dt.grid(row=5, column=0)
day = StringVar()
date = DateEntry(home, textvariable=day, background="green", foreground="white", borderwidth=2, year=2023)
date.grid(row=5, column=1, padx=10, pady=10)

sb = Label(home, text="Subject Matter", padx=5, pady=5)
sb.grid(row=6, column=0)
subject = StringVar()
subjectMatter = Text(home, wrap="word", width=37, height=5)
subjectMatter.grid(row=6, column=1)

sn = Label(home, text="Staff Number", padx=5, pady=5)
sn.grid(row=7, column=0)
staffNum = StringVar()
staffNumber = Entry(home, textvariable=staffNum, width=50)
staffNumber.grid(row=7, column=1)

add = Button(home, text="Add Record", width=12, bg="green", fg="white", command=addData)
add.grid(row=8, column=0, padx=5, pady=5)

clear = Button(home, text="Clear Entries", width=12, bg="green", fg="white", command=clearText)
clear.grid(row=8, column=1, padx=5, pady=5)

# Display Screen
homeDisplay = ScrolledText(home, height=10)
homeDisplay.grid(row=9, column=0, padx=5, pady=5, columnspan=3)

clearDisplay = Button(home, text="Clear Submission", width=12, bg="green", fg="white", command=clearDisp)
clearDisplay.grid(row=10, column=1, padx=10, pady=10)

# View page
viewAll = Button(view, text="View All", width=12, bg="green", fg="white", command=viewAllUsers)
viewAll.grid(row=1, column=0, padx=10, pady=10)
tree = ttk.Treeview(view, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"),
                    show="headings")
tree.heading("#1", text="File Number")
tree.heading("#2", text="Department From")
tree.heading("#3", text="Department To")
tree.heading("#4", text="Transition Column")
tree.heading("#5", text="Date")
tree.heading("#6", text="Subject Matter")
tree.heading("#7", text="Staff Number")
tree.grid(row=10, column=0, columnspan=3, padx=5, pady=5)

clearTree = Button(view, text="Clear Table", width=12, bg="green", fg="white", command=clearTable)
clearTree.grid(row=1, column=1, padx=10, pady=10)

# Search page
sc = Label(search, text="Search by Name", padx=5, pady=5)
sc.grid(row=1, column=0)
searchValue = StringVar()
seach = Entry(search, textvariable=searchValue, width=50)
seach.grid(row=1, column=1)

searchUser = Button(search, text="Search", width=12, bg="green", fg="white", command=searchUser)
searchUser.grid(row=1, column=2, padx=10, pady=10)

clearSearch = Button(search, text="Clear Search", width=12, bg="green", fg="white", command=clearSearch)
clearSearch.grid(row=2, column=1, padx=10, pady=10)

clearResult = Button(search, text="Clear Results", width=12, bg="green", fg="white", command=clearResult)
clearResult.grid(row=2, column=2, padx=10, pady=10)

# Display Screen
searchDisplay = ScrolledText(search, height=10)
# searchDisplay = Listbox(search, width=60, height=5)
searchDisplay.grid(row=10, column=0, padx=5, pady=5, columnspan=3)

# Export page
ex = Label(export, text="File Name", padx=5, pady=5)
ex.grid(row=2, column=0)
filename = StringVar()
fileName = Entry(export, textvariable=filename, width=30)
fileName.grid(row=2, column=1)

toCSV = Button(export, text="Export CSV", width=12, bg="green", fg="white", command=exportCSV)
toCSV.grid(row=3, column=0, padx=10, pady=10)

toExcel = Button(export, text="Export Excel", width=12, bg="green", fg="white", command=exportExcel)
toExcel.grid(row=3, column=1, padx=10, pady=10)

# About page
about = Label(about, text="NPC Register v1.0.0\nMorpheus Softwares", padx=5, pady=5)
about.grid(row=1, column=0)

window.mainloop()
