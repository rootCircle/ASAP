# -*- coding: utf-8 -*-
"""
Created on Sun May 17 10:12:06 2020

@author: rootCircle
"""

# =============================================================================
# Author@rootCircle
# Name of the Software: ASAP:Your school assistant
# Version=1.0.0.1
# Features: Login,Signup, Add/Modify/Delete Student's Profile, Make/Show/Update
#           Result, Search Student,Images,Modify profile for admin
# =============================================================================

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter import (
    messagebox,
    Radiobutton,
    Toplevel,
    PhotoImage,
    StringVar,
    OptionMenu,
    ttk,
)
import sqlite3
from time import ctime, time
from PIL import Image, ImageTk


class ASAPtools:
    def sqlite3_run(self, *sqlite_query):
        """
        The function will take multiple queries and output the result in
        form of list such that output of Query1 lies at index 0 ,Query2
        at index 1 and so on.
        """
        output = []
        try:
            sqliteConnection = sqlite3.connect("asap.db")
            cursor = sqliteConnection.cursor()
            for query in sqlite_query:
                cursor.execute(query)
                sqliteConnection.commit()
                output.append(cursor.fetchall())
            cursor.close()
            return output
        except sqlite3.Error as error:
            print(error)
            messagebox.showwarning("Error", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def image_Show(self, Dir, irow, icolumn, width, height):
        Photo = Image.open(Dir)
        Photo = Photo.resize((width, height))
        render = ImageTk.PhotoImage(Photo)
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=irow, column=icolumn, pady=3)

    def generateId(self, table):
        Query = "Select id from " + table
        out = ASAPtools.sqlite3_run(self, Query)
        data = out[0]
        k = 1
        ListId = []
        for i in range(len(data)):
            ListId.append(data[i][0])
        while k in ListId:
            k += 1
        return k

    def ValidateId(self, Sid, table):
        Query = "Select id from " + table
        out = ASAPtools.sqlite3_run(self, Query)

        data = out[0]
        ListId = []

        for i in range(len(data)):
            ListId.append(data[i][0])
        return bool(int(Sid) in ListId)

    def removeSpace(self, text):
        newText = ""
        for i in text:
            if i != " ":
                newText += i
        return newText

    def checkDigit(self, *text):
        for msg in text:
            c = c2 = 0
            for i in msg:
                if i == ".":
                    c += 1
                elif i == "-":
                    c2 += 1
                elif not (i.isdigit()):
                    return False
            if c > 1 or c2 > 1:
                return False
        return True

    def isnotNull(self, *text):
        for msg in text:
            if msg == "":
                return False
        return True

    def inLimit(self, lower, upper, *text):
        for msg in text:
            n = float(msg)
            if n > upper or n < lower:
                return False
        return True

    def logout(self, master):
        gname.set("")
        gpin.set("")
        gusername.set("")
        master.switch_frame(Homepage)


class Asap(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Homepage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class Homepage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Label(
            self,
            text="Welcome to ASAP:Your School Assistant",
            font=("Chiller", 30),
            fg="#E8E8E8",
            bg="#333333",
        ).grid(row=0, column=0)
        tk.Label(
            self, text="Homepage", font=("Chiller", 20), fg="#E8E8E8", bg="#333333"
        ).grid(row=1, column=0)
        ASAPtools.image_Show(self, "Lighthouse.jpg", 2, 0, 300, 200)
        tk.Button(
            self,
            text="Login",
            command=lambda: master.switch_frame(PageOne_Login),
            bg="#1F8EE7",
            padx=3,
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=3, column=0, pady=2)
        tk.Button(
            self,
            text="Admin Signup",
            command=lambda: master.switch_frame(PageTwo_SignupAdmin),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=4, column=0, pady=2)


class PageOne_Login(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)
        global gname
        gname = StringVar()
        global gpin
        gpin = StringVar()
        global gusername
        gusername = StringVar()

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(Homepage),
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)

        tk.Label(
            self, text="Login", font=("Chiller", 30), fg="#E8E8E8", bg="#333333"
        ).grid(row=1, column=2)

        tk.Label(self, text="Username", fg="#E8E8E8", bg="#333333").grid(
            row=2, column=1
        )

        username = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        username.grid(row=2, column=2)

        tk.Label(self, text="Password", fg="#E8E8E8", bg="#333333").grid(
            row=3, column=1
        )

        password = tk.Entry(self, show="*", fg="#E8E8E8", bg="#333333")
        password.grid(row=3, column=2)

        tk.Button(
            self,
            text="Login",
            command=lambda: self.login_Check(master, username.get(), password.get()),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=4, column=4, padx=5, pady=5)

    def login_Check(self, master, cuser, cpass):
        def_Query = """CREATE TABLE IF NOT EXISTS ADTEA(id INTEGER PRIMARY KEY,Name TEXT NOT NULL,Age INT NOT NULL,Gender CHAR(1),Username TEXT NOT NULL  UNIQUE, Password TEXT Not Null,PIN INTEGER NOT NULL);"""
        ASAPtools.sqlite3_run(self, def_Query)
        sqlite_query = "Select id,Username,Password,Pin from ADTEA"
        record = ASAPtools.sqlite3_run(self, sqlite_query)[0]
        for aid, usern, pas, pin in record:
            if cuser == usern and cpass == pas:
                Query = "Select Name,Username,PIN from ADTEA Where id =" + str(aid)
                data = ASAPtools.sqlite3_run(self, Query)
                nameG = data[0][0][0]
                gpin.set(pin)
                gusername.set(data[0][0][1])
                gname.set("Welcome " + nameG)
                master.switch_frame(PageThree_Dashboard)
                return
        messagebox.showerror("Invalid credentials", "Invalid username or password!")


