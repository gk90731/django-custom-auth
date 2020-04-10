from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User
from rest_auth.serializers import LoginSerializer

class CustomRegisterSerializer(RegisterSerializer):

    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    DOB = serializers.DateField(required=True)
    phone = serializers.IntegerField(required=True)
    def get_cleaned_data(self):

        
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'DOB': self.validated_data.get('DOB', ''),
            'phone': self.validated_data.get('phone', ''),
        }







# class CustomLoginSerializer(LoginSerializer):

#     phone = serializers.CharField(required=False, allow_blank=True)

#     def _validate_phone(self, phone, password):
#         if phone and password:
#             user = self.authenticate(phone=phone, password=password)
#         else:
#             msg = _('Must include "phone" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user
        











# class RegisterSerializer(serializers.Serializer):
#     username = serializers.CharField(
#         max_length=get_username_max_length(),
#         min_length=allauth_settings.USERNAME_MIN_LENGTH,
#         required=allauth_settings.USERNAME_REQUIRED
#     )
#     email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
#     password1 = serializers.CharField(write_only=True)
#     password2 = serializers.CharField(write_only=True)

#     def validate_username(self, username):
#         username = get_adapter().clean_username(username)
#         return username

#     def validate_email(self, email):
#         email = get_adapter().clean_email(email)
#         if allauth_settings.UNIQUE_EMAIL:
#             if email and email_address_exists(email):
#                 raise serializers.ValidationError(
#                     _("A user is already registered with this e-mail address."))
#         return email

#     def validate_password1(self, password):
#         return get_adapter().clean_password(password)

#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError(_("The two password fields didn't match."))
#         return data

#     def custom_signup(self, request, user):
#         pass

#     def get_cleaned_data(self):
#         return {
#             'username': self.validated_data.get('username', ''),
#             'password1': self.validated_data.get('password1', ''),
#             'email': self.validated_data.get('email', '')
#         }

#     def save(self, request):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         adapter.save_user(request, user, self)
#         self.custom_signup(request, user)
#         setup_user_email(request, user, [])
#         return user

class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email','first_name','last_name','DOB','phone')
        read_only_fields = ('email','phone',)

class CustomLoginSerializer(LoginSerializer):
    pass