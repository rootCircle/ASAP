# =============================================================================
# Author@Microsoftlabs
# Name of the software:ASAP
# Version:1.0.0.1
# =============================================================================
import tkinter
from tkinter import StringVar,Toplevel

import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
import sqlite3


#Insert student details in database
def studentInsertDb(name,age,fname,mname,Class,soc,gender,religon):

    try:
        sqliteConnection=sqlite3.connect('asap.db')
        cursor=sqliteConnection.cursor()
        def_Query="CREATE TABLE IF NOT EXISTS STUDENTS (id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Age INT NOT NULL, Gender CHAR(1) NOT NULL, Class INT NOT NULL, Father_name TEXT, Mother_name TEXT, Social_Status varchar(3), Religon TEXT);"
        cursor.execute(def_Query)
        Query_2="select count(*) from students"
        cursor.execute(Query_2)
        numberofstudent=cursor.fetchone()[0]
        religonval=""
        if religon!="NAN":
            religonval=religon
        else:
            religonval=otherReligonInput.get()
        VALUE="("+str(numberofstudent)+",'"+name+"',"+age+",'"+gender+"',"+Class+",'"+fname+"','"+mname+"','"+soc+"','"+religonval+"');"
        sqlite_Query="Insert into students(id,Name,Age,Gender,Class,Father_name,Mother_name,Social_Status,Religon) values"+VALUE
        cursor.execute(sqlite_Query)
        sqliteConnection.commit()
        cursor.close()
        screen1.destroy()
    except sqlite3.Error as error:
        print(error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()


#Insert admin details in database
def loginDb(name,age,gender,Username,Password,Repassword,PIN):
    if Password==Repassword:
        try:
            sqliteConnection=sqlite3.connect('asap.db')
            cursor=sqliteConnection.cursor()
            def_Query= "CREATE TABLE IF NOT EXISTS ADTEA(id INTEGER PRIMARY KEY,Name TEXT NOT NULL,Age INT NOT NULL,Gender CHAR(1),Username TEXT NOT NULL  UNIQUE, Password TEXT Not Null,PIN INTEGER NOT NULL);"
            cursor.execute(def_Query)

            Query_2="select count(*) from ADTEA"
            cursor.execute(Query_2)
            numberofADTEA=cursor.fetchone()[0]
            VALUE="("+str(numberofADTEA)+",'"+name+"',"+age+",'"+gender+"','"+Username+"','"+Password+"',"+PIN+");"
            sqlite_Query="Insert into ADTEA(id,Name,Age,Gender,Username,Password,PIN) values"+VALUE
            cursor.execute(sqlite_Query)
            sqliteConnection.commit()
            cursor.close()
            screen4.destroy()
        except sqlite3.Error as error:
            print(error)

        finally:
            if sqliteConnection:
                sqliteConnection.close()



#checks user creditinals
def login_Check():
    try:
        sqliteConnection=sqlite3.connect('asap.db')
        cursor=sqliteConnection.cursor()
        sqlite_Query="Select id,Username,Password,Pin from ADTEA"
        cursor.execute(sqlite_Query)
        record=cursor.fetchall()
        cuser=username.get()
        cpass=password.get()
        for (aid,usern,pas,pin) in record:
            if cuser==usern and cpass==pas:
                        cursor.execute("Select Name,Gender,PIN from ADTEA Where id ="+str(aid))
                        record=cursor.fetchone()
                        nameG=record[0]
                        global dvar
                        dvar=StringVar()
                        dvar.set("Welcome "+nameG)
                        dashboard()
                        screen2.destroy()
            else:
                        var.set("Invalid Credentials")
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()


def login():
    global username,password,screen2
    screen2=Toplevel(screen)
    #Defining Label and Textfield
    Label1=ttk.Label(screen2,text="Login",font=("Chiller",30))
    Label1.grid(row=0,column=2)

    Label2=ttk.Label(screen2,text="Username")
    Label2.grid(row=1,column=1,padx=25)

    username=ttk.Entry(screen2)
    username.grid(row=1,column=2)

    Label3=ttk.Label(screen2,text="Password")
    Label3.grid(row=2,column=1)

    password=ttk.Entry(screen2,show="*")
    password.grid(row=2,column=2)

    Button=ttk.Button(screen2,text="Login",command=login_Check)
    Button.grid(row=3,column=4)

    #Defining a variable for Label4
    global var
    var=StringVar()
    Label4=ttk.Label(screen2,textvariable=var)
    Label4.grid(row=4,column=1)



def dashboard():
    global screen3

    screen3=Toplevel(screen)
    Label1=ttk.Label(screen3,text="Dashboard",font=("Chiller",30))
    Label1.grid(row=0,column=2)
    Label2=ttk.Label(screen3,textvariable=dvar)
    Label2.grid(row=1,column=2)
    signupst=ttk.Button(screen3,text="Register student",command=signup_page_student)
    signupst.grid(row=3,column=2)
    searchstu=ttk.Button(screen3,text="Search student",command=search_students)
    searchstu.grid(row=4,column=2)

def signup_page_Admin():
    global screen4
    screen4=Toplevel(screen)
    screen4.title("Admin sign up")

    Label1=ttk.Label(screen4,text="Register",font=("Chiller",30))
    Label1.grid(row=0,column=2)

    Label2=ttk.Label(screen4,text="Name")
    Label2.grid(row=1,column=1,padx=25)

    Aname=ttk.Entry(screen4)
    Aname.grid(row=1,column=2)

    Label3=ttk.Label(screen4,text="Age")
    Label3.grid(row=2,column=1)

    AAge=ttk.Entry(screen4)
    AAge.grid(row=2,column=2)

    Label4=ttk.Label(screen4,text="Gender")
    Label4.grid(row=3,column=1)

    Agender=StringVar(screen4,"M")
    GEN={"Male":"M","Female":"F","Not specified":"N"}
    i=2
    for (text,value) in GEN.items():
        ttk.Radiobutton(screen4,text=text,variable=Agender,value=value).grid(row=3,column=i)
        i+=1

    Label5=ttk.Label(screen4,text="Pin")
    Label5.grid(row=4,column=1)

    Pin=ttk.Entry(screen4,show="*")
    Pin.grid(row=4,column=2)

    Ausername=ttk.Entry(screen4)
    Ausername.grid(row=5,column=2)

    Label6=ttk.Label(screen4,text="Username")
    Label6.grid(row=5,column=1)

    APassword=ttk.Entry(screen4,show='*')
    APassword.grid(row=6,column=2)

    Label7=ttk.Label(screen4,text="Password")
    Label7.grid(row=6,column=1)

    ARepassword=ttk.Entry(screen4,show='*')
    ARepassword.grid(row=7,column=2)

    Label8=ttk.Label(screen4,text="Confirm Password")
    Label8.grid(row=7,column=1)


    ARegister=ttk.Button(screen4,text="Register",command=lambda:loginDb(Aname.get(),AAge.get(),Agender.get(),Ausername.get(),APassword.get(),ARepassword.get(),Pin.get()))
    ARegister.grid(row=8,column=3)


def search(text,criteria):
    try:
        sqliteConnection=sqlite3.connect('asap.db')
        cursor=sqliteConnection.cursor()
        if criteria not in("Age","Class"):
            sqlite_Query="Select * from students where "+criteria+"='"+text+"'"
        else:
            sqlite_Query="Select * from students where "+criteria+"="+str(text)
        cursor.execute(sqlite_Query)
        record=cursor.fetchall()
        L=["Id","Name","Age","Gender","Class","Father's name","Mother's name","Social status","Religon"]
        for i in range(0,9):
                ttk.Label(screen5,text=L[i],font=("Arial",12)).grid(row=6,column=i+1)
        co=0
        for t in record:
            co+=1
            for i in range(0,9):
                ttk.Label(screen5,text=t[i]).grid(row=7+co,column=i+1)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()


def search_students():
    global screen5
    screen5=Toplevel(screen)
    screen5.title("Search student")

    Label1=ttk.Label(screen5,text="Search Student",font=("Chiller",30))
    Label1.grid(row=0,column=2)

    Label2=ttk.Label(screen5,text="Search by")
    Label2.grid(row=1,column=1,padx=25)

    criteria=StringVar(screen5,"Name")
    options={"Name":"Name","Class":"Class","Age":"Age","Father's name":"Father_name","Mother's name":"Mother_name","Social status(GEN/OBC/SC/ST)":"Social_status","Gender(M/F/N)":"Gender","Religon":"Religon"}
    i=1
    for (text,value) in options.items():
        ttk.Radiobutton(screen5,text=text,variable=criteria,value=value).grid(row=2,column=i)
        i+=1
    text=ttk.Entry(screen5)
    text.grid(row=4,column=2)
    Button=ttk.Button(screen5,text="Search",command=lambda:search(text.get(),criteria.get()))
    Button.grid(row=5,column=3)
    screen5.mainloop()


def signup_page_student():
    global screen1
    screen1=Toplevel(screen)
    screen1.title("Register")

    Label1=ttk.Label(screen1,text="Register",font=("Chiller",30))
    Label1.grid(row=0,column=2)

    Label2=ttk.Label(screen1,text="Name")
    Label2.grid(row=1,column=1,padx=25)

    name=ttk.Entry(screen1)
    name.grid(row=1,column=2)

    Label3=ttk.Label(screen1,text="Age")
    Label3.grid(row=2,column=1)

    Age=ttk.Entry(screen1)
    Age.grid(row=2,column=2)

    Label4=ttk.Label(screen1,text="Class")
    Label4.grid(row=3,column=1)

    Class=ttk.Entry(screen1)
    Class.grid(row=3,column=2)

    Label5=ttk.Label(screen1,text="Father's Name")
    Label5.grid(row=4,column=1)

    Fname=ttk.Entry(screen1)
    Fname.grid(row=4,column=2)

    Label6=ttk.Label(screen1,text="Mother's Name")
    Label6.grid(row=5,column=1)

    Mname=ttk.Entry(screen1)
    Mname.grid(row=5,column=2)

    Label7=ttk.Label(screen1,text="Social status")
    Label7.grid(row=6,column=1)

    socstatus=StringVar(screen1,"Gen")
    SOC={"General":"GEN","OBC":"OBC","SC":"SC","ST":"ST"}
    i=2
    for (text,value) in SOC.items():
        ttk.Radiobutton(screen1,text=text,variable=socstatus,value=value).grid(row=6,column=i)
        i+=1

    Label8=ttk.Label(screen1,text="Gender")
    Label8.grid(row=7,column=1)

    gender=StringVar(screen1,"M")
    GEN={"Male":"M","Female":"F","Not specified":"N"}
    i=2
    for (text,value) in GEN.items():
        ttk.Radiobutton(screen1,text=text,variable=gender,value=value).grid(row=7,column=i)
        i+=1

    Label9=ttk.Label(screen1,text="Religon")
    Label9.grid(row=8,column=1)

    religon=StringVar(screen1,"Hindu")
    REL={"Hindu":"Hindu","Muslim":"Muslim","Christian":'Christian',"Sikh":'Sikh'}
    i=2
    for (text,value) in REL.items():
        ttk.Radiobutton(screen1,text=text,variable=religon,value=value).grid(row=8,column=i)
        i+=1
    ttk.Radiobutton(screen1,text="Other",variable=religon,value="NAN",command=other_religon).grid(row=8,column=6)


    Label10=ttk.Label(screen1,text="Pin")
    Label10.grid(row=9,column=1)

    Pin=ttk.Entry(screen1,show="*")
    Pin.grid(row=9,column=2)

    Button=ttk.Button(screen1,text="Register",command=lambda:studentInsertDb(name.get(),Age.get(),Fname.get(),Mname.get(),Class.get(),socstatus.get(),gender.get(),religon.get()))
    Button.grid(row=10,column=3)






def other_religon():
    global otherReligonInput
    otherReligonInput=ttk.Entry(screen1).grid(row=8,column=7)



def main_screen():
    global screen
    screen=tkinter.Tk()
    screen.title("Asap: Your School assistant")
    #screen.configure(background="#ff3d72")
    style= ThemedStyle(screen)
    style.set_theme("arc")
    style.set_theme_advanced("arc",brightness=0.9)
    ttk.Button(screen,text="Signup",command=signup_page_Admin).grid(row=0,column=0)
    ttk.Button(screen,text="Login",command=login).grid(row=1,column=0)
    themes=style.theme_names()
    setth=StringVar(screen,'scidmint')
    Menu=ttk.OptionMenu(screen,setth,*themes)
    Menu.grid(row=2,column=0)
    ttk.Button(screen, text="Change Theme",command=lambda:style.set_theme(setth.get())).grid(row=3,column=1)
    screen.mainloop()


main_screen()
