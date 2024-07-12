import rsa
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from galleryapp.forms import CustomUserCreationForm, AlbumForm
from galleryapp.models import CustomUser, Album

# Load the public key
with open('galleryapp/public_key.pem', 'rb') as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

# Load the private key
with open('galleryapp/private_key.pem', 'rb') as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())


def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # cleaned data
            email = form.cleaned_data.get('email')
            mobile_number = form.cleaned_data.get('mobile_number')
            password = form.cleaned_data.get('password1')

            # encrypting data
            encrypted_email = rsa.encrypt(email.encode(), public_key)
            encrypted_mobile = rsa.encrypt(mobile_number.encode(), public_key)
            encrypted_password = rsa.encrypt(password.encode(), public_key)

            form.instance.encrypted_email = encrypted_email.hex()
            form.instance.encrypted_mobile = encrypted_mobile.hex()
            form.instance.encrypted_password = encrypted_password.hex()
            form.save()
            messages.success(request, 'Your account has been created!')

    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            print('your email is', email)

            stored_user = CustomUser.objects.get(email=email)

            encrypted_email_bytes = bytes.fromhex(stored_user.encrypted_email)
            encrypted_password_bytes = bytes.fromhex(stored_user.encrypted_password)

            # decrypting data
            email = rsa.decrypt(encrypted_email_bytes, private_key).decode()

            password = rsa.decrypt(encrypted_password_bytes, private_key).decode()

            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dashboard/')

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def upload_album(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AlbumForm(request.POST, request.FILES)
            if form.is_valid():
                album = form.save(commit=False)
                album.user = request.user
                album.save()
                return redirect('/')

        else:
            form = AlbumForm()
        return render(request, 'upload.html', {'form': form})

    else:
        return redirect('/login/')


def home_page(request):
    all_photos = Album.objects.all()
    return render(request, 'home.html', {'all_photos': all_photos})


def detail_page(request, pk):
    album = Album.objects.get(pk=pk)
    return render(request, 'detail.html', {'album': album})


def del_album(request, pk):
    album = Album.objects.get(pk=pk)
    album.delete()
    return redirect('/dashboard/')


def profile_page(request):
    user = request.user
    album = Album.objects.filter(user=user)

    return render(request, 'dashboard.html', {'album': album})


def logout_page(request):
    logout(request)
    return redirect('/')