class PageTwo_SignupAdmin(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(Homepage),
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)

        tk.Label(
            self, text="Register", font=("Chiller", 30), fg="#E8E8E8", bg="#333333"
        ).grid(row=1, column=2)
        tk.Label(self, text="Name", fg="#E8E8E8", bg="#333333").grid(
            row=2, column=1, padx=25
        )

        name = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        name.grid(row=2, column=2)

        tk.Label(self, text="Age", fg="#E8E8E8", bg="#333333").grid(row=3, column=1)

        age = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        age.grid(row=3, column=2)

        tk.Label(self, text="Gender", fg="#E8E8E8", bg="#333333").grid(row=4, column=1)

        gender = StringVar(self, "M")
        gen = {"Male": "M", "Female": "F", "Not specified": "N"}
        i = 2
        for text, value in gen.items():
            Radiobutton(
                self,
                text=text,
                variable=gender,
                value=value,
                activebackground="#333333",
                bg="#333333",
                fg="#E8E8E8",
                selectcolor="#333333",
            ).grid(sticky="W", row=4, column=i)
            i += 1
        tk.Label(self, text="Pin", fg="#E8E8E8", bg="#333333").grid(row=5, column=1)

        Pin = tk.Entry(self, show="*", fg="#E8E8E8", bg="#333333")
        Pin.grid(row=5, column=2)

        username = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        username.grid(row=6, column=2)

        tk.Label(self, text="Username", fg="#E8E8E8", bg="#333333").grid(
            row=6, column=1
        )

        Password = tk.Entry(self, show="*", fg="#E8E8E8", bg="#333333")
        Password.grid(row=7, column=2)

        tk.Label(self, text="Password", fg="#E8E8E8", bg="#333333").grid(
            row=7, column=1
        )

        Repassword = tk.Entry(self, show="*", fg="#E8E8E8", bg="#333333")
        Repassword.grid(row=8, column=2)

        tk.Label(self, text="Confirm Password", fg="#E8E8E8", bg="#333333").grid(
            row=8, column=1
        )

        tk.Button(
            self,
            text="Register",
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
            command=lambda: self.RegisterAdmin(
                master,
                name.get(),
                age.get(),
                gender.get(),
                username.get(),
                Password.get(),
                Repassword.get(),
                Pin.get(),
            ),
        ).grid(row=9, column=3, pady=3)

    def RegisterAdmin(
        self, master, name, age, gender, Username, Password, Repassword, PIN
    ):
        if Password == Repassword:
            def_Query = "CREATE TABLE IF NOT EXISTS ADTEA(id INTEGER PRIMARY KEY,Name TEXT NOT NULL,Age INT NOT NULL,Gender CHAR(1),Username TEXT NOT NULL  UNIQUE, Password TEXT Not Null,PIN INTEGER NOT NULL);"
            Query_2 = "select id from adtea where username='" + Username + "';"
            out = ASAPtools.sqlite3_run(self, def_Query, Query_2)

            if (
                ASAPtools.isnotNull(
                    self, name, age, gender, Username, Password, Repassword, PIN
                )
                and ASAPtools.checkDigit(self, age, PIN)
                and ASAPtools.inLimit(self, 0, 150, age)
            ):
                if out[1] == []:
                    VALUE = (
                        "("
                        + str(ASAPtools.generateId(self, "adtea"))
                        + ",'"
                        + name
                        + "',"
                        + age
                        + ",'"
                        + gender
                        + "','"
                        + Username
                        + "','"
                        + Password
                        + "',"
                        + PIN
                        + ");"
                    )
                    sqlite_query = (
                        "Insert into ADTEA(id,Name,Age,Gender,Username,Password,PIN) values"
                        + VALUE
                    )
                    ASAPtools.sqlite3_run(self, sqlite_query)
                    messagebox.showinfo(
                        "Registration done", "Registered user successfully"
                    )
                    master.switch_frame(Homepage)
                else:
                    messagebox.showinfo(
                        "Sorry! Usename already taken", "Try a different username"
                    )
            else:
                messagebox.showinfo(
                    "Invalid entry", "Fill all the entry correctly to proceed"
                )
        else:
            messagebox.showwarning("Password Mismatch", "Re-enter Password")


class PageThree_Dashboard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Label(
            self,
            text="Welcome to ASAP:Your school Assistant",
            font=("Chiller", 30),
            fg="#E8E8E8",
            bg="#333333",
        ).grid(row=0, column=0)
        tk.Label(
            self, text="Dashboard", font=("Chiller", 25), fg="#E8E8E8", bg="#333333"
        ).grid(row=1, column=0)

        tk.Label(
            self,
            textvariable=gname,
            font=("Segoe Print", 15),
            fg="#E8E8E8",
            bg="#333333",
        ).grid(row=2, column=0, pady=20)

        ASAPtools.image_Show(self, "Jellyfish.jpg", 3, 0, 200, 150)

        tk.Button(
            self,
            text="Student's tool",
            command=lambda: master.switch_frame(PageThreePart1_Dashboard),
            padx=9,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=4, column=0, pady=1, padx=3)

        tk.Button(
            self,
            text="Teacher/Admin's tool",
            command=lambda: master.switch_frame(PageThreePart2_Dashboard),
            padx=8,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=5, column=0, pady=3)

        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=25,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=6, column=0, pady=3)


class PageThreePart1_Dashboard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(PageThree_Dashboard),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=3)
        tk.Label(
            self,
            text="Student's tool",
            font=("Chiller", 25),
            fg="#E8E8E8",
            bg="#333333",
        ).grid(row=1, column=1)

        ASAPtools.image_Show(self, "Jellyfish.jpg", 2, 1, 200, 150)

        tk.Button(
            self,
            text="Register student",
            command=lambda: master.switch_frame(PageFour_SignupStudent),
            padx=9,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=3, column=1, pady=1, padx=3)

        tk.Button(
            self,
            text="Search student",
            command=lambda: master.switch_frame(Page5_SearchStudents),
            padx=8,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=4, column=1, pady=1)

        tk.Button(
            self,
            text="Modify/Delete Profile of student",
            command=lambda: master.switch_frame(Page9_ModifyProfileStudent),
            padx=5,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=5, column=1, pady=1)

        tk.Button(
            self,
            text="Show Result",
            command=lambda: master.switch_frame(Page10_ShowResult),
            padx=5,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=6, column=1, pady=1)

        tk.Button(
            self,
            text="Add Result",
            command=lambda: master.switch_frame(Page11_MakeResult),
            padx=5,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=7, column=1, pady=1)

        tk.Button(
            self,
            text="Modify Result",
            command=lambda: master.switch_frame(Page12_UpdateResult),
            padx=5,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=8, column=1, pady=1)


class PageThreePart2_Dashboard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(PageThree_Dashboard),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=3)
        tk.Label(
            self,
            text="Teacher's tool",
            font=("Chiller", 25),
            fg="#E8E8E8",
            bg="#333333",
        ).grid(row=1, column=1)

        ASAPtools.image_Show(self, "Jellyfish.jpg", 2, 1, 200, 150)

        tk.Button(
            self,
            text="Profile",
            command=lambda: master.switch_frame(Page6_ProfileAdmin),
            padx=30,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=3, column=1, pady=2)

        tk.Button(
            self,
            text="Modify Profile",
            command=lambda: master.switch_frame(Page7_ModifyProfileAdmin),
            padx=9,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=4, column=1, pady=2)

        tk.Button(
            self,
            text="Image",
            command=lambda: master.switch_frame(Page8_Image),
            padx=30,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=5, column=1, pady=2)

        tk.Button(
            self,
            text="Delete Account",
            command=lambda: self.del_AccountAdmin(master),
            padx=5,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=6, column=1, pady=2)

    def del_AccountAdmin(self, master):
        choice = messagebox.askyesno(
            "Alert", "Are you sure want to delete your account?"
        )
        if choice:
            ASAPtools.sqlite3_run(
                self, "Delete from adtea where username='" + gusername.get() + "';"
            )
            messagebox.showinfo("Success", "Account Deleted Successfully")
            master.switch_frame(Homepage)


