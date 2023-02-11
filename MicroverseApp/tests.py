from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import login, authenticate  # add to imports
from . import forms
from .models import CustomUser, BankAccount, Card, Transaction, Reference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm

def login_func(request):
    form = forms.LoginForm(request.POST)
    message = ''
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['national_ID'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'Hello {user.first_name}! You have been logged in')
                if user.is_staff == True:
                    return redirect("/ad_dash")
                else:
                    return redirect("/dashboard")
        else:
                messages.error(request,'Login failed! Use existing national ID with correct password.')
    return render(request, 'registration/login.html', context={'form': form, 'message': message})

@login_required(login_url='/login/')
def ad_dashboard(request):
    customers = CustomUser.objects.filter(user_type='Customer')
    customers= customers.filter(is_staff=False)
    return render(request, 'users/dashboard.html', context={'customers':customers})

@login_required(login_url='/login/')
def add_customer(request):
    if request.user.is_staff==True:
        head="Add Customer"
        form = forms.UserForm(request.POST)
        if request.method == 'POST':
            form = forms.UserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Customer created sucessfully.')
                return redirect("/ad_dash")

        return render(request, 'users/application.html', context={'form':form, 'head':head})

def add_bank(request, id):
    if request.user.is_staff==True:
        head="Create Bank Account"
        customer = CustomUser.objects.filter(id=id)[0]
        accountN = Reference.generate(prefix="ACC/")
        if request.method == 'POST':    
            account= BankAccount(user=customer, account_no=accountN, phone_number=customer.phone_number, available_amount=0)
            accountN=account.account_no
            account.save()        
            messages.success(request, f'{accountN} has been created')
            return redirect("/customers")

        return render(request, 'users/application.html', context={'account':accountN, 'head':head})
def view_bank(request, id):
    if request.user.is_staff==True:
        head="View Bank accounts"
        customer = CustomUser.objects.filter(id=id)[0]
        accounts = BankAccount.objects.filter(user=customer)
        return render(request, 'bankaccount.html', context={'accounts':accounts, 'head':head})
    else:
         return redirect("/customers")

from datetime import datetime
from datetime import timedelta
from datetime import date
def add_card(request, id):
    if request.user.is_staff==True:
        head="Create card Account"
        bank = BankAccount.objects.filter(id=id)[0]
        cardN = Reference.generate(prefix="CARD/")
        if request.method == 'POST':  
            # taking input as the date
            Begindatestring = date.today()
            Begindatestring = date.today()
            
            # carry out conversion between string 
            # to datetime object
            Begindate = datetime.strptime(Begindatestring, "%Y-%m-%d")
            
            # print begin date
            print("Beginning date")
            print(Begindate)
            
            # calculating end date by adding 10 days
            Enddate = Begindate + timedelta(days=365*5)
            
            # printing end date
            print("Ending date")
            print(Enddate)


  
            card= Card(bank=bank, card_no=cardN, expiry_date=Enddate)
            cardN=card.account_no
            card.save()        
            messages.success(request, f'{cardN} has been created')
            return redirect("/customers")

        return render(request, 'users/application.html', context={'account':cardN, 'head':head})
def customers(request):
    customers = CustomUser.objects.filter(user_type='Customer')
    customers= customers.filter(is_staff=False)
    return render(request, 'customers.html', {'customers':customers})

@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'users/customer.html')