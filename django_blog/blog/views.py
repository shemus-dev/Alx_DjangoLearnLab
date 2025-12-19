from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserUpdateForm

def register(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        #Load raw data into the form (still untrusted)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        
        else:
            form = RegisterForm()
        return render(request, 'blog/register.html', {'form': form})
    
@login_required
def profile(request):
    if request.method == 'POST':
        #instance=request.use =Update THIS user, not create a new one
        #request.POST=raw data from user
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})