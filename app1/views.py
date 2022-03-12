from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection


# Create your views here.
def xyz(request):
    return render(request, "index.html")


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
        # to insert the data into database
        query = "insert into users1 (email,password) values (%s,%s)"
        value = (email, password)
        cursor.execute(query, value)
        print(cursor.rowcount)

    #to fetch the data from database
    #query = "select * from city where name='"+email+"'"
    #cursor.execute(query)
    #row = cursor.fetchone()
    #print(row)
        data = {"email": email, "password": password}
        return render(request, "first.html", data)

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





