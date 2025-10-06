from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.db import connection
import json
import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)


def run_select(sql, params=None):
    """Helper function to execute SELECT queries and return results"""
    with connection.cursor() as cursor:
        cursor.execute(sql, params or {})
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return {
            'columns': columns,
            'rows': [dict(zip(columns, row)) for row in rows]
        }

def home(request):
    return render(request, 'home.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'donor')
        
        try:
            if role == 'donor':
                # Authenticate donor
                from api.models import Donor
                try:
                    donor = Donor.objects.get(email=email)
                    if donor.check_password(password):
                        # Store donor ID in session
                        request.session['user_id'] = donor.donor_id
                        request.session['user_type'] = 'donor'
                        return redirect('donor')
                    else:
                        return render(request, 'login.html', {'error': 'Invalid email or password'})
                except Donor.DoesNotExist:
                    return render(request, 'login.html', {'error': 'Invalid email or password'})
            
            elif role == 'recipient':
                # Authenticate recipient
                from api.models import Recipient
                try:
                    recipient = Recipient.objects.get(email=email)
                    if recipient.check_password(password):
                        # Store recipient ID in session
                        request.session['user_id'] = recipient.recipient_id
                        request.session['user_type'] = 'recipient'
                        return redirect('recipient')
                    else:
                        return render(request, 'login.html', {'error': 'Invalid email or password'})
                except Recipient.DoesNotExist:
                    return render(request, 'login.html', {'error': 'Invalid email or password'})
            
            elif role == 'ngo_admin':
                # Authenticate NGO
                from api.models import NGO
                try:
                    ngo = NGO.objects.get(email=email)
                    if ngo.check_password(password):
                        # Store NGO ID in session
                        request.session['user_id'] = ngo.ngo_id
                        request.session['user_type'] = 'ngo'
                        return redirect('ngo')
                    else:
                        return render(request, 'login.html', {'error': 'Invalid email or password'})
                except NGO.DoesNotExist:
                    return render(request, 'login.html', {'error': 'Invalid email or password'})
            
            else:
                return render(request, 'login.html', {'error': 'Invalid user role'})
                
        except Exception as e:
            logger.error(f"Exception in user login: {str(e)}")
            return render(request, 'login.html', {'error': f"Login failed: {str(e)}"})
    
    return render(request, 'login.html')


def logout_page(request):
    # Clear the session
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_type' in request.session:
        del request.session['user_type']
    return redirect('home')


@csrf_protect
def register_page(request):
    if request.method == 'POST':
        role = request.POST.get('role', 'donor')
        
        try:
            if role == 'donor':
                # Handle donor registration
                donor_data = {
                    'name': request.POST.get('name'),
                    'email': request.POST.get('email'),
                    'phone': request.POST.get('phone', ''),
                    'address': request.POST.get('address', ''),
                    'city': request.POST.get('city', ''),
                    'state': request.POST.get('state', ''),
                    'pincode': request.POST.get('pincode', ''),
                    'password': request.POST.get('password', '')
                }
                
                logger.info(f"Attempting to create donor with data: {donor_data}")
                
                # Make API call to create donor
                api_url = "http://127.0.0.1:8000/api/donors/"
                response = requests.post(api_url, json=donor_data)
                
                logger.info(f"API response status: {response.status_code}")
                logger.info(f"API response text: {response.text}")
                
                if response.status_code == 200 or response.status_code == 201:
                    logger.info("Donor created successfully, redirecting to login")
                    return redirect('login')
                else:
                    error_msg = response.text
                    logger.error(f"API Error: {error_msg}")
                    return render(request, 'register.html', {'error': f"API Error: {error_msg}"})
            
            elif role == 'recipient':
                # Handle recipient registration
                recipient_data = {
                    'name': request.POST.get('name'),
                    'email': request.POST.get('email'),
                    'phone': request.POST.get('phone', ''),
                    'family_size': request.POST.get('family_size', 1),
                    'urgency': request.POST.get('urgency', 'medium'),
                    'address': request.POST.get('address', ''),
                    'city': request.POST.get('city', ''),
                    'state': request.POST.get('state', ''),
                    'pincode': request.POST.get('pincode', ''),
                    'password': request.POST.get('password', '')
                }
                
                logger.info(f"Attempting to create recipient with data: {recipient_data}")
                
                # Make API call to create recipient
                api_url = "http://127.0.0.1:8000/api/recipients/"
                response = requests.post(api_url, json=recipient_data)
                
                logger.info(f"API response status: {response.status_code}")
                logger.info(f"API response text: {response.text}")
                
                if response.status_code == 200 or response.status_code == 201:
                    logger.info("Recipient created successfully, redirecting to login")
                    return redirect('login')
                else:
                    error_msg = response.text
                    logger.error(f"API Error: {error_msg}")
                    return render(request, 'register.html', {'error': f"API Error: {error_msg}"})
            
            elif role == 'ngo_admin':
                # Handle NGO registration
                ngo_data = {
                    'ngo_name': request.POST.get('ngo_name'),
                    'email': request.POST.get('email'),
                    'phone': request.POST.get('phone', ''),
                    'website': request.POST.get('website', ''),
                    'address': request.POST.get('address', ''),
                    'city': request.POST.get('city', ''),
                    'state': request.POST.get('state', ''),
                    'pincode': request.POST.get('pincode', ''),
                    'password': request.POST.get('password', '')
                }
                
                logger.info(f"Attempting to create NGO with data: {ngo_data}")
                
                # Make API call to create NGO
                api_url = "http://127.0.0.1:8000/api/ngos/"
                response = requests.post(api_url, json=ngo_data)
                
                logger.info(f"API response status: {response.status_code}")
                logger.info(f"API response text: {response.text}")
                
                if response.status_code == 200 or response.status_code == 201:
                    logger.info("NGO created successfully, redirecting to login")
                    return redirect('login')
                else:
                    error_msg = response.text
                    logger.error(f"API Error: {error_msg}")
                    return render(request, 'register.html', {'error': f"API Error: {error_msg}"})
            
            else:
                return render(request, 'register.html', {'error': 'Invalid user role'})
                
        except Exception as e:
            logger.error(f"Exception in user registration: {str(e)}")
            return render(request, 'register.html', {'error': f"Exception: {str(e)}"})
    
    return render(request, 'register.html')


def donor_dashboard(request):
    # Check if user is logged in and is a donor
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    
    if not user_id or user_type != 'donor':
        return redirect('login')
    
    if request.method == 'POST':
        # Handle donation submission
        try:
            donation_data = {
                'donor': user_id,
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
                logger.info("Donation created successfully")
                return JsonResponse({'success': True})
            else:
                error_msg = response.text
                logger.error(f"API Error: {error_msg}")
                return JsonResponse({'success': False, 'error': f"API Error: {error_msg}"})
        except Exception as e:
            logger.error(f"Exception in donation submission: {str(e)}")
            return JsonResponse({'success': False, 'error': f"Exception: {str(e)}"})
    
    # GET request - display donor dashboard with donor information and KPIs
    try:
        # Calculate KPIs using SQL
        donor_id = user_id
        
        kpi_sql = """
        SELECT 
            COUNT(*) AS total_donations,
            COALESCE(SUM(quantity), 0) AS total_items,
            SUM(CASE WHEN status='delivered' THEN 1 ELSE 0 END) AS delivered_count,
            SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END) AS pending_count,
            (SELECT AVG(f.rating)
             FROM api_feedback f
             JOIN api_donation d2 ON d2.donation_id = f.match_id
             WHERE d2.donor_id = %(donor_id)s) AS avg_rating
        FROM api_donation
        WHERE donor_id = %(donor_id)s
        """
        
        kpis_result = run_select(kpi_sql, {'donor_id': donor_id})
        kpis = kpis_result['rows'][0] if kpis_result['rows'] else {
            'total_donations': 0,
            'total_items': 0,
            'delivered_count': 0,
            'pending_count': 0,
            'avg_rating': None
        }
        
        # Fetch donor details from API
        api_url = f"http://127.0.0.1:8000/api/donors/{user_id}/"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            donor_data = response.json()
            context = {
                'donor': donor_data,
                'kpis': kpis,
                'kpi_sql': kpi_sql,
                'kpi_params': {'donor_id': donor_id}
            }
        else:
            # Fallback to database if API fails
            from api.models import Donor
            donor = Donor.objects.get(donor_id=user_id)
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
                },
                'kpis': kpis,
                'kpi_sql': kpi_sql,
                'kpi_params': {'donor_id': donor_id}
            }
    except Exception as e:
        logger.error(f"Error fetching donor information or KPIs: {str(e)}")
        context = {
            'kpis': {
                'total_donations': 0,
                'total_items': 0,
                'delivered_count': 0,
                'pending_count': 0,
                'avg_rating': None
            }
        }
    
    return render(request, 'donor_dashboard.html', context)


