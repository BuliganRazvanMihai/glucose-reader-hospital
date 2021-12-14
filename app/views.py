from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
from app.models import Device
import json
import os
import csv
from datetime import datetime
import pandas as pd


def index(request):
    if request.user.is_anonymous:
        return redirect("/login.html")
    return html(request, "index")

#2021/08/30 01:48
def format_date(date):
    myDate = datetime.strptime(date, '%Y/%m/%d %H:%M').strftime('%Y-%m-%d %H:%M:%S')
    return myDate

def import_csv(request):
    context = {}
    # data from the txt files
    if request.method == 'POST':
        my_file = request.FILES['document']
        txtData = my_file.read()
        text_file = open("data.txt","wb")
        text_file.write(txtData)
        text_file.close()
        df = pd.read_csv("data.txt", delimiter="\t+|\t\t+|’", header=1)
        df.rename(columns={'Type d': 'Type', 'enregistrement': 'GlucoseHistorique'},
              inplace=True)
        df.drop('Taux de glucose scanné (mg/dL)', inplace=True, axis=1)
        df.drop('Insuline à action rapide (sans valeur numérique)', inplace=True, axis=1)
        df.drop('Insuline à action rapide (unités)', inplace=True, axis=1)
        df.drop('Historique du taux de glucose (mg/dL)', inplace=True, axis=1)
        df.drop('Insuline modifiée par l', inplace=True, axis=1)
        df.drop('utilisateur (unités)', inplace=True, axis=1)
        df.drop('Nourriture (sans valeur numérique)', inplace=True, axis=1)
        df.drop('Glucides (grammes)', inplace=True, axis=1)
        df.drop('Insuline à action lente (sans valeur numérique)', inplace=True, axis=1)
        df.drop('Insuline à action lente (unités)', inplace=True, axis=1)
        df.drop('Commentaires', inplace=True, axis=1)
        df.drop('Glycémie avec électrode de dosage (mg/dL)', inplace=True, axis=1)
        df.drop('Cétonémie (mmol/L)', inplace=True, axis=1)
        df.drop('Insuline repas (unités)', inplace=True, axis=1)
        df.drop('Insuline de correction (unités)', inplace=True, axis=1)
        df.drop('Heure précédente', inplace=True, axis=1)
        df.drop('Heure mise à jour', inplace=True, axis=1)
        csvfile = df.to_csv('log.csv', index=None)
    # Parsing the data
        final_file = open('log.csv','r')
        reader = csv.reader(final_file)
        header = []
        header = next(reader)
        rows = []
        for row in reader:
            print(row)
            deviceDate = format_date(row[1])
            Device.objects.create(patientId=1, deviceId=row[0], hour=deviceDate, type=row[2], glucoseValue=row[3])

    #creating the context
        context = {
               "file_content": json.dumps(txtData.decode("utf-8"))  # moving the data to frontend
               }
    return render(request, "index.html", context=context)

def html(request, filename):

    #Data for the graph
    labels = ["Jan", "Jan", "Jan", "Jan","Jan", "Jan", "Jan", "Jan"]
    data = [100, 200, 210, 321, 122, 232, 133, 123, 543, 213]

    context = {"filename": filename,
               "collapse": "",
               "labels": json.dumps(labels),
               "data": json.dumps(data),
               }
    if request.user.is_anonymous and filename != "login":
        return redirect("/login.html")
    if filename == "logout":
        logout(request)
        return redirect("/")
    if filename == "login" and request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            if "@" in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                context["error"] = "Wrong password"
        except ObjectDoesNotExist:
            context["error"] = "User not found"

        print("login")
        print(username, password)
    print(filename, request.method)
    if filename in ["buttons", "cards"]:
        context["collapse"] = "components"
    if filename in ["utilities-color", "utilities-border", "utilities-animation", "utilities-other"]:
        context["collapse"] = "utilities"
    if filename in ["404", "blank"]:
        context["collapse"] = "pages"

    return render(request, f"{filename}.html", context=context)
