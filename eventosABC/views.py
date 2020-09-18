'''This is a docstring'''
import json
import requests
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

user_token = None

# Create your views here.
def home(request):
    '''This is a docstring'''
    return render(request, 'home.html')

def check_token():
    global user_token
    token = user_token
    logedin = False
    if token:
        logedin = True
    return logedin

@csrf_exempt
def create_user(request):
    '''This is a docstring'''
    logedin = check_token()
    if request.method == 'POST':
        data = {}
        data['username'] = request.POST['username']
        data['first_name'] = request.POST['first_name']
        data['last_name'] = request.POST['last_name']
        data['email'] = request.POST['email']
        data['password'] = request.POST['password']
        requests.post('http://10.158.0.2:8080/api/create-user/', json=data)

    return render(request, 'registration/create-user.html', {'logedin': logedin})

@csrf_exempt
def api_auth(request):
    '''This is a docstring'''
    logedin = check_token()
    if request.method == 'POST':
        data = {}
        data['username'] = request.POST['username']
        data['password'] = request.POST['password']
        response = requests.post('http://10.158.0.2:8080/api/api-auth/', json=data)
        answer = response.json()
        global user_token
        user_token = answer['token']
        return redirect('/')
    return render(request, 'registration/api-auth.html', {'logedin': logedin})

def logout(request):
    global user_token
    user_token = None

    return redirect('/')

def get_events(request):
    '''This is a docstring'''
    logedin = check_token()
    global user_token
    token = user_token
    if request.method == 'GET' and token is not None:
        response = requests.get('http://10.158.0.2:8080/api/events/',
                                headers={'Content-Type':'application/json',
                                         'Authorization': 'Token {}'.format(token)})
        data = response.json()
        return render(request, 'home.html', {'data': data, 'context': logedin})
    return render(request, 'home.html')

# def get_base64_encoded_image(image_path):
#     with open(image_path, "rb") as img_file:
#         return pybase64.b64encode(img_file.read()).decode('utf-8')

def create_event(request):
    '''This is a docstring'''
    global user_token
    token = user_token
    logedin = check_token()
    if request.method == 'POST':
        data = {}
        data['event_name'] = request.POST['event_name']
        data['event_category'] = request.POST['event_category']
        data['event_place'] = request.POST['event_place']
        data['event_address'] = request.POST['event_address']
        data['event_initial_date'] = request.POST['event_initial_date']
        data['event_final_date'] = request.POST['event_final_date']
        data['event_type'] = request.POST['event_type']
        response = requests.post('http://10.158.0.2:8080/api/events/', json=data,
                                 headers={'Content-Type':'application/json',
                                          'Authorization': 'Token {}'.format(token)})
        return redirect('/')

    return render(request, 'create-event.html', {'context': logedin})

def event_detail(request, event_id):
    global user_token
    token = user_token
    if request.method == 'GET':
        response = requests.get('http://10.158.0.2:8080/api/events/'+str(event_id),
                                headers={'Content-Type':'application/json',
                                         'Authorization': 'Token {}'.format(token)})
        data = response.json()

    if request.method == 'POST':
        reponse = requests.delete('http://10.158.0.2:8080/api/events/'+str(event_id),
                                  headers={'Content-Type':'application/json',
                                           'Authorization': 'Token {}'.format(token)})
        return redirect('/')
    return render(request, 'event-detail.html', {'data': data})

def event_update(request, event_id):
    '''This is a docstring'''
    global user_token
    token = user_token
    if request.method == 'GET':
        response = requests.get('http://10.158.0.2:8080/api/events/'+str(event_id),
                                headers={'Content-Type':'application/json',
                                         'Authorization': 'Token {}'.format(token)})
        data = response.json()

    if request.method == 'POST':
        data = {}
        data['event_name'] = request.POST['event_name']
        data['event_category'] = request.POST['event_category']
        data['event_place'] = request.POST['event_place']
        data['event_address'] = request.POST['event_address']
        data['event_initial_date'] = request.POST['event_initial_date']
        data['event_final_date'] = request.POST['event_final_date']
        data['event_type'] = request.POST['event_type']
        response = requests.put('http://10.158.0.2:8080/api/events/'+str(event_id)+'/',
                                json=data, headers={'Content-Type':'application/json',
                                                    'Authorization': 'Token {}'.format(token)})
        return redirect('/')

    return render(request, 'update-event.html', {'data': data})