class PageFour_SignupStudent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(PageThreePart1_Dashboard),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=8)

        tk.Label(
            self, text="Register", font=("Chiller", 30), fg="#E8E8E8", bg="#333333"
        ).grid(row=1, column=2)

        tk.Label(self, text="Name", fg="#E8E8E8", bg="#333333").grid(
            row=2, column=1, padx=25
        )

        name = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        name.grid(row=2, column=2)

        tk.Label(self, text="Age", fg="#E8E8E8", bg="#333333").grid(row=3, column=1)

        Age = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        Age.grid(row=3, column=2)

        tk.Label(self, text="Class", fg="#E8E8E8", bg="#333333").grid(row=4, column=1)

        Class = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        Class.grid(row=4, column=2)

        tk.Label(self, text="Father's Name", fg="#E8E8E8", bg="#333333").grid(
            row=5, column=1
        )

        Fname = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        Fname.grid(row=5, column=2)

        tk.Label(self, text="Mother's Name", fg="#E8E8E8", bg="#333333").grid(
            row=6, column=1
        )

        Mname = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        Mname.grid(row=6, column=2)

        tk.Label(self, text="Social status", fg="#E8E8E8", bg="#333333").grid(
            row=7, column=1
        )

        socstatus = StringVar(self, "GEN")
        SOC = {"General": "GEN", "OBC": "OBC", "SC": "SC", "ST": "ST"}
        i = 2
        for text, value in SOC.items():
            Radiobutton(
                self,
                text=text,
                variable=socstatus,
                value=value,
                activebackground="#333333",
                bg="#333333",
                fg="#E8E8E8",
                selectcolor="#333333",
            ).grid(sticky="W", row=7, column=i)
            i += 1
        tk.Label(self, text="Gender", fg="#E8E8E8", bg="#333333").grid(row=8, column=1)

        gender = StringVar(self, "M")
        GEN = {"Male": "M", "Female": "F", "Not specified": "N"}
        i = 2
        for text, value in GEN.items():
            Radiobutton(
                self,
                text=text,
                variable=gender,
                value=value,
                activebackground="#333333",
                bg="#333333",
                fg="#E8E8E8",
                selectcolor="#333333",
            ).grid(sticky="W", row=8, column=i)
            i += 1
        tk.Label(self, text="Religion", fg="#E8E8E8", bg="#333333").grid(
            row=9, column=1
        )

        Religion = StringVar(self, "Hindu")
        REL = {
            "Hindu": "Hindu",
            "Muslim": "Muslim",
            "Christian": "Christian",
            "Sikh": "Sikh",
        }
        i = 2
        for text, value in REL.items():
            Radiobutton(
                self,
                text=text,
                variable=Religion,
                value=value,
                activebackground="#333333",
                bg="#333333",
                fg="#E8E8E8",
                selectcolor="#333333",
            ).grid(sticky="W", row=9, column=i)
            i += 1
        Radiobutton(
            self,
            text="Other",
            variable=Religion,
            value="NAN",
            command=self.other_Religion,
            activebackground="#333333",
            bg="#333333",
            fg="#E8E8E8",
            selectcolor="#333333",
        ).grid(sticky="W", row=9, column=6)

        tk.Label(self, text="Pin", fg="#E8E8E8", bg="#333333").grid(row=10, column=1)

        Pin = tk.Entry(self, show="*", fg="#E8E8E8", bg="#333333")
        Pin.grid(row=10, column=2)

        tk.Button(
            self,
            text="Register",
            command=lambda: self.RegisterStudent(
                master,
                name.get(),
                Age.get(),
                Fname.get(),
                Mname.get(),
                Class.get(),
                socstatus.get(),
                gender.get(),
                Religion.get(),
                Pin.get(),
            ),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=11, column=3, pady=3)

    def RegisterStudent(
        self, master, name, age, fname, mname, Class, soc, gender, Religion, PINraw
    ):
        def_Query = "CREATE TABLE IF NOT EXISTS STUDENTS (id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Age INT NOT NULL, Gender CHAR(1) NOT NULL, Class INT NOT NULL, Father_name TEXT, Mother_name TEXT, Social_Status varchar(3), Religion TEXT);"

        ASAPtools.sqlite3_run(self, def_Query)

        Religionval = ""
        if Religion != "NAN":
            Religionval = Religion
        else:
            Religionval = otherReligionInput.get()
        if gpin.get() == PINraw:
            if (
                ASAPtools.isnotNull(
                    self, name, age, fname, mname, Class, soc, gender, Religionval
                )
                and ASAPtools.checkDigit(self, age, Class)
                and ASAPtools.inLimit(self, 0, 150, age)
                and ASAPtools.inLimit(self, -2, 12, Class)
            ):
                VALUE = (
                    "("
                    + str(ASAPtools.generateId(self, "students"))
                    + ",'"
                    + name
                    + "',"
                    + age
                    + ",'"
                    + gender
                    + "',"
                    + Class
                    + ",'"
                    + fname
                    + "','"
                    + mname
                    + "','"
                    + soc
                    + "','"
                    + Religionval
                    + "');"
                )
                sqlite_query = (
                    "Insert into students(id,Name,Age,Gender,Class,Father_name,Mother_name,Social_Status,Religion) values"
                    + VALUE
                )
                ASAPtools.sqlite3_run(self, sqlite_query)
                messagebox.showinfo(
                    "Registration done", "Registered student successfully"
                )
                master.switch_frame(PageThreePart1_Dashboard)
            else:
                messagebox.showinfo(
                    "Invalid entry", "Fill all the entry correctly to proceed"
                )
        else:
            messagebox.showerror("Invalid PIN", "Re-enter correct PIN")

    def other_Religion(self):
        global otherReligionInput
        otherReligionInput = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        otherReligionInput.grid(row=9, column=7)


