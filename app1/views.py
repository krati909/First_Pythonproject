import random
import string
from random import randint


from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.core.mail import send_mail


# Create your views here.
def xyz(request):
    return render(request, "home.html")


def signup(request):
    email = request.POST['email']
    password = request.POST['psw']
    cursor = connection.cursor()
    query1 = "select * from users1 where email='"+email+"'"
    cursor.execute(query1)
    data = cursor.fetchall()
    if len(data)>0:
        data = {"email": "already signed up", "password":""}
        return render(request, "first.html", data)
    else:
        otp=randint(1000,9999)
        strotp=str(otp)
        # to insert the data into database
        query = "insert into users1 (email,password,otp) values (%s,%s,%s)"
        value = (email, password,strotp)
        cursor.execute(query, value)
        print(cursor.rowcount)
        #sending a mail
        body="Your opt for our portal signup with mail " +email+ "is" +strotp+"."
        send_mail('OTP for verification',body,"nightullu220@gmail.com",[email])

    #to fetch the data from database
    #query = "select * from city where name='"+email+"'"
    #cursor.execute(query)
    #row = cursor.fetchone()
    #print(row)
        data = {"email": email}
        return render(request, "singupsucess.html", data)

def signin(request):
    return render(request, "login.html")
def login(request):
    email = request.POST['email']
    password = request.POST['psw']
    cursor = connection.cursor()
    query1 = "select * from users1 where email='"+email+"'"
    cursor.execute(query1)
    data = cursor.fetchone()
    if data == None:
        data = {"email": "Not signed up", "password": ""}
        return render(request, "first.html", data)
    else:
        if data[2]==0:
            data = {"email": " you are Not verified user", "password": ""}
            return render(request, "first.html", data)
        if data[1]==password:
            data = {"email": "  Login sucessful", "password": ""}
            return render(request, "first.html", data)
        else:
            data = {"email": "password incorrect", "password": ""}
            return render(request, "first.html", data)

def otpverification(request):
    email = request.POST['email']
    otp = request.POST['otp']
    cursor = connection.cursor()
    query1 = "select * from users1 where email='" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()
    if data is not None:
        if data[2]==otp:
            query2 = "update users1 set is_verified=1 where email='" + email + "'"
            cursor.execute(query2)
            if cursor.rowcount==1:
                print("otp verified successfully")
            data = {"email": "  Login sucessful"}
            return render(request, "first.html", data)
        else:
            data = {"email": " wrong otp"}
            return render(request, "first.html", data)


def generateshorturl():
    letter=string.ascii_letters + string.digits
    shorturl=''
    for i in range(6):
        shorturl=shorturl+''.join(random.choice(letter))
    return shorturl


def urlshortner(request):
    longlink= request.GET['link']
    customurl = request.GET['customurl']
    if customurl is None or customurl=="":
        shorturl=''
    else:
        cursor = connection.cursor()
        query1 = "select * from links where short_link='" + customurl + "'"
        cursor.execute(query1)
        data = cursor.fetchone()
        if data is not None:
            data = {"email": " Already custom Url exist please try some other url"}
            return render(request, "first.html", data)
        else:
            query = "insert into links (long_link, short_link) values (%s,%s)"
            value = (longlink,customurl)
            cursor.execute(query, value)
            data = {"email": " Url shortened with nano.co/"+customurl}
            return render(request, "first.html", data)
    if shorturl is not None or shorturl !='':
      while True:
        shorturl = generateshorturl()
        cursor = connection.cursor()
        query2= "select * from links where short_link='" + shorturl + "'"
        cursor.execute(query2)
        data = cursor.fetchone()
        if data is not None:
            break
        else:
            query = "insert into links (long_link, short_link) values (%s,%s)"
            value = (longlink,shorturl)
            cursor.execute(query, value)
            data = {"email": " Url shortened with nano.co/"+shorturl}
            return render(request, "first.html", data)
