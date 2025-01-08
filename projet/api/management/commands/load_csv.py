import csv
from django.core.management.base import BaseCommand
from api.models import AirportData
from datetime import datetime

class Command(BaseCommand):
    help = 'Load CSV data into the AirportData model'

    def handle(self, *args, **kwargs):
        with open('projet/data.csv', newline='', encoding='utf-8') as csvfile:
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
                    
                def parse_time(datetime_str):
                    if datetime_str:
                        try:
                            # Parse the datetime string and extract time
                            parsed_datetime = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M')
                            return parsed_datetime.time()  # Return only the time part
                        except ValueError:
                            return None  # Return None for invalid format
                    return None
                
                def parse_date(date_str):
                    if date_str:
                        try:
                            # Parse the date string in 'DD.MM.YYYY' format
                            parsed_date = datetime.strptime(date_str, '%d.%m.%Y').date()
                            return parsed_date  # Return as date object
                        except ValueError:
                            return None  # Return None if format is incorrect
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
                    date = parse_date(row.get('DATE', None)),
                    
                    std=parse_float(row.get('STD', None)),
                    atd=parse_time(row.get('ATD', None)),
                    type=row.get('Type'),
                    fluid=parse_int(row['Fluid']),
                    water=parse_int(row['Water']),
                    meteo=row.get('Meteo', None),
                    oat=parse_float(row['OAT']),
                    finish=row.get('Finish'),
                    duration=parse_float(row.get('Duration', None)),

                    Wingspan_ft_without_winglets_sharklets=parse_float(row.get('Wingspan_ft_without_winglets_sharklets', None)),
                    Wingspan_ft_with_winglets_sharklets=parse_float(row.get('Wingspan_ft_with_winglets_sharklets', None)),
                    Cockpit_to_Main_Gear_ft=parse_float(row.get('Cockpit_to_Main_Gear_ft', None)),
                    Main_Gear_Width_ft=parse_float(row.get('Main_Gear_Width_ft', None)),
                    OneStep_Fluid=parse_float(row.get('OneStep Fluid', None)),
                    TwoStep_I_Fluid=parse_float(row.get('TwoStep I Fluid', None)),
                    TwoStep_II_Fluid=parse_float(row.get('TwoStep II Fluid', None)),
                    deicing_time_minutes=parse_float(row.get('deicing_time_minutes', None)),
                    meteo_numerical=parse_float(row.get('meteo_numerical', None)),
                    Month=parse_float(row.get('Month', None)),
                    Year=parse_float(row.get('Year', None)),
                    ACMARK=row.get('ACMARK', None),
                    ACTYPE=row.get('ACTYPE', None),
                    FLIGHT=row.get('FLIGHT', None),
                    CARRIER=row.get('CARRIER', None),
                )

        self.stdout.write(self.style.SUCCESS('Data successfully loaded into the database'))