class Page5_SearchStudents(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(PageThreePart1_Dashboard),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=9)
        tk.Label(
            self,
            text="Search Student",
            font=("Chiller", 30),
            fg="#E8E8E8",
            bg="#333333",
        ).grid(row=1, column=5)

        tk.Label(self, text="Search by", fg="#E8E8E8", bg="#333333").grid(
            row=2, column=1, padx=25
        )

        criteria = StringVar(self, "Name")
        options = {
            "Name": "Name",
            "Class": "Class",
            "Age": "Age",
            "Father's name": "Father_name",
            "Mother's name": "Mother_name",
            "Social status(GEN/OBC/SC/ST)": "Social_status",
            "Gender(M/F/N)": "Gender",
            "Religion": "Religion",
        }
        i = 1
        for text, value in options.items():
            Radiobutton(
                self,
                text=text,
                variable=criteria,
                value=value,
                activebackground="#333333",
                bg="#333333",
                fg="#E8E8E8",
                selectcolor="#333333",
            ).grid(row=3, column=i)
            i += 1
        tk.Label(self, text="Enter detail", fg="#E8E8E8", bg="#333333").grid(
            row=5, column=4, pady=5
        )
        text = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        text.grid(row=5, column=5, pady=5)
        tk.Button(
            self,
            text="Search",
            command=lambda: self.search(text.get(), criteria.get()),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=7, column=5, pady=3, padx=5)
        tk.Button(
            self,
            text="Show All",
            command=self.showAll,
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=7, column=6, pady=3)

    def search(self, text, criteria):
        def_Query = "CREATE TABLE IF NOT EXISTS STUDENTS (id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Age INT NOT NULL, Gender CHAR(1) NOT NULL, Class INT NOT NULL, Father_name TEXT, Mother_name TEXT, Social_Status varchar(3), Religion TEXT);"

        ASAPtools.sqlite3_run(self, def_Query)
        if ASAPtools.isnotNull(self, text):
            if criteria not in ("Age", "Class"):
                sqlite_query = (
                    "Select * from students where "
                    + criteria
                    + " like '%"
                    + text
                    + "%'"
                )
                record = ASAPtools.sqlite3_run(self, sqlite_query)
            else:
                if ASAPtools.checkDigit(self, text):
                    sqlite_query = (
                        "Select * from students where " + criteria + "=" + str(text)
                    )
                    record = ASAPtools.sqlite3_run(self, sqlite_query)
                else:
                    messagebox.showwarning("Error", "Incorrect input!")
                    record = None
            if record is not None:
                out = record[0]
                if out != []:
                    self.output(out)
                else:
                    messagebox.showinfo("No data", "No records found")
        else:
            messagebox.showwarning("Error", "Incomplete input!")

    def showAll(self):
        def_Query = "CREATE TABLE IF NOT EXISTS STUDENTS (id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Age INT NOT NULL, Gender CHAR(1) NOT NULL, Class INT NOT NULL, Father_name TEXT, Mother_name TEXT, Social_Status varchar(3), Religion TEXT);"

        ASAPtools.sqlite3_run(self, def_Query)
        sqlite_query = "Select * from students;"
        record = ASAPtools.sqlite3_run(self, sqlite_query)
        if record is not None:
            out = record[0]
            if out != []:
                self.output(out)
        if out == []:
            messagebox.showinfo("No data", "No records found")

    def output(self, out):
        screen = Toplevel(self, bg="#333333", width=200)
        screen.iconphoto(False, Icon)
        tk.Label(
            screen,
            text="Search Result",
            font=("Chiller", 30),
            fg="#E8E8E8",
            bg="#333333",
        ).grid(row=0, columnspan=3)

        # L=["Id","Name","Age","Gender","Class","Father's name","Mother's name"
        # ,"Social status","Religion"]
        # for i in range(0,9):
        #     tk.Label(screen,text=L[i],font=("Cailbri",12),fg='#E8E8E8',bg='#333333').grid(row=1,column=i+1)
        # counter=1
        # print(out)
        # for data in out:
        #     counter+=1
        #     for i in range(0,9):
        #         tk.Label(screen,text=data[i],fg='#E8E8E8',bg='#333333').grid(row=counter,column=i+1,padx=10)

        column = (
            "Id",
            "Name",
            "Age",
            "Gender",
            "Class",
            "Father's name",
            "Mother's name",
            "Social status",
            "Religion",
        )
        listBox = ttk.Treeview(
            screen, selectmode="extended", columns=column, show="headings"
        )

        for i in range(0, len(column)):
            listBox.heading(column[i], text=column[i])
            listBox.column(column[i], minwidth=0, width=70)
        for col in column:
            listBox.heading(col, text=col)
        listBox.grid(row=2, column=0)

        for i in out:
            listBox.insert("", "end", values=i)


class Page6_ProfileAdmin(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(PageThreePart2_Dashboard),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=4)
        tk.Label(
            self, text="Profile", font=("Chiller", 30), fg="#E8E8E8", bg="#333333"
        ).grid(row=1, column=2)

        sqlite_query = (
            "Select id,name,age,gender,username from adtea where username='"
            + gusername.get()
            + "';"
        )
        out = ASAPtools.sqlite3_run(self, sqlite_query)
        data = out[0][0]
        data = list(data)
        if data[3] == "M":
            data[3] = "Male"
        elif data[3] == "F":
            data[3] = "Female"
        else:
            data[3] = "Not specified"
        L = ["Id", "Name", "Age", "Gender", "Username"]
        for i in range(0, 5):
            tk.Label(
                self, text=L[i] + ":", font=("Calibri", 12), fg="#E8E8E8", bg="#333333"
            ).grid(row=2 + i, column=1)
            tk.Label(self, text=data[i], fg="#E8E8E8", bg="#333333").grid(
                row=2 + i, column=3
            )


class Page7_ModifyProfileAdmin(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(PageThreePart2_Dashboard),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=5)
        sqlite_query = (
            "Select name,age,gender from adtea where username='" + gusername.get() + "'"
        )
        out = ASAPtools.sqlite3_run(self, sqlite_query)
        data = out[0][0]

        tk.Label(
            self,
            text="Modify Profile",
            font=("Chiller", 30),
            fg="#E8E8E8",
            bg="#333333",
        ).grid(row=1, column=2)

        tk.Label(self, text="Name", fg="#E8E8E8", bg="#333333").grid(
            row=2, column=1, padx=25
        )

        name = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        name.grid(row=2, column=2)
        name.insert(0, data[0])

        tk.Label(self, text="Age", fg="#E8E8E8", bg="#333333").grid(row=3, column=1)

        age = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        age.grid(row=3, column=2)
        age.insert(0, data[1])

        tk.Label(self, text="Gender", fg="#E8E8E8", bg="#333333").grid(row=4, column=1)

        gender = StringVar(self, data[2])
        gen = {"Male": "M", "Female": "F", "Not specified": "N"}
        i = 2
        for text, value in gen.items():
            Radiobutton(
                self,
                text=text,
                variable=gender,
                value=value,
                activebackground="#333333",
                bg="#333333",
                fg="#E8E8E8",
                selectcolor="#333333",
            ).grid(sticky="W", row=4, column=i, pady=3)
            i += 1
        tk.Button(
            self,
            text="Modify Profile",
            command=lambda: self.modifyAdmin(
                master, name.get(), age.get(), gender.get()
            ),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=5, column=3, pady=3)

    def modifyAdmin(self, master, name, age, gen):
        if (
            ASAPtools.isnotNull(self, name, age, gen)
            and ASAPtools.checkDigit(self, age)
            and ASAPtools.inLimit(self, 0, 150, age)
        ):
            Query = (
                "Update ADTEA set name='"
                + name
                + "'"
                + ",age="
                + age
                + ",Gender='"
                + gen
                + "' where username='"
                + gusername.get()
                + "';"
            )
            ASAPtools.sqlite3_run(self, Query)
            gname.set("Welcome " + name)
            messagebox.showinfo("Success!", "Profile updated successfully")
            master.switch_frame(PageThreePart2_Dashboard)
        else:
            messagebox.showwarning("Error", "Fill all form(s) correctly to continue")


class Page8_Image(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(PageThreePart2_Dashboard),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=7)
        tk.Label(
            self, text="Just for Fun", font=("Chiller", 30), fg="#E8E8E8", bg="#333333"
        ).grid(row=1, column=2)

        ASAPtools.image_Show(self, "Koala.jpg", 2, 1, 200, 200)
        ASAPtools.image_Show(self, "icon.png", 2, 2, 200, 200)
        ASAPtools.image_Show(self, "Hydrangeas.jpg", 2, 3, 200, 200)

        ASAPtools.image_Show(self, "Penguins.jpg", 3, 1, 200, 200)
        ASAPtools.image_Show(self, "logo.png", 3, 2, 200, 200)
        ASAPtools.image_Show(self, "Tulips.jpg", 3, 3, 200, 200)


