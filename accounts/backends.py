from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:

            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


class HardcodedDevBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Логін і пароль адміна. Суто для розробки! Потім видалю
        if username == 'admin' and password == 'admin123':

            user, created = User.objects.get_or_create(username='admin_dev', defaults={'email': 'admin@dev.com'})

            if created:
                user.set_password('admin123')
                user.is_staff = True
                user.is_superuser = True
                user.role = 'admin'
                user.save()


            if user.check_password('admin123'):
                return user
        return None