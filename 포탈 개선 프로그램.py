import tkinter as tk
from tkinter import messagebox
from tkinter import *

import time
import datetime
import json
#from PIL import Image, ImageTk
from collections import OrderedDict
import ftplib
import requests
import io





#알림 실시간 체크
import threading
endeded=False
def checkn(second=2.0):
    global endeded,noticelabel
    if endeded:
        return
    url = 'http://pydoctor.gq/account.json'
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    pre_msg= data["message"] #메시지
    time.sleep(2)
    url = 'http://pydoctor.gq/account.json'
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    new_msg= data["message"] #메시지
    noticelabel['text'] = new_msg
    #print(pre_msg,' vs ',new_msg)
    #print(clsaccount.message)
    if pre_msg != new_msg:
        global who
        if who==1 or who=='1':
            messagebox.showinfo("알림", "수업일정에 변경이 있습니다.\n 알림창을 확인하세요")
        else:
            pass

    
    threading.Timer(second,checkn,[second]).start()

#도서관 좌석
def lib(second=1.0):
    global libdata,labellib,libtitle,labeltime
    url = 'http://knb.cau.ac.kr/student/lib.txt'
    resp = requests.get(url=url)
    resp.encoding='utf-8'
    libdb = resp.text.split('\\n\\n')
    libdtitle,libdata = libdb[0],libdb[1].replace('\\n','\n')
    
    labellib['text']=libdata
    labeltime['text']=libdtitle    
    
    threading.Timer(second,lib,[second]).start()




def sawnotice():
    notice= 0
            
#FTP 업로드
def ftp_upload():
    ftpfood = ftplib.FTP("pydoctor.gq","u857776350", "python")
    ftpfood.cwd("/public_html/")
    file=io.open('account.json','rb')
    ftpfood.storbinary('STOR '+"account.json", file)
    file.close()
    ftpfood.close()


def login(e=''):
    global who
    who = var.get()
    if var.get() == 1:
        for i in range(0, len(student_list), 1):
            if ent1_ID.get() == student_list[i]["ID"] and ent2_password.get() == student_list[i]["PW"]:
                student.login(ent1_ID.get())
                stMenu()
                home()
                I1 = i

                break
    elif var.get() == 2:
        for i in range(0, len(pro_list), 1):
            if ent1_ID.get() == pro_list[i]["ID"] and ent2_password.get() == pro_list[i]["PW"]:
                prMenu()
                home()
                I2 = i
                break
    else:
        messagebox.showinfo("오류", "메뉴를 선택하시오")


def getLastDay(year, month):  # ㅍㅈ

    if month == 12:
        year = year + 1
        month = 1

    else:
        month = month + 1

    d = datetime.date(year, month, 1)
    t = datetime.timedelta(days=1)
    k = d - t

    return k.day


class student_db:
    def __init__(self):
        self.stuid = ''
        self.taking = ''
        try:
            with open('studentdb.json', encoding='utf-8') as studentdb:
                self.studentdb = json.load(studentdb)

        except:
            db = OrderedDict()
            stuinfo = OrderedDict()
            account = OrderedDict()

            classlist = []
            classlist.append("소프트웨어 코딩과 적용")
            classlist.append("회계와사회")
            stuinfo["taking"] = classlist
            account["1001"] = stuinfo
            db["id"] = account
            print(json.dumps(db, ensure_ascii=False, indent="\t"))
            with open('studentdb.json', 'w', encoding="utf-8") as make_file:
                json.dump(db, make_file, ensure_ascii=False, indent="\t")

            with open('studentdb.json', encoding='utf-8') as studentdb:
                self.studentdb = json.load(studentdb)

    def login(self, stuid):
        self.stuid = stuid
        self.taking = self.studentdb["id"][self.stuid]["taking"]  # 로그인한 계정의 수강내역 열기
        print("로그인 성공! 환영합니다.")
        print("아이디:", self.stuid)
        print("수강 과목: ", self.taking)

    def add_class(self):
        newclass = input("수업명을 입력해 주세요.")
        self.studentdb["id"][self.stuid]["taking"].append(newclass)  # 계정에 수업 추가
        self.savedb()

    def del_class(self):
        delclass = input("삭제할 수업명을 입력해 주세요.")
        self.studentdb["id"][self.stuid]["taking"].remove(delclass)  # 계정에 수업 삭제
        self.savedb()

    def savedb(self):
        with open('studentdb.json', 'w', encoding="utf-8") as make_file:
            json.dump(self.studentdb, make_file, ensure_ascii=False, indent="\t")  # DB에 저장


