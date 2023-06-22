from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import AudioFiles, ProtectedFiles
import re


# for checking email validity using regex
def valid_email_check(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


def index(request):
    if request.method == 'POST':
        user = request.user.id
        file_name = request.POST['file_name']
        file_image = request.FILES.get('file_image')
        files = request.FILES['file']
        visibility = request.POST['visibility']
        # file saving code for public and private files
        file = AudioFiles.objects.create(user_id=user, file_name=file_name, file_image=file_image, files=files,
                                         visibility=visibility)
        file.save()
        # file saving code for protected files
        if visibility == 'protected':
            email_list = request.POST.get('p_email').split(',')
            email_list.append(request.user.email)
            if email_list:  # checks if email is provided
                for email in email_list:
                    if valid_email_check(email):  # checking email validity
                        if email in User.objects.values_list('email', flat=True):
                            p_email = ProtectedFiles.objects.create(file_id=file.id, email=email.strip())
                            p_email.save()
                        else:
                            messages.warning(request, 'list contains emails that are not registered with portal')
                    else:
                        messages.warning(request, 'Invalid Email found')
            else:
                messages.warning(request, 'Email is required for protected file')
        
        return redirect('Home:index')
    
    return render(request, 'index.html')


# code for public files

def public_audio_files(request):
    public_files = AudioFiles.objects.all().filter(visibility='public')
    return render(request, 'index.html', {'public_files': public_files})


# code for private files

def private_audio_files(request):
    private_files = AudioFiles.objects.all().filter(visibility='private', user_id=request.user.id)
    return render(request, 'index.html', {'private_files': private_files})


# code for protected files

def protected_audio_files(request):
    email = ProtectedFiles.objects.filter(email=request.user.email).values_list('email', flat=True)
    protected_files = AudioFiles.objects.filter(visibility='protected', protectedfiles__email__in=email)
    if protected_files is None:
        messages.info(request, 'Protected files are empty!!')
    return render(request, 'index.html', {'protected_files': protected_files})


# code for playing and downloading files

def download_file(request, file_id):
    audio_file = AudioFiles.objects.get(id=file_id)  # fetching file from database
    file_path = audio_file.files.path  # fetching file path
    print('file_path:', file_path)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='audio/mp3')  # reading and storing file in response variable
        return response


def delete_file(request, file_id, user_id=None):
    if 'protected' in request.path:
        protected_file = ProtectedFiles.objects.all().filter(file_id=file_id, email=request.user.email).first()
        if protected_file:
            file_name = protected_file.file.file_name
            messages.success(request, f"File '{file_name}' has been deleted.")
            protected_file.delete()
    
    else:
        if user_id:
            audio_file = AudioFiles.objects.filter(id=file_id, user_id=user_id).first()
            if audio_file:
                file_name = audio_file.file_name
                audio_file.delete()
                messages.success(request, f"File '{file_name}' has been deleted.")
            else:
                messages.error(request, "Public files can only be deleted by its owner")
        else:
            audio_file = AudioFiles.objects.get(id=file_id)  # fetching file from database
            messages.success(request, f"File '{audio_file.file_name}' has been deleted.")
            audio_file.delete()
    return redirect('Home:index')