class Page9_ModifyProfileStudent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(PageThreePart1_Dashboard),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=8)
        tk.Label(
            self,
            text="Modify Profile",
            font=("Chiller", 30),
            fg="#E8E8E8",
            bg="#333333",
        ).grid(row=1, column=2)

        tk.Label(self, text="Enter Id of Student", fg="#E8E8E8", bg="#333333").grid(
            row=2, column=1, padx=5, pady=5
        )

        Sid = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        Sid.grid(row=2, column=2)
        tk.Button(
            self,
            text="Proceed",
            command=lambda: self.ModifyUI(master, Sid.get()),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=3, column=2, pady=10, padx=3)

    def ModifyUI(self, master, Sid):
        def_Query = "CREATE TABLE IF NOT EXISTS STUDENTS (id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Age INT NOT NULL, Gender CHAR(1) NOT NULL, Class INT NOT NULL, Father_name TEXT, Mother_name TEXT, Social_Status varchar(3), Religion TEXT);"

        ASAPtools.sqlite3_run(self, def_Query)

        if ASAPtools.isnotNull(self, Sid):
            if ASAPtools.ValidateId(self, Sid, "students"):
                sqlite_query = (
                    "Select Name,Age,Gender,Class,Father_name,Mother_name,Social_Status,Religion from students where id="
                    + Sid
                )
                out = ASAPtools.sqlite3_run(self, sqlite_query)
                data = out[0][0]

                tk.Label(self, text="Name", fg="#E8E8E8", bg="#333333").grid(
                    row=4, column=1, padx=25
                )

                name = tk.Entry(self, fg="#E8E8E8", bg="#333333")
                name.grid(row=4, column=2)
                name.insert(0, data[0])

                tk.Label(self, text="Age", fg="#E8E8E8", bg="#333333").grid(
                    row=5, column=1
                )

                Age = tk.Entry(self, fg="#E8E8E8", bg="#333333")
                Age.grid(row=5, column=2)
                Age.insert(0, data[1])
                tk.Label(self, text="Class", fg="#E8E8E8", bg="#333333").grid(
                    row=6, column=1
                )

                Class = tk.Entry(self, fg="#E8E8E8", bg="#333333")
                Class.grid(row=6, column=2)
                Class.insert(0, data[3])

                tk.Label(self, text="Father's Name", fg="#E8E8E8", bg="#333333").grid(
                    row=7, column=1
                )

                Fname = tk.Entry(self, fg="#E8E8E8", bg="#333333")
                Fname.grid(row=7, column=2)
                Fname.insert(0, data[4])
                tk.Label(self, text="Mother's Name", fg="#E8E8E8", bg="#333333").grid(
                    row=8, column=1
                )

                Mname = tk.Entry(self, fg="#E8E8E8", bg="#333333")
                Mname.grid(row=8, column=2)
                Mname.insert(0, data[5])
                tk.Label(self, text="Social status", fg="#E8E8E8", bg="#333333").grid(
                    row=9, column=1
                )

                socstatus = StringVar(self, data[6])
                SOC = {"General": "GEN", "OBC": "OBC", "SC": "SC", "ST": "ST"}
                i = 2
                for text, value in SOC.items():
                    Radiobutton(
                        self,
                        text=text,
                        variable=socstatus,
                        value=value,
                        activebackground="#333333",
                        bg="#333333",
                        fg="#E8E8E8",
                        selectcolor="#333333",
                    ).grid(sticky="W", row=9, column=i)
                    i += 1
                tk.Label(self, text="Gender", fg="#E8E8E8", bg="#333333").grid(
                    row=10, column=1
                )

                gender = StringVar(self, data[2])
                GEN = {"Male": "M", "Female": "F", "Not specified": "N"}
                i = 2
                for text, value in GEN.items():
                    Radiobutton(
                        self,
                        text=text,
                        variable=gender,
                        value=value,
                        activebackground="#333333",
                        bg="#333333",
                        fg="#E8E8E8",
                        selectcolor="#333333",
                    ).grid(sticky="W", row=10, column=i)
                    i += 1
                tk.Label(self, text="Religion", fg="#E8E8E8", bg="#333333").grid(
                    row=11, column=1
                )

                REL = {
                    "Hindu": "Hindu",
                    "Muslim": "Muslim",
                    "Christian": "Christian",
                    "Sikh": "Sikh",
                }
                if data[7] in REL:
                    Religion = StringVar(self, data[7])
                else:
                    Religion = StringVar(self, "NAN")
                    self.other_Religion()
                    otherReligionInput.insert(0, data[7])
                i = 2
                for text, value in REL.items():
                    Radiobutton(
                        self,
                        text=text,
                        variable=Religion,
                        value=value,
                        activebackground="#333333",
                        bg="#333333",
                        fg="#E8E8E8",
                        selectcolor="#333333",
                    ).grid(sticky="W", row=11, column=i)
                    i += 1
                Radiobutton(
                    self,
                    text="Other",
                    variable=Religion,
                    value="NAN",
                    command=self.other_Religion,
                    activebackground="#333333",
                    bg="#333333",
                    fg="#E8E8E8",
                    selectcolor="#333333",
                ).grid(sticky="W", row=11, column=6)

                tk.Label(self, text="Pin", fg="#E8E8E8", bg="#333333").grid(
                    row=12, column=1
                )

                Pin = tk.Entry(self, show="*", fg="#E8E8E8", bg="#333333")
                Pin.grid(row=12, column=2)
                tk.Button(
                    self,
                    text="Update Profile",
                    command=lambda: self.RegisterStudent(
                        master,
                        Sid,
                        name.get(),
                        Age.get(),
                        Fname.get(),
                        Mname.get(),
                        Class.get(),
                        socstatus.get(),
                        gender.get(),
                        Religion.get(),
                        Pin.get(),
                    ),
                    padx=3,
                    bg="#1F8EE7",
                    fg="#E8E8E8",
                    bd=0,
                    activebackground="#3297E9",
                ).grid(row=13, column=3, pady=3, padx=10)
                tk.Button(
                    self,
                    text="Delete Profile",
                    command=lambda: self.del_AccountStudent(master, Sid, Pin.get()),
                    padx=3,
                    bg="#1F8EE7",
                    fg="#E8E8E8",
                    bd=0,
                    activebackground="#3297E9",
                ).grid(row=13, column=4, pady=3)
            else:
                messagebox.showwarning("Error", "ID Not found")
        else:
            messagebox.showinfo("Error", "Fill the forms to continue")

    def del_AccountStudent(self, master, Sid, PINraw):
        if gpin.get() == PINraw:
            if ASAPtools.isnotNull(self, Sid):
                if ASAPtools.ValidateId(self, Sid, "students"):
                    choice = messagebox.askyesno(
                        "Alert", "Are you sure want to delete the profile?"
                    )
                    if choice:
                        ASAPtools.sqlite3_run(
                            self, "Delete from students where id='" + Sid + "';"
                        )
                        messagebox.showinfo("Success", "Deleted Profile Successfully")
                        master.switch_frame(PageThreePart1_Dashboard)
                else:
                    messagebox.showwarning("Error", "ID Not found")
            else:
                messagebox.showinfo("Error", "Fill the forms to continue")
        else:
            messagebox.showerror("Invalid PIN", "Re-enter correct PIN")

    def RegisterStudent(
        self, master, Sid, name, age, fname, mname, Class, soc, gender, Religion, PINraw
    ):
        def_Query = "CREATE TABLE IF NOT EXISTS STUDENTS (id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Age INT NOT NULL, Gender CHAR(1) NOT NULL, Class INT NOT NULL, Father_name TEXT, Mother_name TEXT, Social_Status varchar(3), Religion TEXT);"

        ASAPtools.sqlite3_run(self, def_Query)

        Religionval = ""
        if Religion != "NAN":
            Religionval = Religion
        else:
            Religionval = otherReligionInput.get()
        if gpin.get() == PINraw:
            if (
                ASAPtools.isnotNull(
                    self, name, age, gender, Religionval, fname, mname, Class, soc
                )
                and ASAPtools.checkDigit(self, age, Class)
                and ASAPtools.inLimit(self, 0, 150, age)
                and ASAPtools.inLimit(self, -2, 12, Class)
            ):
                sqlite_query = (
                    "Update students set Name='"
                    + name
                    + "',Age="
                    + age
                    + ",Gender='"
                    + gender
                    + "',Class="
                    + Class
                    + ",Father_name='"
                    + fname
                    + "',Mother_name='"
                    + mname
                    + "',Social_Status='"
                    + soc
                    + "',Religion='"
                    + Religionval
                    + "' where id="
                    + Sid
                    + ";"
                )
                ASAPtools.sqlite3_run(self, sqlite_query)
                messagebox.showinfo("Success", "Profile updated successfully")
                master.switch_frame(PageThreePart1_Dashboard)
            else:
                messagebox.showinfo(
                    "Invalid entry", "Fill all the entry correctly to proceed"
                )
        else:
            messagebox.showerror("Invalid PIN", "Re-enter correct PIN")

    def other_Religion(self):
        global otherReligionInput
        otherReligionInput = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        otherReligionInput.grid(row=11, column=7)