student = student_db()


class classday_db:
    def __init__(self, fd, class_name):
        # 수업 로딩
        self.dbdown()

        try:
            self.fname='account.json'
            if class_name == "소프트웨어 코딩과 적용" : self.fname= 'coding.json'
                
            with open(fname , encoding='utf-8') as clsdb:
                self.db = json.load(clsdb)
            
            self.class_name = class_name
            self.message = self.db["message"]
            self.firstday = self.db["first_class_day"]  # 첫달 강의 날짜
            fymd = self.firstday.split('-')
            self.fyear, self.fmonth, self.fday = int(fymd[0]), int(fymd[1]), int(fymd[2])  # 첫째날 연,월,일 변수에 저장
            
            self.f1month_class = self.db["all_class_day"][0]  # 첫달 강의 날짜
            self.f2month_class = self.db['all_class_day'][1]  # 둘째달 강의 날짜
            self.f3month_class = self.db['all_class_day'][2]  # 셋째달 강의 날짜
            self.f4month_class = self.db['all_class_day'][3]  # 넷째달 강의 날짜
            self.f5month_class = self.db['all_class_day'][4]  # 다섯째달 강의 날짜
            global last  ###수정
            last = []
            
            f1last = getLastDay(self.fyear, self.fmonth)  # 수업 첫 날이 있는 달의 마지막 일(day) 구하기
            f2last = getLastDay(self.fyear, self.fmonth + 1)
            f3last = getLastDay(self.fyear, self.fmonth + 2)
            f4last = getLastDay(self.fyear, self.fmonth + 3)
            
            last.append(f1last)
            last.append(f2last)
            last.append(f3last)
            last.append(f4last)
            
        except:

            # 수업 생성
            self.firstday = fd  # "2017-09-01"
            self.class_name = class_name
            self.message = "알림 메시지:"
            fymd = self.firstday.split('-')
            self.fyear, self.fmonth, self.fday = int(fymd[0]), int(fymd[1]), int(fymd[2])  # 첫째날 연,월,일 변수에 저장

            fmonthlist = []
            for i in range(0, 4):  # 몇주차까지 수업이 있는지
                if self.fmonth + i > 12:
                    fmonthlist.append(self.fmonth + i - 12)  # 내년 수업
                    continue

                fmonthlist.append(self.fmonth + i)

            last = []

            f1last = getLastDay(self.fyear, self.fmonth)  # 수업 첫 날이 있는 달의 마지막 일(day) 구하기
            f2last = getLastDay(self.fyear, self.fmonth + 1)
            f3last = getLastDay(self.fyear, self.fmonth + 2)
            f4last = getLastDay(self.fyear, self.fmonth + 3)

            last.append(f1last)
            last.append(f2last)
            last.append(f3last)
            last.append(f4last)

            semester_week = 16  # 총 몇 주를 강의 하는지

            self.f1month_class = []  # 8월 달 강의 날짜
            self.f2month_class = []  # 9월 달 강의 날짜
            self.f3month_class = []  # 10월 달 강의 날짜
            self.f4month_class = []  # 11월 달 강의 날짜
            self.f5month_class = []  # 12월 달 강의 날짜

            for i in range(semester_week):  # 총 차시만큼
                if self.fday + i * 7 - (f4last + f3last + f2last + f1last) > 0:  # 수업이 셋째 달의 마지막 일을 넘으면
                    self.f5month_class.append(self.fday + i * 7 - (f4last + f3last + f2last + f1last))  # 다섯째달에 추가

                elif self.fday + i * 7 - (f3last + f2last + f1last) > 0:  # 수업이 셋째 달의 마지막 일을 넘으면
                    self.f4month_class.append(self.fday + i * 7 - (f3last + f2last + f1last))  # 넷째달에 추가

                elif self.fday + i * 7 - (f2last + f1last) > 0:  # 수업이 둘째 달의 마지막 일을 넘으면
                    self.f3month_class.append(self.fday + i * 7 - (f2last + f1last))  # 셋째달에 추가

                elif self.fday + i * 7 - f1last > 0:  # 수업이 첫 달의 마지막 일을 넘으면
                    self.f2month_class.append(self.fday + i * 7 - f1last)  # 둘째달에 추가

                else:
                    self.f1month_class.append(self.fday + i * 7)  # 첫달 수업 날짜 추가
            if str(self.fmonth) == '9':
                self.f5month_class = self.f4month_class
                self.f4month_class = self.f3month_class
                self.f3month_class = self.f2month_class
                self.f2month_class = self.f1month_class
                self.f1month_class = []

        print("8월 ", self.f1month_class)
        print("9월 ", self.f2month_class)
        print("10월 ", self.f3month_class)
        print("11월 ", self.f4month_class)
        print("12월 ", self.f5month_class)

    def dbdown(self):
        myftp = ftplib.FTP("pydoctor.gq","u857776350", "python")
        myftp.cwd("/public_html/")
        filename="account.json"
        fd = open ("" + filename, 'wb')
        myftp.retrbinary ("RETR " + filename, fd.write)
        fd.close()
        myftp.close()
        

    # json 데이타베이스 저장
    def savedb(self):
        # json 생성
        self.data = OrderedDict()
        self.data["name"] = self.class_name
        self.data["first_class_day"] = self.firstday
        self.data["message"] = self.message
        allmonth = []
        allmonth.append(self.f1month_class)
        allmonth.append(self.f2month_class)
        allmonth.append(self.f3month_class)
        allmonth.append(self.f4month_class)
        allmonth.append(self.f5month_class)
        self.data["all_class_day"] = allmonth
        
        with open(self.fname, 'w', encoding="utf-8") as make_file:
            json.dump(self.data, make_file, ensure_ascii=False, indent="\t")

    def delclass(self, date):
        date = date.split('-')
        if date[0] == '08':
            if date[1][0] == '0': date[1] = date[1].replace('0', '')
            self.f1month_class.remove(int(date[1]))
        elif date[0] == '09':
            if date[1][0] == '0': date[1] = date[1].replace('0', '')
            self.f2month_class.remove(int(date[1]))
        elif date[0] == '10':
            if date[1][0] == '0': date[1] = date[1].replace('0', '')
            self.f3month_class.remove(int(date[1]))
        elif date[0] == '11':
            if date[1][0] == '0': date[1] = date[1].replace('0', '')
            self.f4month_class.remove(int(date[1]))
        elif date[0] == '12':
            if date[1][0] == '0': date[1] = date[1].replace('0', '')
            self.f5month_class.remove(int(date[1]))
        self.savedb()

    def addclass(self, date):
        date = date.split('-')
        if date[0] == '08':
            if date[1][0] == '0': date[1] = date[1].replace('0', '')
            self.f1month_class.append(int(date[1]))
        elif date[0] == '09':
            if date[1][0] == '0': date[1] = date[1].replace('0', '')
            self.f2month_class.append(int(date[1]))
        elif date[0] == '10':
            if date[1][0] == '0': date[1] = date[1].replace('0', '')
            self.f3month_class.append(int(date[1]))
        elif date[0] == '11':
            if date[1][0] == '0': date[1] = date[1].replace('0', '')
            self.f4month_class.append(int(date[1]))
        elif date[0] == '12':
            if date[1][0] == '0': date[1] = date[1].replace('0', '')
            self.f5month_class.append(int(date[1]))
        self.savedb()



