from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
import random
from .models import CustomUser
from .permissions import IsManagement
from .serializers import CustomUserSerializer
import os
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from django.contrib.auth.hashers import check_password


# Create your views here.
User = get_user_model()

logger = logging.getLogger(__name__)


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        try:
            user_id = validated_token['user_id']
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, validated_token


class SendOTPView(APIView):
    permission_classes = (permissions.AllowAny,)

    try:
        def post(self, request):
            email = request.data.get('email')
            password = request.data.get('password')
            user = CustomUser.objects.filter(email=email).first()
            if user is None:
                return Response({'error': 'User with given email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            if not password == user.password:
                return Response({'error': 'Password is incorrect, please enter right password','status': 401}, status=status.HTTP_401_UNAUTHORIZED)
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()

            # Render the template with context data
            html_message = render_to_string('otptemplate.html', {'otp': otp, 'first_name': user.first_name, 'last_name': user.last_name})
            EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

            send_mail(
                'Your OTP',
                f'Your OTP is {otp}',
                EMAIL_HOST_USER,
                [email],
                html_message=html_message,
                fail_silently=False,
            )

            return Response({'message': 'OTP sent', 'status': 200}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception("Error sending OTP")
        raise e


class VerifyOTPView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        otp_provided = request.data.get('otp')
        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            return Response({'error': 'Invalid OTP', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

        if str(user.otp) != str(otp_provided):
            return Response({'error': 'Invalid OTP', 'status': 401}, status=status.HTTP_401_UNAUTHORIZED)

        if timezone.now() > user.otp_created_at + timedelta(minutes=10):
            return Response({'error': 'OTP expired', 'status': 408}, status=status.HTTP_408_REQUEST_TIMEOUT)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'status': 200
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = (CustomJWTAuthentication,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out"})
        except Exception as e:
            logger.exception("Error logging out")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = [IsManagement]  # Only HOD users can create users.


@method_decorator(csrf_exempt, name='dispatch')
class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = [IsManagement]  # Only Management users can view users.


@method_decorator(csrf_exempt, name='dispatch')
class CustomUserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = [IsManagement]  # Only Management users can view users.


@method_decorator(csrf_exempt, name='dispatch')
class CustomUserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = [IsManagement]  # Only Management users can update users.


@method_decorator(csrf_exempt, name='dispatch')
class CustomUserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = [IsManagement]  # Only Management users can delete users.


@method_decorator(csrf_exempt, name='dispatch')
class CheckPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist"}, status=400)

        if check_password(password, user.password):
            return Response({"message": "Password matches"}, status=200)
        else:
            return Response({"error": "Password does not match"}, status=400)