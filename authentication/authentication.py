# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework import exceptions
# from .models import BlacklistedToken

# class CustomJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         header = self.get_header(request)
#         if header is None:
#             return None

#         raw_token = self.get_raw_token(header)
#         if raw_token is None:
#             return None

#         if BlacklistedToken.objects.filter(token=str(raw_token)).exists():
#             raise exceptions.AuthenticationFailed("Token is blacklisted.")

#         validated_token = self.get_validated_token(raw_token)
#         return self.get_user(validated_token), validated_token