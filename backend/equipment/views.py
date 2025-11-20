from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Dataset, Equipment
from .serializers import DatasetSerializer, DatasetSummarySerializer, EquipmentSerializer
from .utils import process_csv_file, generate_pdf_report
import pandas as pd
import io


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Handle user login and return auth token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({'error': 'Invalid credentials'}, 
                       status=status.HTTP_401_UNAUTHORIZED)
    
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.pk,
        'username': user.username
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Handle user registration"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password, email=email)
    token = Token.objects.create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.pk,
        'username': user.username
    }, status=status.HTTP_201_CREATED)


class DatasetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing datasets"""
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return DatasetSummarySerializer
        return DatasetSerializer

    def list(self, request):
        """Return last 5 datasets"""
        datasets = Dataset.objects.all()[:5]
        serializer = self.get_serializer(datasets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        """Handle CSV file upload and processing"""
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        csv_file = request.FILES['file']
        
        # Validate file type
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File must be a CSV'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response({'error': f'Missing columns: {", ".join(missing_columns)}'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Process the CSV data
            dataset_name = csv_file.name
            dataset, equipment_list = process_csv_file(df, dataset_name, request.user)
            
            # Maintain only last 5 datasets
            all_datasets = Dataset.objects.all()
            if all_datasets.count() > 5:
                datasets_to_delete = all_datasets[5:]
                for ds in datasets_to_delete:
                    ds.delete()
            
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': f'Error processing file: {str(e)}'}, 
                          status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get summary statistics for a dataset"""
        dataset = self.get_object()
        serializer = DatasetSummarySerializer(dataset)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def generate_report(self, request, pk=None):
        """Generate PDF report for a dataset"""
        dataset = self.get_object()
        
        try:
            pdf_buffer = generate_pdf_report(dataset)
            
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{dataset.name}"'
            
            return response
            
        except Exception as e:
            return Response({'error': f'Error generating report: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
