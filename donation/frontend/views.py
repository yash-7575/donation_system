from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Avg, Sum
from django.db import connection
import json
import requests
import logging

from api.models import UserProfile, Donor, NGO, Recipient, Donation, Feedback
from .forms import SignupStep1Form, DonorProfileForm, NGOProfileForm, RecipientProfileForm

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')


# Step 1 - basic signup
def signup_step1(request):
    if request.method == 'POST':
        form = SignupStep1Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup_step1')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
                return redirect('signup_step1')

            # create User
            user = User.objects.create_user(username=username, email=email, password=password)
            # create profile with role
            profile = UserProfile.objects.create(user=user, role=role)

            # optionally auto login
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

            # redirect to role-specific registration
            if role == 'donor':
                return redirect('signup_donor')
            elif role == 'ngo':
                return redirect('signup_ngo')
            else:
                return redirect('signup_recipient')
    else:
        form = SignupStep1Form()
    return render(request, 'frontend/signup_step1.html', {'form': form})


# Step 2 - donor
def signup_donor(request):
    if not request.user.is_authenticated:
        return redirect('signup_step1')
    # ensure role
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'donor':
        messages.error(request, 'Unauthorized')
        return redirect('signup_step1')

    try:
        existing = request.user.donor_profile
        messages.info(request, 'Donor profile already exists')
        return redirect('signup_success')
    except Donor.DoesNotExist:
        pass

    if request.method == 'POST':
        form = DonorProfileForm(request.POST)
        if form.is_valid():
            Donor.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode'],
            )
            return redirect('signup_success')
    else:
        form = DonorProfileForm()
    return render(request, 'frontend/signup_donor.html', {'form': form})


# Step 2 - ngo
def signup_ngo(request):
    if not request.user.is_authenticated:
        return redirect('signup_step1')
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'ngo':
        messages.error(request, 'Unauthorized')
        return redirect('signup_step1')

    try:
        existing = request.user.ngo_profile
        messages.info(request, 'NGO profile already exists')
        return redirect('signup_success')
    except NGO.DoesNotExist:
        pass

    if request.method == 'POST':
        form = NGOProfileForm(request.POST)
        if form.is_valid():
            NGO.objects.create(
                user=request.user,
                ngo_name=form.cleaned_data['ngo_name'],
                phone=form.cleaned_data['phone'],
                website=form.cleaned_data['website'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode'],
            )
            return redirect('signup_success')
    else:
        form = NGOProfileForm()
    return render(request, 'frontend/signup_ngo.html', {'form': form})


# Step 2 - recipient
def signup_recipient(request):
    if not request.user.is_authenticated:
        return redirect('signup_step1')
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'recipient':
        messages.error(request, 'Unauthorized')
        return redirect('signup_step1')

    try:
        existing = request.user.recipient_profile
        messages.info(request, 'Recipient profile already exists')
        return redirect('signup_success')
    except Recipient.DoesNotExist:
        pass

    if request.method == 'POST':
        form = RecipientProfileForm(request.POST)
        if form.is_valid():
            Recipient.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                family_size=form.cleaned_data['family_size'],
                urgency=form.cleaned_data['urgency'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode'],
            )
            return redirect('signup_success')
    else:
        form = RecipientProfileForm()
    return render(request, 'frontend/signup_recipient.html', {'form': form})


# success page
def signup_success(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        user_profile = UserProfile.objects.get(user=request.user)
        role = user_profile.role

        if role == 'donor':
            return redirect('donor')
        elif role == 'ngo':
            return redirect('ngo')
        elif role == 'recipient':
            return redirect('recipient')
        else:
            return redirect('home')
    except UserProfile.DoesNotExist:
        return redirect('home')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on user role
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.role == 'donor':
                    return redirect('donor')
                elif user_profile.role == 'ngo':
                    return redirect('ngo')
                elif user_profile.role == 'recipient':
                    return redirect('recipient')
                else:
                    return redirect('home')
            except UserProfile.DoesNotExist:
                return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'login.html')

def logout_page(request):
    # Django's logout function handles session cleanup
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')


@csrf_protect
def register_page(request):
    if request.method == 'POST':
        # Handle donor registration
        try:
            # Prepare data for API call
            donor_data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone', ''),
                'address': request.POST.get('address', ''),
                'city': request.POST.get('city', ''),
                'state': request.POST.get('state', ''),
                'pincode': request.POST.get('pincode', ''),
                'password': request.POST.get('password', '')  # Store password (in a real app, we'd hash it)
            }
            
            logger.info(f"Attempting to create donor with data: {donor_data}")
            
            # Make API call to create donor
            # Use direct localhost URL instead of constructing from request
            api_url = "http://127.0.0.1:8000/api/donors/"
            response = requests.post(api_url, json=donor_data)
            
            logger.info(f"API response status: {response.status_code}")
            logger.info(f"API response text: {response.text}")
            
            if response.status_code == 200 or response.status_code == 201:
                # Successfully created donor, redirect to login page
                logger.info("Donor created successfully, redirecting to login")
                return redirect('login')
            else:
                # Handle error
                error_msg = response.text
                logger.error(f"API Error: {error_msg}")
                return render(request, 'register.html', {'error': f"API Error: {error_msg}"})
        except Exception as e:
            logger.error(f"Exception in donor registration: {str(e)}")
            return render(request, 'register.html', {'error': f"Exception: {str(e)}"})
    
    return render(request, 'register.html')


