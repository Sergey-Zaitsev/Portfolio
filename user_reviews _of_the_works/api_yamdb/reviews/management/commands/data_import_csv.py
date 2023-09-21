""" Импорт файлов CSV """
import csv

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

FIELED_DATA = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


class Command(BaseCommand):
    """ Команда вызывает импорт файлов из CSV в БД.
     Импорт вызывается командой python manage.py data_import_csv
    """

    def handle(self, *args, **kwargs):
        try:
            for model, csv_file in FIELED_DATA.items():
                with open(
                        f'{settings.BASE_DIR}/static/data/{csv_file}',
                        'r',
                        encoding='utf-8'
                ) as csvfile:
                    reader = csv.DictReader(csvfile)
                    model.objects.bulk_create(
                        model(**data) for data in reader)
        except IOError:
            print("An IOError has occurred!")