class Page10_ShowResult(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(PageThreePart1_Dashboard),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=8)
        tk.Label(
            self, text="Show Result", font=("Chiller", 30), fg="#E8E8E8", bg="#333333"
        ).grid(row=1, column=2)

        tk.Label(self, text="Enter Id of Student", fg="#E8E8E8", bg="#333333").grid(
            row=2, column=1, padx=5, pady=5
        )

        Sid = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        Sid.grid(row=2, column=2)

        tk.Label(self, text="Exam Type", fg="#E8E8E8", bg="#333333").grid(
            row=3, column=1, padx=5, pady=5
        )

        ExamType = [
            "First Unit test",
            "Second Unit test",
            "Half Yearly Exam",
            "Annual Exam",
        ]
        ExamTypeVar = StringVar(self, "First Unit test")
        Menu = OptionMenu(self, ExamTypeVar, *ExamType)
        Menu.config(bg="#333333", bd=0, fg="#E8E8E8", activebackground="#333333")
        Menu["menu"].config(bg="#333333", fg="#E8E8E8", activebackground="#1F8EE7")
        Menu.grid(row=3, column=2)

        tk.Label(self, text="Exam Year", fg="#E8E8E8", bg="#333333").grid(
            row=4, column=1, padx=5, pady=5
        )
        Time = ctime(time())  # Returns current time
        year = int(Time[-4:])
        ExamYear = []
        for i in range(10):
            ExamYear.append(year - i)
        ExamYearVar = StringVar(self, year)

        Menu1 = OptionMenu(self, ExamYearVar, *ExamYear)
        Menu1.config(bg="#333333", bd=0, fg="#E8E8E8", activebackground="#333333")
        Menu1["menu"].config(bg="#333333", fg="#E8E8E8", activebackground="#1F8EE7")
        Menu1.grid(row=4, column=2)

        tk.Button(
            self,
            text="Proceed",
            command=lambda: self.showResult(
                Sid.get(), ExamTypeVar.get() + ExamYearVar.get()
            ),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=5, column=3, pady=10, padx=3)

    def showResult(self, Sid, ExamID):
        def_Query = "CREATE TABLE IF NOT EXISTS STUDENTS (id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Age INT NOT NULL, Gender CHAR(1) NOT NULL, Class INT NOT NULL, Father_name TEXT, Mother_name TEXT, Social_Status varchar(3), Religion TEXT);"

        ASAPtools.sqlite3_run(self, def_Query)
        ExamID = "RESULT" + ASAPtools.removeSpace(self, ExamID)

        if ASAPtools.isnotNull(self, Sid) and ASAPtools.checkDigit(self, Sid):
            if ASAPtools.ValidateId(self, Sid, "students"):
                Query1 = (
                    "CREATE TABLE IF NOT EXISTS "
                    + ExamID
                    + " (id INTEGER PRIMARY KEY,marks_maths float,marks_computer float,marks_english float,marks_physics float,marks_chemistry float);"
                )
                ASAPtools.sqlite3_run(self, Query1)

                Query2 = (
                    "Select marks_maths,marks_computer,marks_english,marks_physics,marks_chemistry from "
                    + ExamID
                    + " where id="
                    + Sid
                )
                out2 = ASAPtools.sqlite3_run(self, Query2)[0]
                if out2 != []:
                    out2 = list(out2[0])
                    sqlite_query = "Select Name,Class from students where id=" + Sid
                    out = ASAPtools.sqlite3_run(self, sqlite_query)
                    data = out[0][0]

                    screen = Toplevel(self, bg="#333333")
                    screen.iconphoto(False, Icon)
                    tk.Label(
                        screen,
                        text="Report Card",
                        font=("Chiller", 30),
                        fg="#E8E8E8",
                        bg="#333333",
                    ).grid(row=0, column=2)
                    tk.Label(
                        screen, text="Name : " + data[0], fg="#E8E8E8", bg="#333333"
                    ).grid(row=1, column=1)
                    tk.Label(
                        screen, text="Id : " + Sid, fg="#E8E8E8", bg="#333333"
                    ).grid(row=1, column=2)
                    tk.Label(
                        screen,
                        text="Class : " + str(data[1]),
                        fg="#E8E8E8",
                        bg="#333333",
                    ).grid(row=1, column=3, pady=20)

                    tk.Label(
                        screen,
                        text="Subject",
                        font=("Calibri", 15),
                        fg="#E8E8E8",
                        bg="#333333",
                    ).grid(row=2, column=1)
                    L = [
                        "Maths",
                        "Computer",
                        "English",
                        "Physics",
                        "Chemistry",
                        "Total",
                        "Percentage",
                    ]
                    for i in range(0, 7):
                        tk.Label(screen, text=L[i], fg="#E8E8E8", bg="#333333").grid(
                            row=3 + i, column=1
                        )
                    tk.Label(
                        screen,
                        text="Marks",
                        font=("Calibri", 15),
                        fg="#E8E8E8",
                        bg="#333333",
                    ).grid(row=2, column=2)

                    total = sum(out2)
                    out2.append(total)
                    out2.append(str(total / 5) + "%")
                    for i in range(0, 7):
                        tk.Label(screen, text=out2[i], fg="#E8E8E8", bg="#333333").grid(
                            row=i + 3, column=2, padx=10
                        )
                    tk.Label(screen, text="Result", fg="#E8E8E8", bg="#333333").grid(
                        row=10, column=1, padx=10
                    )
                    if total / 5 > 32:
                        res = "Pass"
                    else:
                        res = "Fail"
                    tk.Label(screen, text=res, fg="#E8E8E8", bg="#333333").grid(
                        row=10, column=2, padx=10
                    )
                else:
                    messagebox.showinfo("Error", "Result does not exist")
            else:
                messagebox.showwarning("Error", "ID Not found")
        else:
            messagebox.showinfo("Error", "Fill the forms correctly to continue")