clscoding = classday_db("2017-08-30", "소프트웨어 코딩과 적용")
clsaccount = classday_db("2017-09-04", "회계와 사회")


def init():
    # 아래 변수들이 전역변수임을 알리기 위함.
    global var, I1, I2, rb1, rb2
    global button1, button2, label1, label2, ent1_ID, ent2_password
    global scvar, scrb1, scrb2, scrb3, scbutton, sclabel, frame, schoolplan, schoolfood, schoollib
    global ent_month, labelmonth, ent_day, labelday, ent_month2, labelmonth2, ent_day2, labelday2, labeledit, labeledit2, buttonedit,labelfoodtitle, labelfood,labelplan,labelplantitle
    global libdata,labellibtitle,labellib,libtitle,labeltime,noticelabel , noticeframe
    global cau, img, canvas, tk_img
    cau = Image.open("cau1.png")
    tk_img = ImageTk.PhotoImage(cau)
    canvas = tk.Canvas(window)
    canvas.create_image(400, 530, image=tk_img)

    var = IntVar()
    I1 = IntVar()
    I2 = IntVar()

    rb1 = Radiobutton(canvas, text="학생용", variable=var, value=1)
    rb2 = Radiobutton(canvas, text="교수용", variable=var, value=2)
    label1 = Label(canvas, text="아이디")
    label2 = Label(canvas, text="비밀번호")
    ent1_ID = Entry(canvas, width=10, bg="skyblue")
    ent2_password = Entry(canvas, width=10, bg="yellowgreen")
    ent1_ID.bind("<Return>", login)
    ent2_password.bind("<Return>", login)

    button1 = Button(canvas, text="login", command=login)

    scvar = IntVar()
    scrb1 = Radiobutton(canvas, text="normal", variable=scvar, value=1)
    scrb2 = Radiobutton(canvas, text="전공", variable=scvar, value=2)
    scrb3 = Radiobutton(canvas, text="전기 제외 전공", variable=scvar, value=3)
    scbutton = Button(canvas, text="계산", command=scLabel)
    sclabel = Label(canvas, text="")

    ent_month = Entry(canvas, width=5, bg="plum")
    labelmonth = Label(canvas, text="월")
    ent_day = Entry(canvas, width=5, bg="plum")
    labelday = Label(canvas, text="일")
    ent_month2 = Entry(canvas, width=5, bg="powderblue")
    labelmonth2 = Label(canvas, text="월")
    ent_day2 = Entry(canvas, width=5, bg="powderblue")
    labelday2 = Label(canvas, text="일")
    labeledit = Label(canvas, text="휴강")
    labeledit2 = Label(canvas, text="보강")
    buttonedit = Button(canvas, text="확인", command=edit)

    #홈
    schoolplan = Frame(canvas,borderwidth=3, relief='groove',width=500) #학사일정
    with open('12plan.txt','r', encoding='utf-8') as txt:
        plan12= txt.read()
    labelplan= Label(schoolplan, text=plan12, wraplength=300, justify=LEFT,font=(10))
    labelplantitle= Label(schoolplan, text="학사일정",font=("고딕", 20,'bold'))
    schoolfood = Frame(canvas,borderwidth=3, relief='groove',width=500) #학사일정
    with open('food.txt','r', encoding='utf-8') as txt:
        food= txt.read()
    labelfoodtitle= Label(schoolfood, text="오늘의 식단",font=("고딕", 20,'bold'))
    labelfood= Label(schoolfood, text=food, wraplength=300, justify=LEFT,font=(10))

    schoollib = Frame(canvas,borderwidth=3, relief='groove',width=500) #도서관 좌석
    labellibtitle= Label(schoollib, text="도서관 좌석상황",font=("고딕", 20,'bold'))
    labellib= Label(schoollib, text='', wraplength=300, justify=LEFT,font=(10))
    labeltime=Label(schoollib, text= '',font=("고딕", 15,'bold'))
    lib()

    #알림메뉴
    noticeframe= Frame(canvas,borderwidth=3, relief='groove') #도서관 좌석
    noticelabel= Label(noticeframe, text=clsaccount.message)
    checkn(3)

    ##    img=image.filter(ImageFilter.BLUR)


