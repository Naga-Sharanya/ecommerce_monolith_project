from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile, Address, TokenBlacklist, Role, UserRole
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    AddressSerializer,
    ChangePasswordSerializer,
    UserRoleSerializer,
)

User = get_user_model()


# User Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


# User Login View
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Profile Management View
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    def patch(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Change Password View
class ChangePasswordView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"success": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Logout View
class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            TokenBlacklist.objects.create(token=refresh_token)
            return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)


# Address Management View
class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Role Assignment View
class RoleAssignmentView(generics.CreateAPIView):
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]
