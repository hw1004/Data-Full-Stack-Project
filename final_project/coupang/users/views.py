from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout


@require_http_methods(['GET', 'POST'])
def signup(request):
    # 요청 보낸 사용자가 인증되었다(로그인했다)면 => 바로 돌려보내기
    if request.user.is_authenticated:
        return redirect('recommendation:mainpage')
    
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('recommendation:mainpage')
    else:
        form = UserCreationForm()

    return render(request, 'users/signup.html', {
        'form': form,
    })


@require_http_methods(['GET', 'POST'])
def login(request):
    # 요청 보낸 사용자가 인증되었다(로그인했다)면 => 바로 돌려보내기
    if request.user.is_authenticated:
        return redirect('recommendation:mainpage')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # 쿠키(팔찌) 세팅
            auth_login(request, user)
            return redirect('recommendation:mainpage')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {
        'form': form,
    })


def logout(request):
    auth_logout(request)
    return redirect('recommendation:mainpage')