##    cau=canvas(window,image=display, bg="powderblue")
def loginView():
    button1.grid(row=3, column=0, columnspan=2)
    rb1.grid(row=0, column=0)
    rb2.grid(row=0, column=1)
    label1.grid(row=1, column=0)
    label2.grid(row=2, column=0)
    ent1_ID.grid(row=1, column=1)
    ent2_password.grid(row=2, column=1)


# logout
def logout():
    clear()
    menubar.delete('목록')  # 여기 새로 추가!!!
    loginView()


# destroy
def clear():
    for label in canvas.grid_slaves():
        label.grid_forget()
    for label in canvas.place_slaves():
        if label != cau:
            label.place_forget()
    ent1_ID.delete(0, END)
    ent2_password.delete(0, END)


# menu

def stMenu():
    clear()
    menu = tk.Menu(menubar)  # 상위메뉴설정
    try:
        menubar.delete('목록')
    except:
        pass
    menubar.add_cascade(label="목록", menu=menu)
    # 하위메뉴추가
    menu.add_command(label="강의일정", command=cal)
    menu.add_command(label="알림", command=noticehome)
    menu.add_command(label="학점계산기", command=scorecal)
    menu.add_command(label="재수강시뮬레이션", command=simul)
    button2.place(x=805, y=0)


