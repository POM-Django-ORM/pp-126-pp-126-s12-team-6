from django.db import models
from author.models import Author

class Book(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    count = models.IntegerField(default=10)
    authors = models.ManyToManyField(Author)

    @classmethod
    def create(cls, **kwargs):
        if 'name' not in kwargs or 'description' not in kwargs:
            return None
        if len(kwargs['name']) > 128:
            return None
        count_val = kwargs.get('count', 10)
        book = cls(name=kwargs['name'], description=kwargs['description'], count=count_val)
        book.save()
        authors = kwargs.get('authors')
        if authors:
            for author in authors:
                book.authors.add(author)
        return book

    @classmethod
    def delete_by_id(cls, book_id):
        try:
            book = cls.objects.get(id=book_id)
            book.delete()
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_all(cls):
        return list(cls.objects.all())

    @classmethod
    def get_by_id(cls, book_id):
        try:
            return cls.objects.get(id=book_id)
        except cls.DoesNotExist:
            return None

    def add_authors(self, authors_list):
        for author in authors_list:
            self.authors.add(author)
        self.save()

    def remove_authors(self, authors_list):
        for author in authors_list:
            self.authors.remove(author)
        self.save()

    def update(self, **kwargs):
        allowed = ['name', 'description', 'count']
        for key, value in kwargs.items():
            if key in allowed:
                if key == 'name' and len(value) > 128:
                    continue
                setattr(self, key, value)
        self.save()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'authors': [author.id for author in self.authors.all()],
        }

    def __str__(self):
        d = self.to_dict()
        order = ['id', 'name', 'description', 'count', 'authors']
        return ", ".join(f"'{k}': {repr(d[k])}" for k in order)

    def __repr__(self):
        return f"Book(id={self.id})"
