from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import WaterintakeForm
from .forms import CustomUserCreationForm
from .models import intakeEntry
from datetime import date
from datetime import datetime
from django.core.paginator import Paginator 
from django.http import JsonResponse

def healthyfy(request):
    return render(request, 'home.html')

def signup_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    
    return render(request, 'logout.html', {'user': request.user})

@login_required
def add_intake(request):
    today = date.today()
    existing_entry = intakeEntry.objects.filter(user=request.user, date=today).first()
    if request.method == 'POST':
        form = WaterintakeForm(request.POST)
        if form.is_valid():
            if existing_entry:
                return render(request, 'add_intake.html',{
                    'form':form,
                    'error': 'You have already added your entry for today.'
                })
            intake_entry = form.save(commit=False)
            intake_entry.user = request.user
            intake_entry.date = today
            intake_entry.save()
            return render(request, 'success.html', {'success': 'Your entry was added successfully'})
    else:
        form = WaterintakeForm()
    return render(request, 'add_intake.html', {'form': form, 'error': existing_entry and 'You have already added your entry for today.'})


@login_required
def intake_history(request):
    water = intakeEntry.objects.filter(user=request.user)  # Ensure this matches the model name
    return render(request, 'retrieve.html', {'water': water})


@login_required
def intake_list(request):
    intake_entries = intakeEntry.objects.filter(user=request.user)
    paginator = Paginator(intake_entries, 1)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})

@login_required

def find_difference(request):
     if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        print(f"Start Date: {start_date}")  
        print(f"End Date: {end_date}")     

        try:
            start_intake = intakeEntry.objects.get(user=request.user, date=start_date)
            end_intake = intakeEntry.objects.get(user=request.user, date=end_date)

            water_intake = start_intake.intake - end_intake.intake
            return JsonResponse({'water_intake': water_intake})
        except intakeEntry.DoesNotExist:
            return JsonResponse({'error': 'Water intake data not available for the selected dates'}, status=400)

        
     return render(request, 'find_difference.html')


    
@login_required
def update(request, id):
    intake = get_object_or_404(intakeEntry, pk=id)
    
    if request.method == 'POST':
        form = WaterintakeForm(request.POST, instance=intake)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = WaterintakeForm(instance=intake)
    return render(request, 'update.html', {'form': form})


@login_required
def delete(request, id):
    intake = get_object_or_404(intakeEntry, pk=id)
    if request.method == 'POST':
       intake.delete()
       return redirect('home')
    return render(request, 'delete.html', {'intake':intake})