def prMenu():
    clear()
    menu = tk.Menu(menubar)  # 상위메뉴설정
    try:
        menubar.delete('목록')
    except:
        pass
    menubar.add_cascade(label="목록", menu=menu)
    # 하위메뉴추가
    menu.add_command(label="강의일정", command=cal)
    menu.add_command(label="일정수정", command=editsch)
    button2.place(x=805, y=0)


# destroy menu
def menuDestroy():
    menu.destroy()


global Month, mm, bc
bc = 0


def moveM(v):
    global Month, mm, bc
    bc += 1
    if v == 1:
        Month -= 1
        cal()

    elif v == 2:
        Month += 1
        cal()

    if Month - mm <= 0:
        bemonth.grid_forget()
    elif Month - mm >= 3:
        nemonth.grid_forget()
    else:
        bemonth.grid(row=0, column=2)
        nemonth.grid(row=0, column=4)


def cal():
    clear()
    button2.place(x=805, y=0)
    global Month, mm, bemonth, nemonth, bc, last
    lbList = []
    dayList = []
    dL = ["월", "화", "수", "목", "금", "토", "일"]
    global d
    d = []
    d1 = []
    d2 = []
    d3 = []
    d4 = []
    d.append(d1)
    d.append(d2)
    d.append(d3)
    d.append(d4)

    for i in range(0, 4, 1):
        n = 0
        for j in range(0, last[i], 1):
            n += 1
            d[i].append(str(n))

    td = time.localtime()

    tdYear = td.tm_year
    tdMonth = td.tm_mon
    tdDay = td.tm_mday
    tD = datetime.date(tdYear, tdMonth, tdDay)
    wD = tD.weekday()  # 월요일=0

    if bc == 0:
        Month = tdMonth

    startday = datetime.date(tdYear, Month, 1)  # ㅍㅈ

    stWD = startday.weekday()

    calnder = Frame(canvas)
    calnder.grid(row=0, column=0)

    YM = Label(calnder, text=str(tdYear) + " " + str(Month))

    if tdMonth < 9:
        mm = 3
    else:
        mm = 9

    for i in range(0, 7, 1):
        dayList.append(Label(calnder, text=dL[i], width=10))

    lecc = "white"  # 더미

    # 여기 english.f1month_class 가 첫 달 수업 날짜입니다.

    def calset():
        global who
        row_count = (last[Month - mm] + stWD) // 7
        if (last[Month - mm] + stWD) % 7 != 0:
            row_count += 1

        for i in range(0, row_count, 1):
            for j in range(0, 7, 1):
                if i == 0:
                    #print(d[Month - mm][i + j - stWD])
                    #print(clsaccount.f2month_class)
                    lecc = 'white'
                    if 1:
                        if 1: #논리 레벨을 맞추기 위해 if 1을 추가함
                            if Month==8 :
                                if int(d[Month - mm][i + j - stWD]) in clsaccount.f1month_class: lecc = 'lightcoral'  # 수업 있는 날 빨강
                                if int(d[Month - mm][i + j - stWD]) in clscoding.f1month_class: lecc = 'aquamarine'  # 수업 있는 날
                            elif Month==9 :
                                if int(d[Month - mm][i + j - stWD]) in clsaccount.f2month_class: lecc = 'lightcoral'  # 수업 있는 날 빨강
                                if int(d[Month - mm][i + j - stWD]) in clscoding.f2month_class: lecc = 'aquamarine'  # 수업 있는 날 
                            elif Month==10 :
                                if int(d[Month - mm][i + j - stWD]) in clsaccount.f3month_class: lecc = 'lightcoral'  # 수업 있는 날 빨강
                                if int(d[Month - mm][i + j - stWD]) in clscoding.f3month_class: lecc = 'aquamarine'  # 수업 있는 날 
                            elif Month==11 :
                                if int(d[Month - mm][i + j - stWD]) in clsaccount.f4month_class: lecc = 'lightcoral'  # 수업 있는 날 빨강
                                if int(d[Month - mm][i + j - stWD]) in clscoding.f4month_class: lecc = 'aquamarine'  # 수업 있는 날 
                            elif Month==12 :
                                if int(d[Month - mm][i + j - stWD]) in clsaccount.f5month_class: lecc = 'lightcoral'  # 수업 있는 날 빨강
                                if int(d[Month - mm][i + j - stWD]) in clscoding.f5month_class: lecc = 'aquamarine'  # 수업 있는 날 
                        
                        if who == 2 and lecc== 'aquamarine': lecc= 'white'

                    if i + j < stWD:
                        lbList.append(Label(calnder, text="", width=10, bg='white'))  # 달력의 빈 칸(처음)
                    elif i + j == stWD:
                        lbList.append(Label(calnder, text=d[Month - mm][i + j - stWD], width=10, bg=lecc))  # 이 달의 첫째 날
                    else:
                        lbList.append(
                            Label(calnder, text=d[Month - mm][i + j - stWD], width=10, bg=lecc))  # 둘째날~첫주 일요일
                elif i * 7 + j - stWD < last[Month - mm]:
                    #print(d[Month - mm][i * 7 + j - stWD])
                    #print(clsaccount.f2month_class)
                    lecc = 'white'
                    if 1:
                        if 1:
                            if Month==8:
                                if int(d[Month - mm][i * 7 + j - stWD]) in clsaccount.f1month_class : lecc = 'lightcoral'  # 수업 있는 날 빨강
                                if int(d[Month - mm][i * 7 + j - stWD]) in clscoding.f1month_class : lecc = 'aquamarine'  # 수업 있는 날 빨강
                            elif Month==9 :
                                if int(d[Month - mm][i * 7 + j - stWD]) in clsaccount.f2month_class : lecc = 'lightcoral'  # 수업 있는 날 빨강
                                if int(d[Month - mm][i * 7 + j - stWD]) in clscoding.f2month_class : lecc = 'aquamarine'  # 수업 있는 날 빨강

                            elif Month==10 :
                                if int(d[Month - mm][i * 7 + j - stWD]) in clsaccount.f3month_class : lecc = 'lightcoral'  # 수업 있는 날 빨강
                                if int(d[Month - mm][i * 7 + j - stWD]) in clscoding.f3month_class : lecc = 'aquamarine'  # 수업 있는 날 빨강
                                    
                            elif Month==11 :
                                if int(d[Month - mm][i * 7 + j - stWD]) in clsaccount.f4month_class : lecc = 'lightcoral'  # 수업 있는 날 빨강
                                if int(d[Month - mm][i * 7 + j - stWD]) in clscoding.f4month_class : lecc = 'aquamarine'  # 수업 있는 날 빨강

                            elif Month==12 :
                                if int(d[Month - mm][i * 7 + j - stWD]) in clsaccount.f5month_class : lecc = 'lightcoral'  # 수업 있는 날 빨강
                                if int(d[Month - mm][i * 7 + j - stWD]) in clscoding.f5month_class : lecc = 'aquamarine'  # 수업 있는 날 빨강

                        if who == 2 and lecc== 'aquamarine': lecc= 'white'
                    
                    lbList.append(Label(calnder, text=d[Month - mm][i * 7 + j - stWD], width=10, bg=lecc))  # 둘째주~마지막 날
                else:
                    lecc='white'
                    lbList.append(Label(calnder, text="", width=10, bg=lecc))  # 달력의 빈칸(끝)

    def calgrid():
        row_count = (last[Month - mm] + stWD) // 7
        if (last[Month - mm] + stWD) % 7 != 0:
            row_count += 1

        for i in range(0, row_count + 2, 1):
            for j in range(0, 7, 1):
                if i == 0:
                    if j == 0:
                        YM.grid(row=i, column=j + 3)
                elif i == 1:
                    dayList[j].grid(row=i, column=j)
                else:
                    lbList[(i - 2) * 7 + j].grid(row=i, column=j)

    calset()
    calgrid()

    bemonth = Button(calnder, text="<", command=lambda x=1: moveM(x))
    nemonth = Button(calnder, text=">", command=lambda x=2: moveM(x))

    bemonth.grid(row=0, column=2)
    nemonth.grid(row=0, column=4)

    classinfo = Frame(canvas)
    classinfo.grid(row=1, column=0, pady=50)

    if who == 1 :
        classlabel = Label(classinfo, text="수강 과목: ", width=10)
        classlabel.grid(row=0, column=0)
        classname1 = Label(classinfo, text="회계와 사회", bg='lightcoral')
        classname1.grid(row=0, column=1)
        classname2 = Label(classinfo, text="소프트웨어 코딩과 적용", bg='aquamarine')
        classname2.grid(row=0, column=2, padx=10)
    
    if who == 2 :
        classlabel = Label(classinfo, text="담당 과목: ", width=10)
        classlabel.grid(row=0, column=0)
        classname1 = Label(classinfo, text="회계와 사회", bg='lightcoral')
        classname1.grid(row=0, column=1)



