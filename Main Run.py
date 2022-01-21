import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time
import pymysql.cursors
from tkinter import messagebox

#####Window is our Main frame of system
window = tk.Tk()
window.title("FaceOLogger( Attendance marking system BVICAM )")

window.geometry('1280x720')
window.configure(background='white')

###GUI for admin
def stu_regis():
    global sa
    sa = tk.Tk()
    sa.iconbitmap('AMS.ico')
    sa.title("Enter subject name...")
    sa.geometry('720x800')
    sa.configure(background='snow')
    


    SI = tk.Button(sa, text="Student Detail",fg="white",command=admin_panel  ,bg="blue2"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
    SI.place(x=100, y=200)

    quitWindow = tk.Button(sa, text="Manually Fill Attendance", command=manually_fill  ,fg="black"  ,bg="lawn green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
    quitWindow.place(x=500, y=200)


####GUI for manually fill attendance

def manually_fill():
    global sb
    sb = tk.Tk()
    sb.iconbitmap('AMS.ico')
    sb.title("Enter subject name...")
    sb.geometry('580x320')
    sb.configure(background='white')
    SUB = tk.Label(sb, text="Enter Subject", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
    SUB.place(x=30, y=100)
    global SUB_ENTRY

    SUB_ENTRY = tk.Entry(sb, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
    SUB_ENTRY.place(x=250, y=105)

    def err_screen_for_subject():

        def ec_delete():
            ec.destroy()
        global ec
        ec = tk.Tk()
        ec.geometry('300x100')
        ec.iconbitmap('AMS.ico')
        ec.title('Warning!!')
        ec.configure(background='snow')
        Label(ec, text='Please enter your subject name!!!', fg='red', bg='white', font=('times', 16, ' bold ')).pack()
        Button(ec, text='OK', command=ec_delete, fg="black", bg="lawn green", width=9, height=1, activebackground="Red",
               font=('times', 15, ' bold ')).place(x=90, y=50)

    def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        
        subb= SUB_ENTRY.get()
        

        if subb=='':
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.iconbitmap('AMS.ico')
            MFW.title("Manually attendance of "+ str(subb))
            MFW.geometry('880x470')
            MFW.configure(background='snow')

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry('330x100')
                errsc2.iconbitmap('AMS.ico')
                errsc2.title('Warning!!')
                errsc2.configure(background='white')
                Label(errsc2, text='Please enter Student & Enrollment!!!', fg='red', bg='white',
                      font=('times', 16, ' bold ')).pack()
                Button(errsc2, text='OK', command=del_errsc2, fg="black", bg="lawn green", width=9, height=1,
                       activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == '1':  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="white", bg="blue2",
                           font=('times', 15, ' bold '))
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(MFW, text="Enter Student name", width=15, height=2, fg="white", bg="blue2",
                                font=('times', 15, ' bold '))
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20,validate='key', bg="yellow", fg="red", font=('times', 23, ' bold '))
            ENR_ENTRY['validatecommand'] = (ENR_ENTRY.register(testVal), '%P', '%d')
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(MFW, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            ####get important variable
            def enter_data_DB():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT=='':
                    err_screen1()
                elif STUDENT=='':
                    err_screen1()
                else:
                    time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = time.split(":")
                    
                    try:
                        
                        conn=pymysql.connect(host='localhost',user='root',password='',db='subject')
                        a=conn.cursor()
                        a.execute("insert " + subb + "(Stu_Name,Enrollment)values('"+STUDENT+"','"+ENROLLMENT+"')")
                        conn.commit()
                        messagebox.showinfo("message","Successfully Updated!!")
                    except:
                        
                        messagebox.showinfo("message","Try After Some time ")
                        conn.rollback()
                        conn.close()
            


            c1ear_enroll = tk.Button(MFW, text="Clear", command=remove_enr, fg="black", bg="deep pink", width=10, height=1,activebackground="Red", font=('times', 15, ' bold '))
            c1ear_enroll.place(x=690, y=100)

            c1ear_student = tk.Button(MFW, text="Clear", command=remove_student, fg="black", bg="deep pink", width=10, height=1, activebackground="Red", font=('times', 15, ' bold '))
            c1ear_student.place(x=690, y=200)

            DATA_SUB = tk.Button(MFW, text="SUBMIT",command=enter_data_DB, fg="black", bg="lime green", width=20, height=2, activebackground="Red", font=('times', 15, ' bold '))
            DATA_SUB.place(x=290, y=300)


            MFW.mainloop()

    fill_manual_attendance = tk.Button(sb, text="Fill Attendance",command=fill_attendance, fg="white", bg="deep pink", width=20, height=2, activebackground="Red", font=('times', 15, ' bold '))
    fill_manual_attendance.place(x=250, y=160)
    sb.mainloop()


##For clear textbox
def clear():
    txt.delete(first=0, last=22)

def clear1():
    txt2.delete(first=0, last=22)
def del_sc1():
    sc1.destroy()
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.iconbitmap('AMS.ico')
    sc1.title('Warning!!')
    sc1.configure(background='snow')
    Label(sc1,text='Enrollment & Name required!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    Button(sc1,text='OK',command=del_sc1,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)

##Error screen2
def del_sc2():
    sc2.destroy()
def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.iconbitmap('AMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='snow')
    Label(sc2,text='Please enter your subject name!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    Button(sc2,text='OK',command=del_sc2,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)

###For take images for datasets
def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Enrollment = txt.get()
            Name = txt2.get()
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                   
                    sampleNum = sampleNum + 1
                   
                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 70:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]

            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=450, y=400)

        try:

            conn=pymysql.connect(host='localhost',user='root',password='',db='attendance')
            a=conn.cursor()
            a.execute("insert into Student_data(Name,Enrollment)values('"+l2+"','"+l1+"')")
            conn.commit()
            messagebox.showinfo("message","Successfully Updated!!")
        except:
            
            messagebox.showinfo("message","Try after some time")
            conn.rollback()
            conn.close()
        
    

###for choose subject and fill attendance
def subjectchoose():
    def Fillattendances():
        sub=tx.get()
        now = time.time() 
        future = now + 10
        if time.time() < future:
            if sub == '':
                err_screen1()
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create() 
                try:
                    recognizer.read("TrainingImageLabel\Trainner.yml")
                except:
                    e = 'Model not found,Please train model'
                    Notifica.configure(text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
                    Notifica.place(x=20, y=250)

                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv("StudentDetails\StudentDetails.csv")
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name', 'Date', 'Time']
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        if (conf <70):
                            #print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            global tt, currentId,currentName
                            tt = str(Id) + "-" + aa
                            currentId = str(Id)
                            En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                currentName= convert(aa)

                try:
                    
                    conn=pymysql.connect(host='localhost',user='root',password='',db='subject')
                    a=conn.cursor()
                    a.execute("insert " + Subject + "(Stu_Name,Enrollment)values('"+currentName+"','"+currentId+"')")
                    conn.commit()
                    messagebox.showinfo("message","Successfully Updated!!")
                except:
                    
                    messagebox.showinfo("message","Try Biometric method")
                    conn.rollback()
                    conn.close()

                
                fileName = "Attendance/" + Subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                
                print(attendance)
                currentName= convert(aa)
                attendance.to_csv(fileName, index=False)
                             

    ###windo is frame for subject chooser
    windo = tk.Tk()
    windo.iconbitmap('AMS.ico')
    windo.title("Enter subject name...")
    windo.geometry('580x320')
    windo.configure(background='snow')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                            height=2, font=('times', 15, 'bold'))

  
    sub = tk.Label(windo, text="Enter Subject", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
    sub.place(x=30, y=100)

    tx = tk.Entry(windo, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
    tx.place(x=250, y=105)

    fill_a = tk.Button(windo, text="Fill Attendance", fg="white",command=Fillattendances, bg="deep pink", width=20, height=2,
                       activebackground="Red", font=('times', 15, ' bold '))
    fill_a.place(x=250, y=160)
    windo.mainloop()

def convert(aa): 
  
    # initialization of string to "" 
    str1 = "" 
  
    # using join function join the list s by  
    # separating words by str1 
    return(str1.join(aa))

def stu_info():
    
    conn=pymysql.connect(host="localhost",user="root",password="",db='attendance')
    var = conn.cursor()
    var.execute("select * from student_data")
    v = var.fetchall()
    show = Tk()
    show.geometry("730x800")
    show.iconbitmap('AMS.ico')
    show.resizable(False,False)
    show.title("Student Details")
    show.configure(background='white')
    vary=150
    headlb=Label(show,text="Student Details",bg="white", fg="black",font=('times', 30, 'italic bold '),width=15,height=1).place(x=160,y=20)
    #-------------------------------Label of the Table---------------------------------#
    lb1 = Label(show,text="Student Name ",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=70,y=100)
    lb2 = Label(show,text="Enrollment",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=270,y=100)
    lb3 = Label(show,text="Date",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=470,y=100)
    for i in range(0,var.rowcount):
        lb1 = Label(show,text=v[i][0],width=15,bg="white",bd=5).place(x=110,y=vary)
        lb2 = Label(show,text=v[i][1],width=15,bg="white",bd=5).place(x=310,y=vary)
        lb3 = Label(show,text=v[i][2],width=15,bg="white",bd=5).place(x=510,y=vary)
        vary+=40 
    conn.commit()

    
def err_screen_for_subject():
    def ec_delete():
        ec.destroy()
    global ec
    ec = tk.Tk()
    ec.geometry('300x100')
    ec.iconbitmap('AMS.ico')
    ec.title('Warning!!')
    ec.configure(background='snow')
    Label(ec, text='Please enter your subject name!!!', fg='red', bg='white', font=('times', 16, ' bold ')).pack()
    Button(ec, text='OK', command=ec_delete, fg="black", bg="lawn green", width=9, height=1, activebackground="Red",font=('times', 15, ' bold ')).place(x=90, y=50)


def admin_sub():
    global sb
    sb = tk.Tk()
    sb.iconbitmap('AMS.ico')
    sb.title("Enter subject name.")
    sb.geometry('600x400')
    sb.configure(background='white')

    def mathematics():
        sb.destroy()
        conn=pymysql.connect(host="localhost",user="root",password="",db='subject')
        var = conn.cursor()
        var.execute("select * from mathematics")
        v = var.fetchall()
        show = Tk()
        show.geometry("730x800")
        show.resizable(False,False)
        show.iconbitmap('AMS.ico')
        show.title("Maths Attendance sheet")
        show.configure(background='white')
        vary=150
        headlb=Label(show,text="Mathematics Attendance Sheet",bg="white", fg="black",font=('times', 30, 'bold '),width=25,height=1).place(x=70,y=20)
        #-------------------------------Label of the Table---------------------------------#
        lb1 = Label(show,text="Student Name ",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=70,y=100)
        lb2 = Label(show,text="Enrollment",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=270,y=100)
        lb3 = Label(show,text="Date",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=470,y=100)
        for i in range(0,var.rowcount):
            lb1 = Label(show,text=v[i][0],width=15,bg="white",bd=5).place(x=110,y=vary)
            lb2 = Label(show,text=v[i][1],width=15,bg="white",bd=5).place(x=310,y=vary)
            lb3 = Label(show,text=v[i][2],width=15,bg="white",bd=5).place(x=510,y=vary)
            vary+=40 
        conn.commit()

    def java():
        sb.destroy()
        conn=pymysql.connect(host="localhost",user="root",password="",db='subject')
        var = conn.cursor()
        var.execute("select * from java")
        v = var.fetchall()
        show = Tk()
        show.geometry("730x800")
        show.iconbitmap('AMS.ico')
        show.resizable(False,False)
        show.title("Jav Attendance sheet")
        show.configure(background='white')
        vary=150
        headlb=Label(show,text="Java Attendance Sheet",bg="white", fg="black",font=('times', 30, 'bold '),width=25,height=1).place(x=70,y=20)
        #-------------------------------------Label of the Table--------------------------------------#
        lb1 = Label(show,text="Student Name ",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=70,y=100)
        lb2 = Label(show,text="Enrollment",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=270,y=100)
        lb3 = Label(show,text="Date",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=470,y=100)
        for i in range(0,var.rowcount):
            lb1 = Label(show,text=v[i][0],width=15,bg="white",bd=5).place(x=110,y=vary)
            lb2 = Label(show,text=v[i][1],width=15,bg="white",bd=5).place(x=310,y=vary)
            lb3 = Label(show,text=v[i][2],width=15,bg="white",bd=5).place(x=510,y=vary)
            vary+=40
        
        conn.commit()

    def linux():
        sb.destroy()
        conn=pymysql.connect(host="localhost",user="root",password="",db='subject')
        var = conn.cursor()
        var.execute("select * from linux")
        v = var.fetchall()
        show = Tk()
        show.geometry("730x800")
        show.iconbitmap('AMS.ico')
        show.resizable(False,False)
        show.title("Linux Attendance sheet")
        show.configure(background='white')
        vary=150
        headlb=Label(show,text="Linux Attendance Sheet",bg="white", fg="black",font=('times',30, 'bold'),width=25,height=1).place(x=70,y=20)
        #-------------------------------Label of the Table---------------------------------#
        lb1 = Label(show,text="Student Name ",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=70,y=100)
        lb2 = Label(show,text="Enrollment",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=270,y=100)
        lb3 = Label(show,text="Date",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=470,y=100)
        for i in range(0,var.rowcount):
            lb1 = Label(show,text=v[i][0],width=15,bg="white",bd=5).place(x=110,y=vary)
            lb2 = Label(show,text=v[i][1],width=15,bg="white",bd=5).place(x=310,y=vary)
            lb3 = Label(show,text=v[i][2],width=15,bg="white",bd=5).place(x=510,y=vary)
            vary+=40 
        conn.commit()

    def multimedia():
        sb.destroy()
        conn=pymysql.connect(host="localhost",user="root",password="",db='subject')
        var = conn.cursor()
        var.execute("select * from multimedia")
        v = var.fetchall()
        show = Tk()
        show.geometry("730x800")
        show.resizable(False,False)
        show.iconbitmap('AMS.ico')
        show.title("Multimedia Attendance sheet")
        show.configure(background='white')
        vary=150
        headlb=Label(show,text="Multimedia Attendance Sheet",bg="white", fg="black",font=('times', 30, 'bold '),width=25,height=1).place(x=70,y=20)
        #-------------------------------Label of the Table---------------------------------#
        lb1 = Label(show,text="Student Name ",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=70,y=100)
        lb2 = Label(show,text="Enrollment",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=270,y=100)
        lb3 = Label(show,text="Date",font=('times',15,'bold'),width=15,bg="white",bd=5).place(x=470,y=100)
        for i in range(0,var.rowcount):
            lb1 = Label(show,text=v[i][0],width=15,bg="white",bd=5).place(x=110,y=vary)
            lb2 = Label(show,text=v[i][1],width=15,bg="white",bd=5).place(x=310,y=vary)
            lb3 = Label(show,text=v[i][2],width=15,bg="white",bd=5).place(x=510,y=vary)
            vary+=40 
        conn.commit()
       

    maths = tk.Button(sb, text="Mathematics", command = mathematics, fg="black", bg="lime green", width=20, height=2,activebackground="Red", font=('times', 15, ' bold '))
    maths.place(x=30, y=60)
    linux = tk.Button(sb, text="Linux",fg="black",command = linux, bg="blue", width=20, height=2,activebackground="Red", font=('times', 15, ' bold '))
    linux.place(x=300, y=60)
    java = tk.Button(sb, text="Java", fg="black", bg="blue", command = java, width=20, height=2,activebackground="Red", font=('times', 15, ' bold '))
    java.place(x=30, y=250)
    multimedia = tk.Button(sb, text="Multemedia", fg="black", bg="lime green",command = multimedia ,width=20, height=2,activebackground="Red", font=('times', 15, ' bold '))
    multimedia.place(x=300, y=250)

    
def admin_panel():
    win = tk.Tk()
    win.iconbitmap('AMS.ico')
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='white')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'virender' :
            if password == 'viru01':
                win.destroy()
                global sa
                sa = tk.Tk()
                sa.iconbitmap('AMS.ico')
                sa.title("Admin Panel")
                sa.geometry('600x400')
                sa.configure(background='white')

    
                SI = tk.Button(sa, text="Student Detail",fg="white",command= stu_info ,bg="blue2"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
                SI.place(x=50, y=150)

                quitWindow = tk.Button(sa, text="Attendance Sheet", command=admin_sub  ,fg="black"  ,bg="lawn green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
                quitWindow.place(x=330, y=150)

         
            else:
                valid = 'Incorrect ID or Password'
                Nt.configure(text=valid, bg="red", fg="black", width=38, font=('times', 19, 'bold'))
                Nt.place(x=120, y=350)

        else:
            valid ='Incorrect ID or Password'
            Nt.configure(text=valid, bg="red", fg="black", width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=350)


    Nt = tk.Label(win, text="Attendance filled Successfully", bg="Green", fg="white", width=40,
                  height=2, font=('times', 19, 'bold'))
    # Nt.place(x=120, y=350)

    un = tk.Label(win, text="Enter username", width=15, height=2, fg="white", bg="blue2",
                   font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password", width=15, height=2, fg="white", bg="blue2",
                  font=('times', 15, ' bold '))
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20,show="*", bg="yellow", fg="red", font=('times', 23, ' bold '))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=c00, fg="black", bg="deep pink", width=10, height=1,
                            activebackground="Red", font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=c11, fg="black", bg="deep pink", width=10, height=1,
                   activebackground="Red", font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Login = tk.Button(win, text="LogIn", fg="black", bg="lime green", width=20,
                       height=2,
                       activebackground="Red",command=log_in, font=('times', 15, ' bold '))
    Login.place(x=290, y=250)
    win.mainloop()


###For train the model
def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces,Id
        faces, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        l='please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("TrainingImageLabel\Trainner.yml")
    except Exception as e:
        q='Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    res = "Model Trained"  # +",".join(str(f) for f in Id)
    Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
  
    faceSamples = []
    Ids = []
    for imagePath in imagePaths:

        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
  
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(imageNp)
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.iconbitmap('AMS.ico')

def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)

message = tk.Label(window, text=" FaceOLogger ", bg="white", fg="red", width=15,
                   height=2, font=('times', 40, 'bold '))

message.place(x=430, y=40)

Notification = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,
                      height=2, font=('times', 17, 'bold'))

lbl = tk.Label(window, text="Enter Enrollment", width=20, height=2, fg="black", bg="deep pink", font=('times', 15, ' bold '))
lbl.place(x=200, y=200)

def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True

txt = tk.Entry(window, validate="key", width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
txt['validatecommand'] = (txt.register(testVal),'%P','%d')
txt.place(x=550, y=210)

lbl2 = tk.Label(window, text="Enter Name", width=20, fg="black", bg="deep pink", height=2, font=('times', 15, ' bold '))
lbl2.place(x=200, y=300)

txt2 = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
txt2.place(x=550, y=310)

clearButton = tk.Button(window, text="Clear",command=clear,fg="black"  ,bg="deep pink"  ,width=10  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=210)

clearButton1 = tk.Button(window, text="Clear",command=clear1,fg="black"  ,bg="deep pink"  ,width=10 ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton1.place(x=950, y=310)

AP = tk.Button(window, text="Check Register students",command=admin_panel,fg="black"  ,bg="cyan"  ,width=19 ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
AP.place(x=990, y=410)

takeImg = tk.Button(window, text="Take Images",command=take_img,fg="black"  ,bg="lawn green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=150, y=500)


FA = tk.Button(window, text="Automatic Attendace",fg="black",command=subjectchoose  ,bg="lawn green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
FA.place(x=550, y=500)

quitWindow = tk.Button(window, text="Manually Fill Attendance", command=manually_fill  ,fg="black"  ,bg="lawn green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=950, y=500)

window.mainloop() 
