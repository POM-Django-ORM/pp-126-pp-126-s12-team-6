from django.db import models
from authentication.models import CustomUser
from book.models import Book

def format_dt(dt):
    s = dt.strftime("%Y-%m-%d %H:%M:%S%z")
    return s[:-2] + ":" + s[-2:] if len(s) >= 5 else s

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)
    plated_end_at = models.DateTimeField()

    @classmethod
    def create(cls, user, book, plated_end_at):
        if not user.pk:
            return None
        if book.count <= 1:
            return None
        try:
            order = cls(user=user, book=book, plated_end_at=plated_end_at)
            order.save()
            book.count -= 1
            book.save()
            return order
        except Exception:
            return None

    @classmethod
    def delete_by_id(cls, order_id):
        try:
            order = cls.objects.get(id=order_id)
            order.delete()
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_all(cls):
        return list(cls.objects.all())

    @classmethod
    def get_by_id(cls, order_id):
        try:
            return cls.objects.get(id=order_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_not_returned_books(cls):
        return list(cls.objects.filter(end_at__isnull=True))

    def update(self, **kwargs):
        allowed = ['end_at', 'plated_end_at']
        for key, value in kwargs.items():
            if key in allowed:
                setattr(self, key, value)
        self.save()
        return self

    def to_dict(self):
        dt_format = lambda dt: format_dt(dt) if dt else None
        return {
            'id': self.id,
            'user': self.user.__repr__(),
            'book': self.book.__repr__(),
            'end_at': dt_format(self.end_at),
            'plated_end_at': dt_format(self.plated_end_at),
        }

    def __str__(self):
        d = self.to_dict()
        parts = []
        for k in ['id', 'user', 'book', 'created_at', 'end_at', 'plated_end_at']:
            if k in ['user', 'book']:
                parts.append(f"'{k}': {d[k]}")
            else:
                parts.append(f"'{k}': {repr(d[k])}")
        return ", ".join(parts)

    def __repr__(self):
        return f"Order(id={self.id})"