# 수업 요일 DB 객체



# score simulation

# normal
def simulnor(I1):
    sc = 0.0
    tot = 0.0
    lenstscL = len(scoreList[I1])
    for i in range(0, lenstscL, 1):
        sc += scoreList[I1][i]["성적"] * scoreList[I1][i]["학점"]
        tot += scoreList[I1][i]["학점"]
    sc /= tot
    return (sc)


# 전공
def simulsub1(I1):
    sc = 0.0
    tot = 0.0
    lenstscL = len(scoreList[I1])
    for i in range(0, lenstscL, 1):
        if (scoreList[I1][i]["구분"] != "교양"):
            sc += scoreList[I1][i]["성적"] * scoreList[I1][i]["학점"]
            tot += scoreList[I1][i]["학점"]
    sc /= tot
    return (sc)


# 전기 제외 전공
def simulsub2(I1):
    sc = 0.0
    tot = 0.0
    lenstscL = len(scoreList[I1])
    for i in range(0, lenstscL, 1):
        if (scoreList[I1][i]["구분"] == "전공"):
            sc += scoreList[I1][i]["성적"] * scoreList[I1][i]["학점"]
            tot += scoreList[I1][i]["학점"]
    sc /= tot
    return (sc)


# 계산버튼 함수
def scLabel():
    if scvar.get() == 1:
        sclabel.configure(text=str(simulnor(I1)))
    elif scvar.get() == 2:
        sclabel.configure(text=str(simulsub1(I1)))
    elif scvar.get() == 3:
        sclabel.configure(text=str(simulsub2(I1)))


