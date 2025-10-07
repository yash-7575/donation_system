from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache  # ← Already imported
from django.http import JsonResponse
from .models import Donor, Recipient, NGO, Donation, Feedback
from .serializers import DonorSerializer, RecipientSerializer, NGOSerializer, DonationSerializer, FeedbackSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return Response({'status': 'ok'})


@never_cache  # ← ADD HERE
@api_view(['GET'])
def superadmin_demo(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM api_donation")
        donation_count = cursor.fetchone()[0]
        cursor.execute("SELECT city, COUNT(*) AS c FROM api_recipient GROUP BY city HAVING COUNT(*) > 0 ORDER BY c DESC LIMIT 5")
        top_cities = cursor.fetchall()
    return Response({
        'donation_count': donation_count,
        'top_cities': [{'city': row[0], 'count': row[1]} for row in top_cities],
    })


@never_cache  # ← ADD HERE
@csrf_exempt
@api_view(['GET', 'POST'])
def donors_list_create(request):
    if request.method == 'GET':
        donors = Donor.objects.all()
        serializer = DonorSerializer(donors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        password = request.data.get('password')
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            donor = serializer.save()
            if password:
                donor.set_password(password)
                donor.save()
            response_data = serializer.data
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)


@never_cache  # ← ADD HERE
@csrf_exempt
@api_view(['GET', 'POST'])
def recipients_list_create(request):
    if request.method == 'GET':
        recipients = Recipient.objects.all()
        serializer = RecipientSerializer(recipients, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        password = request.data.get('password')
        serializer = RecipientSerializer(data=request.data)
        if serializer.is_valid():
            recipient = serializer.save()
            if password:
                recipient.set_password(password)
                recipient.save()
            response_data = serializer.data
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)


@never_cache  
@csrf_exempt
@api_view(['GET', 'POST'])
def ngos_list_create(request):
    if request.method == 'GET':
        ngos = NGO.objects.all()
        serializer = NGOSerializer(ngos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        password = request.data.get('password')
        serializer = NGOSerializer(data=request.data)
        if serializer.is_valid():
            ngo = serializer.save()
            if password:
                ngo.set_password(password)
                ngo.save()
            response_data = serializer.data
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)


@never_cache  
@csrf_exempt
@api_view(['GET', 'POST'])
def donations_list_create(request):
    if request.method == 'GET':
        items = Donation.objects.select_related('donor', 'ngo').all()
        return Response(DonationSerializer(items, many=True).data)
    serializer = DonationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@never_cache  
@api_view(['GET'])
def donor_detail(request, donor_id):
    try:
        donor = Donor.objects.get(donor_id=donor_id)
        serializer = DonorSerializer(donor)
        return Response(serializer.data)
    except Donor.DoesNotExist:
        return Response({'error': 'Donor not found'}, status=404)


@never_cache  
@api_view(['GET'])
def recipient_detail(request, recipient_id):
    try:
        recipient = Recipient.objects.get(recipient_id=recipient_id)
        serializer = RecipientSerializer(recipient)
        return Response(serializer.data)
    except Recipient.DoesNotExist:
        return Response({'error': 'Recipient not found'}, status=404)


@never_cache  
@api_view(['GET'])
def ngo_detail(request, ngo_id):
    try:
        ngo = NGO.objects.get(ngo_id=ngo_id)
        serializer = NGOSerializer(ngo)
        return Response(serializer.data)
    except NGO.DoesNotExist:
        return Response({'error': 'NGO not found'}, status=404)


@never_cache  
@api_view(['GET'])
def donor_donations(request, donor_id):
    try:
        donor = Donor.objects.get(donor_id=donor_id)
        donations = Donation.objects.filter(donor=donor).select_related('ngo').order_by('-created_at')
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)
    except Donor.DoesNotExist:
        return Response({'error': 'Donor not found'}, status=404)


@csrf_exempt
@api_view(['POST'])
def match_donation(request):
    donation_id = request.data.get('donation_id')
    try:
        donation = Donation.objects.select_related('donor').get(donation_id=donation_id)
    except Donation.DoesNotExist:
        return Response({'error': 'donation not found'}, status=404)
    ngo = NGO.objects.filter(city=donation.donor.city).first()
    if ngo:
        donation.ngo = ngo
        donation.status = 'matched'
        donation.save()
        return Response({'matched': True, 'ngo_id': ngo.ngo_id})
    return Response({'matched': False})


@never_cache  # ← ALREADY ADDED ✓
@api_view(['GET'])
def join_operations(request, join_type):
    """Handle different types of JOIN queries for DBMS demonstration"""
    
    queries = {
        'equijoin': """
            SELECT 
                api_donor.name AS donor_name,
                api_donor.city,
                api_donation.title,
                api_donation.category,
                api_donation.status
            FROM api_donor
            INNER JOIN api_donation 
            ON api_donor.donor_id = api_donation.donor_id
            ORDER BY api_donor.name
        """,
        
        'non-equijoin': """
            SELECT 
                d1.name AS donor1,
                d1.city AS city1,
                d2.name AS donor2,
                d2.city AS city2
            FROM api_donor d1
            JOIN api_donor d2 
            ON d1.donor_id < d2.donor_id
            LIMIT 20
        """,
        
        'self-join': """
            SELECT 
                d1.name AS donor1,
                d2.name AS donor2,
                d1.city AS common_city
            FROM api_donor d1
            INNER JOIN api_donor d2 
            ON d1.city = d2.city 
            WHERE d1.donor_id < d2.donor_id
            ORDER BY d1.city
        """,
        
        'natural-join': """
            SELECT 
                api_donor.name,
                api_donor.city,
                api_donation.title,
                api_donation.quantity
            FROM api_donor
            INNER JOIN api_donation 
            ON api_donor.donor_id = api_donation.donor_id
            ORDER BY api_donor.name
        """,
        
        'left-join': """
            SELECT 
                api_donor.donor_id,
                api_donor.name,
                api_donor.city,
                COUNT(api_donation.donation_id) AS donation_count,
                COALESCE(SUM(api_donation.quantity), 0) AS total_items
            FROM api_donor
            LEFT OUTER JOIN api_donation 
            ON api_donor.donor_id = api_donation.donor_id
            GROUP BY api_donor.donor_id, api_donor.name, api_donor.city
            ORDER BY api_donor.name
        """,
        
        'right-join': """
            SELECT 
                api_donation.title,
                api_donation.category,
                api_donor.name AS donor_name,
                api_donor.city
            FROM api_donor
            RIGHT OUTER JOIN api_donation 
            ON api_donor.donor_id = api_donation.donor_id
            ORDER BY api_donation.title
        """,
        
        'full-join': """
            SELECT 
                api_donor.name AS donor_name,
                api_donation.title AS donation_title,
                api_donation.category,
                'Left Join' AS join_source
            FROM api_donor
            LEFT JOIN api_donation ON api_donor.donor_id = api_donation.donor_id
            UNION
            SELECT 
                api_donor.name AS donor_name,
                api_donation.title AS donation_title,
                api_donation.category,
                'Right Join' AS join_source
            FROM api_donor
            RIGHT JOIN api_donation ON api_donor.donor_id = api_donation.donor_id
            WHERE api_donor.donor_id IS NULL
            ORDER BY donor_name, donation_title
        """
    }
    
    if join_type not in queries:
        return JsonResponse({'error': 'Invalid join type'}, status=400)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(queries[join_type])
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        
        return JsonResponse({
            'success': True,
            'results': results,
            'query': queries[join_type],
            'join_type': join_type,
            'count': len(results)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
