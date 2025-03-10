from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .registerform import RegisterForm
from .contactform import ContactForm
from .models import Ticket
from .inventoryform import ProductForm
from .models import Product

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()  # Handle GET request here

    return render(request, 'accounts/register.html', {'form': form})

        
def login_view(request):
    error_message = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'index'
            return redirect(next_url)
        else:
            error_message = "Invalid Credentials!"

    return render(request, 'accounts/login.html', {'error': error_message})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('index')

#Using the decorator

@login_required
def home_view(request):
    return render(request, 'index.html')

# Protected View
class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    # 'next' - to redirect URL
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'registration/protected.html')

# Home View
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    tickets = Ticket.objects.all()
    context = {'tickets': tickets}
    return render(request, 'index.html', context)

# This is the home page view function.
def home_view(request):
    return render(request, 'index.html')

# Define the contact_view function to handle the contact form.
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            return redirect('contact-success')
    else:
        form = ContactForm()
    context = {'form':form}
    return render(request, 'app_forms/contact.html', context)

# Define the contact_success_view function to handle the success page
def contact_success_view(request):
    return render(request, 'app_forms/contact_success.html' )

# CRUD = Create , Read, Update, Delete
# Home View
def home_view(request):
    return render(request, 'index.html')


# Create View
def product_create_view(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    return render(request, 'invApp/product_form.html', {'form':form})

# Read View
def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'invApp/product_list.html', {'products':products})

# Update View
def product_update_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    return render(request, 'invApp/product_form.html', {'form':form})   
 
# Delete View
def product_delete_view(request, product_id):
    product = Product.objects.get(product_id = product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'invApp/product_confirm_delete.html', {'product':product})