def scorecal():
    clear()
    scrb1.place(x=250, y=250)
    scrb2.place(x=250, y=280)
    scrb3.place(x=250, y=310)
    scbutton.place(x=250, y=340)
    sclabel.place(x=450, y=285)
    button2.place(x=805, y=0)


# 재수강 시뮬레이션
def simul():
    clear()
    button2.place(x=805, y=0)

def strlist(lst):
    txt=''
    for i in lst:
        txt=txt+', '+str(i)
    return txt[2:]

# 일정수정
def editsch():
    clear()
    button2.place(x=805, y=0)
    ent_month.place(x=300, y=250)
    labelmonth.place(x=350, y=250)
    ent_day.place(x=400, y=250)
    labelday.place(x=450, y=250)
    ent_month2.place(x=300, y=280)
    labelmonth2.place(x=350, y=280)
    ent_day2.place(x=400, y=280)
    labelday2.place(x=450, y=280)
    labeledit.place(x=480, y=250)
    labeledit2.place(x=480, y=280)
    buttonedit.place(x=370, y=310)
    huokay=Label(canvas,text='',relief='sunken',width=25)
    huokay.place(x=280,y=130)
    hutxt="휴강 가능 일정\n"+"9월: "+strlist(clsaccount.f2month_class)+ "\n10월: "+strlist(clsaccount.f3month_class)+"\n11월: "+strlist(clsaccount.f4month_class)+"\n12월: "+strlist(clsaccount.f5month_class)
    huokay['text']=hutxt
    