def recipient_dashboard(request):
    # Check if user is logged in and is a recipient
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    
    if not user_id or user_type != 'recipient':
        return redirect('login')
    
    # GET request - display recipient dashboard with recipient information
    try:
        # Fetch recipient details from API
        api_url = f"http://127.0.0.1:8000/api/recipients/{user_id}/"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            recipient_data = response.json()
            context = {'recipient': recipient_data}
        else:
            # Fallback to database if API fails
            from api.models import Recipient
            recipient = Recipient.objects.get(recipient_id=user_id)
            context = {
                'recipient': {
                    'recipient_id': recipient.recipient_id,
                    'name': recipient.name,
                    'email': recipient.email,
                    'phone': recipient.phone,
                    'family_size': recipient.family_size,
                    'urgency': recipient.urgency,
                    'address': recipient.address,
                    'city': recipient.city,
                    'state': recipient.state,
                    'pincode': recipient.pincode
                }
            }
    except Exception as e:
        logger.error(f"Error fetching recipient information: {str(e)}")
        context = {}
    
    return render(request, 'recipient_dashboard.html', context)


def ngo_dashboard(request):
    # Check if user is logged in and is an NGO
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    
    if not user_id or user_type != 'ngo':
        return redirect('login')
    
    # GET request - display NGO dashboard with NGO information
    try:
        # Fetch NGO details from API
        api_url = f"http://127.0.0.1:8000/api/ngos/{user_id}/"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            ngo_data = response.json()
            context = {'ngo': ngo_data}
        else:
            # Fallback to database if API fails
            from api.models import NGO
            ngo = NGO.objects.get(ngo_id=user_id)
            context = {
                'ngo': {
                    'ngo_id': ngo.ngo_id,
                    'ngo_name': ngo.ngo_name,
                    'email': ngo.email,
                    'phone': ngo.phone,
                    'website': ngo.website,
                    'address': ngo.address,
                    'city': ngo.city,
                    'state': ngo.state,
                    'pincode': ngo.pincode
                }
            }
    except Exception as e:
        logger.error(f"Error fetching NGO information: {str(e)}")
        context = {}
    
    return render(request, 'ngo_dashboard.html', context)