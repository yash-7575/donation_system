from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import logging

from .models import Donor, NGO, Recipient, Donation  # Adjust imports for your model paths
from .serializers import DonorSerializer, RecipientSerializer, NGOSerializer, DonationSerializer  # Adjust for your serializers

logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def donations_list_create(request):
    if request.method == 'GET':
        items = Donation.objects.select_related('donor', 'ngo').all()
        serializer = DonationSerializer(items, many=True)
        return Response(serializer.data)

    logger.info(f"Received donation data: {request.data}")
    serializer = DonationSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        logger.info(f"Donation saved: {serializer.data} (pk={getattr(obj, 'donation_id', getattr(obj, 'id', 'n/a'))})")
        return Response(serializer.data, status=201)
    logger.error(f"Validation errors: {serializer.errors}")
    return Response({'error': 'Invalid data', 'details': serializer.errors}, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return Response({'status': 'ok'})


@api_view(['GET'])
def superadmin_demo(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM api_donation")
        donation_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT city, COUNT(*) AS c 
            FROM api_recipient 
            GROUP BY city 
            HAVING COUNT(*) > 0 
            ORDER BY c DESC 
            LIMIT 5
        """)
        top_cities = cursor.fetchall()

    return Response({
        'donation_count': donation_count,
        'top_cities': [{'city': row[0], 'count': row[1]} for row in top_cities],
    })


@csrf_exempt
@api_view(['GET', 'POST'])
def donors_list_create(request):
    if request.method == 'GET':
        donors = Donor.objects.all()
        serializer = DonorSerializer(donors, many=True)
        data = serializer.data
        for donor in data:
            donor.pop('password', None)
        return Response(data)

    serializer = DonorSerializer(data=request.data)
    password = request.data.get('password')
    if serializer.is_valid():
        donor = serializer.save()
        if password:
            donor.set_password(password)
            donor.save()
        response_data = serializer.data
        response_data.pop('password', None)
        return Response(response_data, status=201)
    return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
def recipients_list_create(request):
    if request.method == 'GET':
        items = Recipient.objects.all()
        serializer = RecipientSerializer(items, many=True)
        return Response(serializer.data)

    serializer = RecipientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
def ngos_list_create(request):
    if request.method == 'GET':
        items = NGO.objects.all()
        serializer = NGOSerializer(items, many=True)
        return Response(serializer.data)

    serializer = NGOSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def donor_detail(request, donor_id):
    try:
        donor = Donor.objects.get(donor_id=donor_id)
        serializer = DonorSerializer(donor)
        data = serializer.data
        data.pop('password', None)
        return Response(data)
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


@api_view(['GET'])
def donation_donor_join(request):
    with connection.cursor() as cursor:
        query = '''
        SELECT 
            d.donation_id,
            d.title,
            d.category,
            d.quantity,
            d.status,
            dn.name as donor_name,
            dn.email as donor_email,
            dn.city as donor_city,
            dn.state as donor_state
        FROM api_donation d
        INNER JOIN api_donor dn ON d.donor_id = dn.donor_id
        ORDER BY d.created_at DESC
        '''
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]

    return Response({
        'query': query.strip(),
        'results': results,
        'total_count': len(results)
    })


@api_view(['GET'])
def donation_recipient_join(request):
    with connection.cursor() as cursor:
        query = '''
        SELECT 
            d.donation_id,
            d.title,
            d.category,
            d.status,
            r.name as recipient_name,
            r.city as recipient_city,
            r.family_size,
            r.urgency
        FROM api_donation d
        LEFT JOIN api_match m ON d.donation_id = m.donation_id
        LEFT JOIN api_recipient r ON m.recipient_id = r.recipient_id
        ORDER BY d.created_at DESC
        '''
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]

    return Response({
        'query': query.strip(),
        'results': results,
        'total_count': len(results)
    })
