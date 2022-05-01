from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    book_type = models.CharField(
        max_length=140,
        choices=(
            ("Sci-tech", "Sci-tech"),
            ("Magazine", "Magazine"),
            ("Comic", "Comic"),
            ("Classic", "Classic"),
            ("Horror", "Horror"),
        ),
    )
    ISBN = models.CharField(max_length=255)
    year_published = models.CharField(max_length=4)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    no_of_pages = models.PositiveIntegerField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
