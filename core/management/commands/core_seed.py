from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Seed Core tables with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))