# 일정수정버튼
def edit():
    lullu = ent_month.get()+'-'+ent_day.get()
    bogang =ent_month2.get()+'-'+ent_day2.get()
    clsaccount.delclass(lullu) #휴강
    clsaccount.addclass(bogang) #보강
    clsname= clsaccount.class_name
    clsaccount.message = clsaccount.message+ "\n{0} 과목 {1}일 휴강, {2}일 보강처리 되었습니다.".format(clsname,lullu,bogang)
    messagebox.showinfo("성공", "[{0}] {1}일 휴강, {2}일 보강처리 완료 \n 모든 수강생에게 알림이 전송되었습니다.".format(clsname,lullu,bogang))
    clsaccount.savedb()
    ftp_upload()
    
def home():
    clear()
    schoolplan.grid(row=0,column=0)
    labelplantitle.grid(row=0,column=0)
    labelplan.grid(row=1,column=0)

    schoolfood.grid(row=0,column=1,padx=40)
    labelfoodtitle.grid(row=0,column=0)    
    labelfood.grid(row=1,column=0)    

    schoollib.grid(row=1,column=0,padx=40)
    labellibtitle.grid(row=0,column=0)
    labeltime.grid(row=1,column=0)
    labellib.grid(row=2,column=0)

def noticehome():
    clear()
    noticeframe.grid(row=0,column=0)
    noticelabel.grid(row=0,column=0)
    

window = tk.Tk()

init()
loginView()
w = 850
h = 650
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.anchor(CENTER)
canvas.anchor(CENTER)
button2 = Button(canvas, text="logout", command=logout)
menubar = tk.Menu(window)
window.config(menu=menubar)
filemenu = tk.Menu(menubar, tearoff=0)  # PIL깔아야 실행
menu = tk.Menu(menubar)  # 상위메뉴설정
# for score simulation
canvas.place(x=0, y=0, relwidth=1, relheight=1)
scoreList = []
st1score = []
score1_1 = {"과목": "가", "학점": 3, "성적": 4.5, "구분": "전기"}
score1_2 = {"과목": "나", "학점": 2, "성적": 4.0, "구분": "교양"}
score1_3 = {"과목": "다", "학점": 3, "성적": 2.0, "구분": "전기"}
score1_4 = {"과목": "라", "학점": 4, "성적": 2.0, "구분": "전공"}
score1_5 = {"과목": "마", "학점": 2, "성적": 3.0, "구분": "전공"}
score1_6 = {"과목": "바", "학점": 4, "성적": 4.0, "구분": "전공"}
st1score.append(score1_1)
st1score.append(score1_2)
st1score.append(score1_3)
st1score.append(score1_4)
st1score.append(score1_5)
st1score.append(score1_6)
# for i in range(0,len(student_list),1):
scoreList.append(st1score)  # 1명기준 편집필요
I1 = 0  # 더미

# users
student_list = []
pro_list = []
student1 = {"ID": "20141457", "PW": "1000"}
student2 = {"ID": "1001", "PW": "1001"}
pro1 = {"ID": "1001", "PW": "1001"}
student_list.append(student1)
student_list.append(student2)
pro_list.append(pro1)



window.mainloop()

