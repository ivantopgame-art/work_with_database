import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from phones.models import Phone


class Command(BaseCommand):
    help = 'Импорт телефонов из CSV-файла'

    def handle(self, *args, **options):
        with open('phones.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                phone, created = Phone.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'price': row['price'],
                        'image': row.get('image', ''),
                        'release_date': datetime.strptime(row['release_date'], '%Y-%m-%d').date(),
                        'lte_exists': row.get('lte_exists', 'False').lower() == 'true',
                        'slug': slugify(row['name']),
                    }
                )
                if created:
                    self.stdout.write(f'Добавлен: {phone.name}')
                else:
                    self.stdout.write(f'Уже есть: {phone.name}')

        self.stdout.write(self.style.SUCCESS('Импорт завершён'))