class Page11_MakeResult(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(PageThreePart1_Dashboard),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=8)
        tk.Label(
            self, text="Add Result", font=("Chiller", 30), fg="#E8E8E8", bg="#333333"
        ).grid(row=1, column=2)

        tk.Label(
            self, text="Id", font=("Segoe Print", 15), fg="#E8E8E8", bg="#333333"
        ).grid(row=2, column=1)
        Sid = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        Sid.grid(row=2, column=2)

        tk.Label(self, text="Math's Marks", fg="#E8E8E8", bg="#333333").grid(
            row=3, column=1
        )
        maths = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        maths.grid(row=3, column=2)

        tk.Label(self, text="Computer's Marks", fg="#E8E8E8", bg="#333333").grid(
            row=4, column=1
        )
        comp = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        comp.grid(row=4, column=2)

        tk.Label(self, text="English's Marks", fg="#E8E8E8", bg="#333333").grid(
            row=5, column=1
        )
        eng = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        eng.grid(row=5, column=2)

        tk.Label(self, text="Physics's Marks", fg="#E8E8E8", bg="#333333").grid(
            row=6, column=1
        )
        phy = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        phy.grid(row=6, column=2)

        tk.Label(self, text="Chemistry's Marks", fg="#E8E8E8", bg="#333333").grid(
            row=7, column=1
        )
        che = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        che.grid(row=7, column=2)

        tk.Label(self, text="Exam Type", fg="#E8E8E8", bg="#333333").grid(
            row=8, column=1, padx=5, pady=5
        )

        ExamType = [
            "First Unit test",
            "Second Unit test",
            "Half Yearly Exam",
            "Annual Exam",
        ]
        ExamTypeVar = StringVar(self, "First Unit test")
        Menu = OptionMenu(self, ExamTypeVar, *ExamType)
        Menu.config(bg="#333333", bd=0, fg="#E8E8E8", activebackground="#333333")
        Menu["menu"].config(bg="#333333", fg="#E8E8E8", activebackground="#1F8EE7")
        Menu.grid(row=8, column=2)

        tk.Label(self, text="Exam Year", fg="#E8E8E8", bg="#333333").grid(
            row=9, column=1, padx=5, pady=5
        )

        Time = ctime(time())  # Returns current time
        year = int(Time[-4:])
        ExamYear = []
        for i in range(10):
            ExamYear.append(year - i)
        ExamYearVar = StringVar(self, year)

        Menu1 = OptionMenu(self, ExamYearVar, *ExamYear)
        Menu1.config(bg="#333333", bd=0, fg="#E8E8E8", activebackground="#333333")
        Menu1["menu"].config(bg="#333333", fg="#E8E8E8", activebackground="#1F8EE7")
        Menu1.grid(row=9, column=2)

        tk.Label(self, text="Pin", fg="#E8E8E8", bg="#333333").grid(row=10, column=1)

        Pin = tk.Entry(self, show="*", fg="#E8E8E8", bg="#333333")
        Pin.grid(row=10, column=2)

        tk.Button(
            self,
            text="Proceed",
            command=lambda: self.RegisterResult(
                master,
                ExamTypeVar.get() + ExamYearVar.get(),
                Sid.get(),
                maths.get(),
                comp.get(),
                eng.get(),
                phy.get(),
                che.get(),
                Pin.get(),
            ),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=11, column=3, pady=10, padx=3)

    def RegisterResult(self, master, ExamID, Sid, math, comp, eng, phy, che, PINraw):
        ExamID = "RESULT" + ASAPtools.removeSpace(self, ExamID)
        def_Query = (
            "CREATE TABLE IF NOT EXISTS "
            + ExamID
            + " (id INTEGER PRIMARY KEY,marks_maths float,marks_computer float,marks_english float,marks_physics float,marks_chemistry float);"
        )

        ASAPtools.sqlite3_run(self, def_Query)

        if gpin.get() == PINraw:
            if (
                ASAPtools.isnotNull(self, Sid, math, phy, comp, eng, che)
                and ASAPtools.checkDigit(self, math, eng, phy, che, comp, Sid)
                and ASAPtools.inLimit(self, 0, 100, math, comp, eng, phy, che)
            ):
                if ASAPtools.ValidateId(self, Sid, "Students"):
                    if not (ASAPtools.ValidateId(self, Sid, ExamID)):
                        VALUE = (
                            "("
                            + str(Sid)
                            + ","
                            + math
                            + ","
                            + comp
                            + ","
                            + eng
                            + ","
                            + phy
                            + ","
                            + che
                            + ");"
                        )
                        sqlite_query = (
                            "Insert into "
                            + ExamID
                            + "(id,marks_maths,marks_computer,marks_english,marks_physics,marks_chemistry) values"
                            + VALUE
                        )
                        ASAPtools.sqlite3_run(self, sqlite_query)
                        messagebox.showinfo("Success", "Registered result successfully")
                        master.switch_frame(PageThreePart1_Dashboard)
                    else:
                        messagebox.showinfo("Error", "Result already created")
                else:
                    messagebox.showwarning("Error", "ID Not found")
            else:
                messagebox.showinfo(
                    "Invalid entry", "Fill all the entry correctly to proceed"
                )
        elif PINraw == "":
            messagebox.showinfo(
                "Invalid entry", "Fill all the entry correctly to proceed"
            )
        else:
            messagebox.showerror("Invalid PIN", "Re-enter correct PIN")


