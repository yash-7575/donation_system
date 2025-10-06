from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
import json
import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to authenticate the donor
        try:
            # Make API call to get donor by email
            api_url = f"http://127.0.0.1:8000/api/donors/"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                donors = response.json()
                donor_data = None
                for d in donors:
                    if d['email'] == email:
                        donor_data = d
                        break
                
                if donor_data:
                    # For now, we're doing a simple comparison (in a real app, we'd use proper password hashing)
                    # Let's check the database directly for proper password verification
                    from api.models import Donor
                    try:
                        donor = Donor.objects.get(email=email)
                        if donor.check_password(password):
                            # Store donor ID in session
                            request.session['donor_id'] = donor.donor_id
                            return redirect('donor')
                        else:
                            return render(request, 'login.html', {'error': 'Invalid email or password'})
                    except Donor.DoesNotExist:
                        return render(request, 'login.html', {'error': 'Invalid email or password'})
                else:
                    return render(request, 'login.html', {'error': 'Invalid email or password'})
            else:
                return render(request, 'login.html', {'error': 'Authentication service unavailable'})
        except Exception as e:
            logger.error(f"Exception in donor login: {str(e)}")
            return render(request, 'login.html', {'error': f"Login failed: {str(e)}"})
    
    return render(request, 'login.html')


def logout_page(request):
    # Clear the session
    if 'donor_id' in request.session:
        del request.session['donor_id']
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
    # Check if donor is logged in
    donor_id = request.session.get('donor_id')
    if not donor_id:
        return redirect('login')
    
    if request.method == 'POST':
        # Handle donation submission
        try:
            # Fetch donor details from API
            api_url = f"http://127.0.0.1:8000/api/donors/{donor_id}/"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                donor_data = response.json()
            else:
                # Fallback to database if API fails
                from api.models import Donor
                donor = Donor.objects.get(donor_id=donor_id)
                donor_data = {
                    'donor_id': donor.donor_id,
                    'name': donor.name,
                    'email': donor.email,
                    'phone': donor.phone,
                    'address': donor.address,
                    'city': donor.city,
                    'state': donor.state,
                    'pincode': donor.pincode
                }
            
            donation_data = {
                'donor': donor_id,
                'title': request.POST.get('title'),
                'description': request.POST.get('description', ''),
                'category': request.POST.get('category'),
                'quantity': int(request.POST.get('quantity', 1)),
                'status': 'pending'
            }
            
            logger.info(f"Attempting to create donation with data: {donation_data}")
            
            # Make API call to create donation
            api_url = "http://127.0.0.1:8000/api/donations/"
            response = requests.post(api_url, json=donation_data)
            
            logger.info(f"API response status: {response.status_code}")
            logger.info(f"API response text: {response.text}")
            
            if response.status_code == 200 or response.status_code == 201:
                # Successfully created donation
                logger.info("Donation created successfully")
                # Return success response
                return JsonResponse({'success': True})
            else:
                # Handle error
                error_msg = response.text
                logger.error(f"API Error: {error_msg}")
                return JsonResponse({'success': False, 'error': f"API Error: {error_msg}"})
        except Exception as e:
            logger.error(f"Exception in donation submission: {str(e)}")
            return JsonResponse({'success': False, 'error': f"Exception: {str(e)}"})
    
    # GET request - display donor dashboard with donor information
    try:
        # Fetch donor details from API
        api_url = f"http://127.0.0.1:8000/api/donors/{donor_id}/"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            donor_data = response.json()
            context = {'donor': donor_data}
        else:
            # Fallback to database if API fails
            from api.models import Donor
            donor = Donor.objects.get(donor_id=donor_id)
            context = {
                'donor': {
                    'donor_id': donor.donor_id,
                    'name': donor.name,
                    'email': donor.email,
                    'phone': donor.phone,
                    'address': donor.address,
                    'city': donor.city,
                    'state': donor.state,
                    'pincode': donor.pincode
                }
            }
    except Exception as e:
        logger.error(f"Error fetching donor information: {str(e)}")
        context = {}
    
    return render(request, 'donor_dashboard.html', context)


def recipient_dashboard(request):
    # Placeholder: replicate donor layout for now
    return render(request, 'recipient_dashboard.html')


def ngo_dashboard(request):
    return render(request, 'ngo_dashboard.html')