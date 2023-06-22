from django.contrib import messages, auth
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
import requests
from .models import ProfileVerify
import uuid
from django.conf import settings
from django.core.mail import send_mail


# email verification

def verify_email(email):
    api_key = 'live_edb42e2cafbf02a566fa5b486039cd6cedf850ce16ab4b8232331cbb0942979f'
    url = f'https://api.kickbox.com/v2/verify?email={email}'
    
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    result = data.get('result')
    
    if result == 'deliverable':
        return True
    else:
        return False


def login(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            profile_verify = ProfileVerify.objects.get(user=user)
            if profile_verify.is_verified:
                auth.login(request, user)
                return redirect('Home:index')
            else:
                messages.error(request, 'Please Verify your mail id')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('authentication:login')
    return render(request, 'login.html', {messages: 'messages'})


def register(request):
    if request.method == 'POST':
        first_name = request.POST['username']
        email = request.POST['email']
        Password = request.POST['password']
        ConfirmPassword = request.POST['password1']
        is_valid_email = verify_email(email)
        if is_valid_email:
            try:  # code for password validation using django validators
                password_validation.validate_password(Password, User)
            except password_validation.ValidationError as error:
                messages.error(request, error.messages[0])
                return redirect('authentication:register')
            if Password == ConfirmPassword:
                if User.objects.filter(first_name=first_name).exists():
                    messages.error(request, 'user already exists')
                    return redirect('authentication:register')
                elif User.objects.filter(username=email).exists():
                    messages.error(request, 'email already exists')
                    return redirect('authentication:register')
                else:
                    user = User.objects.create_user(first_name=first_name, username=email, email=email,
                                                    password=Password)
                    user.save()
                    # for saving details in profile verify for tokens
                    auth_token = str(uuid.uuid4())
                    profile_verify = ProfileVerify.objects.create(user=user, auth_tokens=auth_token)
                    profile_verify.save()
                    send_mail_after_registration(email, auth_token)
                    return redirect('authentication:success')
            else:
                messages.error(request,'Password doesnt match')
        else:
            messages.warning(request, 'Invalid mail address, Please provide actual one.')
    return render(request, 'register.html', {messages: 'messages'})


# function for sending verification mail
def send_mail_after_registration(email, token):
    subject = 'Your account need to be verified'
    message = f'Hi,paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


# for verifying the request
def verify(request, auth_token):
    try:
        verify_obj = ProfileVerify.objects.filter(auth_tokens=auth_token).first()
        if verify_obj.is_verified:
            messages.info(request, 'Your account already verified')
            return redirect('authentication:login')
        elif verify_obj:
            verify_obj.is_verified = True
            verify_obj.save()
            messages.info(request, 'Your account has been verified')
            return redirect('authentication:login')
        else:
            return redirect('authentication:error')
    except Exception as e:
        print(e)
        return redirect('/')


def error(request):
    return render(request, 'error.html')


def success(request):
    return render(request, 'success.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
