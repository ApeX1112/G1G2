import csv
from django.core.management.base import BaseCommand
from api.models import AirportData
from datetime import datetime

class Command(BaseCommand):
    help = 'Load CSV data into the AirportData model'

    def handle(self, *args, **kwargs):
        with open('projet/data1.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Define a helper function to safely convert strings to float
                def parse_float(value):
                    if value == '' or value is None:
                        return None
                    try:
                        return float(value)
                    except ValueError:
                        return None

                def parse_int(value):
                    if value == '' or value is None:
                        return None
                    try:
                        return int(value)
                    except ValueError:
                        return None

                # Create an entry for each row in the CSV
                AirportData.objects.create(
                    start=row['Start'],
                    temperature_en_chiffre=parse_float(row['temperature_en_chiffre']),
                    humidity_en_chiffre=parse_int(row['humidity_en_chiffre']),
                    temperature_en_chiffre_2days_left=parse_float(row['temperature_en_chiffre_2days_left']),
                    humidity_en_chiffre_2days_left=parse_int(row['humidity_en_chiffre_2days_left']),
                    faa_designator=row.get('FAA_Designator', None),
                    length_ft=parse_float(row.get('Length_ft', None)),
                    tail_height_at_oew_ft=parse_float(row.get('Tail_Height_at_OEW_ft', None)),
                    wheelbase_ft=parse_float(row.get('Wheelbase_ft', None)),
                    date=datetime.strptime(row['DATE'], '%d.%m.%Y').date(),
                    std=datetime.strptime(row['STD'], '%d.%m.%Y %H:%M').time(),
                    atd=datetime.strptime(row['ATD'], '%d.%m.%Y %H:%M').time() if row['ATD'] else None,
                    type=row['Type'],
                    fluid=parse_int(row['Fluid']),
                    water=parse_int(row['Water']),
                    meteo=row.get('Meteo', None),
                    oat=parse_float(row['OAT']),
                    finish=row['Finish'],
                    duration=parse_float(row.get('Duration', None))
                )

        self.stdout.write(self.style.SUCCESS('Data successfully loaded into the database'))
