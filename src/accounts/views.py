import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from accounts.forms import UserLoginForm, UserRegistrationForm, UserPreferencesForm, ContactForm
from test_check.models import Errors

User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Пользователь зарегистрирован')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def preference_view(request):
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserPreferencesForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.mailing = data['mailing']
                user.save()
                return redirect('accounts:preference')
        form = UserPreferencesForm(
            initial={'city': user.city, 'language': user.language,
                     'mailing': user.mailing})
        return render(request, 'accounts/preference.html',
                      {'form': form, 'contact_form': contact_form})
    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удален')
    return redirect('home')


def contact_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            language = data.get('language')
            email = data.get('email')
            qs = Errors.objects.filter(timestamp=datetime.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'language': language, 'email': email})
                err.data['user_data'] = data
                err.save()
            else:
                data = [{'city': city, 'language': language, 'email': email}]
                Errors(data=f"user_data: {data}").save()
            messages.success(request, 'Спасибо! Данный отправлены.')
            return redirect('accounts:preference')
        else:
            return redirect('accounts:preference')
    else:
        return redirect('accounts:login')