def donor_dashboard(request):
    # Ensure user is logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # Ensure user role is donor
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'donor':
            return redirect('home')
    except UserProfile.DoesNotExist:
        return redirect('home')

    # Handle donation submission (POST)
    if request.method == 'POST':
        try:
            # Get current donor profile from DB
            donor = Donor.objects.get(user=request.user)

            # Create donation directly — no API calls needed
            Donation.objects.create(
                donor=donor,
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                category=request.POST.get('category'),
                quantity=int(request.POST.get('quantity', 1)),
                status='pending',
                image_url=request.POST.get('image_url', '')
            )

            return JsonResponse({'success': True})

        except Donor.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Donor profile missing. Complete your profile.'})
        except Exception as e:
            logger.exception("Donation submission failed")
            return JsonResponse({'success': False, 'error': str(e)})

    # GET request → Display dashboard
    try:
        donor = Donor.objects.get(user=request.user)
        context = {'donor': donor}
    except Donor.DoesNotExist:
        context = {}

    return render(request, 'donor_dashboard.html', context)


def recipient_dashboard(request):
    # Placeholder: replicate donor layout for now
    return render(request, 'recipient_dashboard.html')


def ngo_dashboard(request):
    # Get the selected category from the request
    selected_category = request.GET.get('category', '')
    
    # Get basic counts (filtered by category if selected)
    donor_count = Donor.objects.count()
    recipient_count = Recipient.objects.count()
    
    # Get donations query (filtered by category if selected)
    donations_query = Donation.objects.all()
    if selected_category:
        donations_query = donations_query.filter(category=selected_category)
    
    donation_count = donations_query.count()
    
    # Get donation statistics (filtered by category if selected)
    total_items_donated = donations_query.aggregate(total=Sum('quantity'))['total'] or 0
    
    # Get delivered donations count (filtered by category if selected)
    delivered_count = donations_query.filter(status='delivered').count()
    
    # Get average rating from feedback (this is not category-specific in our current model)
    avg_rating = Feedback.objects.aggregate(avg=Avg('rating'))['avg']
    if avg_rating:
        avg_rating = round(avg_rating, 1)
    else:
        avg_rating = 0
    
    # Get donations by category (show all categories, but highlight selected)
    donations_by_category = Donation.objects.values('category').annotate(count=Count('category'))
    
    # Get donations by status (filtered by category if selected)
    donations_by_status = donations_query.values('status').annotate(count=Count('status'))
    
    # Get top cities by donor count (this is not category-specific)
    top_cities = Donor.objects.values('city').annotate(count=Count('city')).order_by('-count')[:5]
    
    # Define available categories
    available_categories = [
        'Clothing', 'Food', 'Electronics', 'Books', 
        'Furniture', 'Toys', 'Other'
    ]
    
    context = {
        'donors': Donor.objects.all(),
        'recipients': Recipient.objects.all(),
        'stats': {
            'donor_count': donor_count,
            'recipient_count': recipient_count,
            'donation_count': donation_count,
            'total_items_donated': total_items_donated,
            'delivered_count': delivered_count,
            'avg_rating': avg_rating,
            'donations_by_category': list(donations_by_category),
            'donations_by_status': list(donations_by_status),
            'top_cities': list(top_cities),
        },
        'selected_category': selected_category,
        'available_categories': available_categories
    }
    return render(request, 'ngo_dashboard.html', context)