class Page12_UpdateResult(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#333333")
        self.makeWidgets(master)

    def makeWidgets(self, master):
        tk.Button(
            self,
            text="<Back",
            command=lambda: master.switch_frame(PageThreePart1_Dashboard),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Logout",
            command=lambda: ASAPtools.logout(self, master),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=0, column=8)
        tk.Label(
            self, text="Update Result", font=("Chiller", 30), fg="#E8E8E8", bg="#333333"
        ).grid(row=1, column=2)

        tk.Label(self, text="Enter Id of Student", fg="#E8E8E8", bg="#333333").grid(
            row=2, column=1, padx=5, pady=5
        )

        Sid = tk.Entry(self, fg="#E8E8E8", bg="#333333")
        Sid.grid(row=2, column=2)

        tk.Label(self, text="Exam Type", fg="#E8E8E8", bg="#333333").grid(
            row=3, column=1, padx=5, pady=5
        )

        ExamType = [
            "First Unit test",
            "Second Unit test",
            "Half Yearly Exam",
            "Annual Exam",
        ]
        ExamTypeVar = StringVar(self, "First Unit test")
        Menu = OptionMenu(self, ExamTypeVar, *ExamType)
        Menu.config(bg="#333333", bd=0, fg="#E8E8E8", activebackground="#333333")
        Menu["menu"].config(bg="#333333", fg="#E8E8E8", activebackground="#1F8EE7")
        Menu.grid(row=3, column=2)

        tk.Label(self, text="Exam Year", fg="#E8E8E8", bg="#333333").grid(
            row=4, column=1, padx=5, pady=5
        )
        Time = ctime(time())  # Returns current time
        year = int(Time[-4:])
        ExamYear = []
        for i in range(10):
            ExamYear.append(year - i)
        ExamYearVar = StringVar(self, year)

        Menu1 = OptionMenu(self, ExamYearVar, *ExamYear)
        Menu1.config(bg="#333333", bd=0, fg="#E8E8E8", activebackground="#333333")
        Menu1["menu"].config(bg="#333333", fg="#E8E8E8", activebackground="#1F8EE7")
        Menu1.grid(row=4, column=2)

        tk.Button(
            self,
            text="Proceed",
            command=lambda: self.modifyUIResult(
                master, Sid.get(), ExamTypeVar.get() + ExamYearVar.get()
            ),
            padx=3,
            bg="#1F8EE7",
            fg="#E8E8E8",
            bd=0,
            activebackground="#3297E9",
        ).grid(row=5, column=3, pady=10, padx=3)

    def modifyUIResult(self, master, Sid, ExamID):
        def_Query = "CREATE TABLE IF NOT EXISTS STUDENTS (id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Age INT NOT NULL, Gender CHAR(1) NOT NULL, Class INT NOT NULL, Father_name TEXT, Mother_name TEXT, Social_Status varchar(3), Religion TEXT);"
        ExamID = "RESULT" + ASAPtools.removeSpace(self, ExamID)
        def_Query2 = (
            "CREATE TABLE IF NOT EXISTS "
            + ExamID
            + " (id INTEGER PRIMARY KEY,marks_maths float,marks_computer float,marks_english float,marks_physics float,marks_chemistry float);"
        )
        ASAPtools.sqlite3_run(self, def_Query, def_Query2)
        if ASAPtools.isnotNull(self, Sid, ExamID) and ASAPtools.checkDigit(self, Sid):
            if ASAPtools.ValidateId(self, Sid, "students"):
                if ASAPtools.ValidateId(self, Sid, ExamID):
                    sqlite_query = (
                        "Select marks_maths,marks_computer,marks_english,marks_physics,marks_chemistry from "
                        + ExamID
                        + " where id="
                        + Sid
                    )
                    out = ASAPtools.sqlite3_run(self, sqlite_query)
                    data = out[0][0]
                    tk.Label(
                        self, text="Math's Marks", fg="#E8E8E8", bg="#333333"
                    ).grid(row=6, column=1)
                    maths = tk.Entry(self, fg="#E8E8E8", bg="#333333")
                    maths.insert(0, data[0])
                    maths.grid(row=6, column=2)

                    tk.Label(
                        self, text="Computer's Marks", fg="#E8E8E8", bg="#333333"
                    ).grid(row=7, column=1)
                    comp = tk.Entry(self, fg="#E8E8E8", bg="#333333")
                    comp.insert(0, data[1])
                    comp.grid(row=7, column=2)

                    tk.Label(
                        self, text="English's Marks", fg="#E8E8E8", bg="#333333"
                    ).grid(row=8, column=1)
                    eng = tk.Entry(self, fg="#E8E8E8", bg="#333333")
                    eng.insert(0, data[2])
                    eng.grid(row=8, column=2)

                    tk.Label(
                        self, text="Physics's Marks", fg="#E8E8E8", bg="#333333"
                    ).grid(row=9, column=1)
                    phy = tk.Entry(self, fg="#E8E8E8", bg="#333333")
                    phy.insert(0, data[3])
                    phy.grid(row=9, column=2)

                    tk.Label(
                        self, text="Chemistry's Marks", fg="#E8E8E8", bg="#333333"
                    ).grid(row=10, column=1)
                    che = tk.Entry(self, fg="#E8E8E8", bg="#333333")
                    che.insert(0, data[4])
                    che.grid(row=10, column=2)

                    tk.Label(self, text="Pin", fg="#E8E8E8", bg="#333333").grid(
                        row=11, column=1
                    )

                    Pin = tk.Entry(self, show="*", fg="#E8E8E8", bg="#333333")
                    Pin.grid(row=11, column=2)

                    tk.Button(
                        self,
                        text="Modify",
                        command=lambda: self.UpdateResult(
                            master,
                            ExamID,
                            Sid,
                            maths.get(),
                            comp.get(),
                            eng.get(),
                            phy.get(),
                            che.get(),
                            Pin.get(),
                        ),
                        padx=3,
                        bg="#1F8EE7",
                        fg="#E8E8E8",
                        bd=0,
                        activebackground="#3297E9",
                    ).grid(row=12, column=3, pady=10, padx=3)
                else:
                    messagebox.showinfo("Error", "Result does not exist")
            else:
                messagebox.showwarning("Error", "ID Not found")
        else:
            messagebox.showinfo("Error", "Fill the forms correctly to continue")

    def UpdateResult(self, master, ExamID, Sid, math, comp, eng, phy, che, PINraw):
        if gpin.get() == PINraw:
            if (
                ASAPtools.isnotNull(self, Sid, math, eng, comp, phy, che)
                and ASAPtools.checkDigit(self, math, eng, phy, che, comp)
                and ASAPtools.inLimit(self, 0, 100, phy, che, comp, math, eng)
            ):
                sqlite_query = (
                    "Update "
                    + ExamID
                    + " set marks_maths="
                    + math
                    + ",marks_computer="
                    + comp
                    + ",marks_english="
                    + eng
                    + ",marks_physics="
                    + phy
                    + ",marks_chemistry="
                    + che
                )
                ASAPtools.sqlite3_run(self, sqlite_query)
                messagebox.showinfo("Success", "Updated result successfully")
                master.switch_frame(PageThreePart1_Dashboard)
            else:
                messagebox.showinfo(
                    "Invalid entry", "Fill all the entry correctly to proceed"
                )
        elif PINraw == "":
            messagebox.showinfo(
                "Invalid entry", "Fill all the entry correctly to proceed"
            )
        else:
            messagebox.showerror("Invalid PIN", "Re-enter correct PIN")


# Main Program
if __name__ == "__main__":
    app = Asap()
    app.title("Asap:Your school assistant")
    app.resizable(0, 0)
    Icon = PhotoImage(file="icon.png")
    app.iconphoto(False, Icon)
    app.mainloop()
