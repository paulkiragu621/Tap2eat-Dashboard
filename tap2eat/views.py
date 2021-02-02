from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import requests

access_token = ""

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        data = {
            'username': username,
            'password': password
        }
        #get access tocken
        response1 = requests.post(
            'http://127.0.0.1:8000/api-token-auth/',
            data=data
        )
        #access_tocken
        token = response1.json()
        global access_token
        access_token = token['token']

        print(access_token)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            form = AuthenticationForm(request.POST)
            return redirect(request, 'signin.html', {'form': form}) 
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('/home')        

@login_required
def home(request):
    headers = {'Authorization': f'Token {access_token}'}
    response2 = requests.get('http://127.0.0.1:8000/hello', headers=headers)
    print("Token: " +access_token)
    print(response2.status_code)
    if response2.status_code >= 200 and response2.status_code < 300:
        todos = response2.json()
        return render(request, "home.html", {"data": todos})
    else:
        return render(request, "home2.html")     
    #todos = response2.json()
    #return render(request, "home.html", {"data": todos})

def test(request):
    return render(request, "home2.html")    