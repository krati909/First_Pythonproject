from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection


# Create your views here.
def xyz(request):
    return render(request, "index.html")


def signup(request):
    email = request.GET['email']
    password = request.GET['psw']
    cursor = connection.cursor()
    # to insert the data into database
    query= "insert into users(email,password) values (%s,%s)"
    value= (email, password)
    cursor.execute(query, value)
    print(cursor.rowcount)

    #to fetch the data from database
    #query = "select * from city where name='"+email+"'"
    #cursor.execute(query)
    #row = cursor.fetchone()
    #print(row)
    data = {"email": email, "password": password}
    return render(request, "first.html", data)
