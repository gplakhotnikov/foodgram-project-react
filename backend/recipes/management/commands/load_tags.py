import os
import psycopg2
from django.core.management.base import BaseCommand

HOST = os.getenv('DB_HOST')
NAME = os.getenv('DB_NAME')
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')

TAB = 'recipes_tag'


class Command(BaseCommand):
    help = 'Загрузка записей в базу данных из файла tags.csv'
    conn = psycopg2.connect(
        f'host={HOST} dbname={NAME} user={USER} password={PASSWORD}')
    cur = conn.cursor()

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            default='data/tags.csv',
            nargs='?',
            type=str,
            help='Путь к файлу tags.csv')

    def handle(self, *args, **kwargs):
        csv = kwargs['path']
        tab = TAB
        try:
            with open(csv, 'r') as file:
                self.cur.copy_from(
                    file,
                    tab,
                    sep=',',
                    columns=('name', 'color', 'slug'))
            self.conn.commit()
        except FileNotFoundError:
            raise CommandError('Файл не найден')
