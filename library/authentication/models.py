from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class CustomUser(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    @classmethod
    def create(cls, email, password, first_name, middle_name, last_name):
        if len(first_name) > 20 or len(last_name) > 20 or (middle_name and len(middle_name) > 20):
            return None
        try:
            validate_email(email)
        except ValidationError:
            return None
        try:
            user = cls(
                email=email,
                password=password,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
            )
            user.save()
            return user
        except (IntegrityError, Exception):
            return None

    @classmethod
    def get_by_email(cls, email):
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_by_id(cls, user_id):
        try:
            return cls.objects.get(id=user_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def delete_by_id(cls, user_id):
        user = cls.get_by_id(user_id)
        if user:
            user.delete()
            return True
        return False

    @classmethod
    def get_all(cls):
        return list(cls.objects.all())

    def update(self, *args, **kwargs):
        allowed = ['first_name', 'middle_name', 'last_name', 'email', 'password', 'role', 'is_active']
        if args:
            if len(args) != 6:
                raise TypeError(f"update() expects exactly 6 positional arguments, got {len(args)}")
            first_name, last_name, middle_name, password, role, is_active = args

            if len(first_name) > 20 or len(last_name) > 20 or (middle_name and len(middle_name) > 20):
                return self

            self.first_name = first_name
            self.last_name = last_name
            self.middle_name = middle_name
            self.password = password
            self.role = role
            self.is_active = is_active
        for key, value in kwargs.items():
            if key in allowed:
                if key in ['first_name', 'last_name'] and len(value) > 20:
                    continue
                if key == 'middle_name' and value and len(value) > 20:
                    continue
                setattr(self, key, value)
        self.save()
        return self

    def get_role_name(self):
        return "admin" if self.role == 1 else "visitor"

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'updated_at': int(self.updated_at.timestamp()) if self.updated_at else None,
            'role': self.role,
            'is_active': self.is_active,
        }

    def __str__(self):
        d = self.to_dict()
        order = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'created_at', 'updated_at', 'role', 'is_active']
        return ", ".join(f"'{k}': {repr(d[k])}" for k in order)

    def __repr__(self):
        return f"CustomUser(id={self.id})"
