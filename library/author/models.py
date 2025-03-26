from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=10)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)

    @classmethod
    def create(cls, name, surname, patronymic):
        if len(name) > 10 or len(surname) > 20 or len(patronymic) > 20:
            return None
        try:
            author = cls(name=name, surname=surname, patronymic=patronymic)
            author.save()
            return author
        except Exception:
            return None

    @classmethod
    def delete_by_id(cls, author_id):
        try:
            author = cls.objects.get(id=author_id)
            author.delete()
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_all(cls):
        return list(cls.objects.all())

    @classmethod
    def get_by_id(cls, author_id):
        try:
            return cls.objects.get(id=author_id)
        except cls.DoesNotExist:
            return None

    def update(self, **kwargs):
        allowed = ['name', 'surname', 'patronymic']
        for key, value in kwargs.items():
            if key in allowed:
                if key == 'name' and len(value) > 10:
                    continue
                if key in ['surname', 'patronymic'] and len(value) > 20:
                    continue
                setattr(self, key, value)
        self.save()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
        }

    def __str__(self):
        d = self.to_dict()
        order = ['id', 'name', 'surname', 'patronymic']
        return ", ".join(f"'{k}': {repr(d[k])}" for k in order)

    def __repr__(self):
        return f"Author(id={self.id})"
