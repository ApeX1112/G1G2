from django.shortcuts import render
from .models import AirportData
from django.db.models import F, ExpressionWrapper, DurationField, Avg,Count
import json
from django.db.models.functions import ExtractMonth
import calendar

def dashboard(request):
    # 1. Temperature and Humidity (Line Chart)
    temp_humidity_data = AirportData.objects.values('date', 'temperature_en_chiffre', 'humidity_en_chiffre').order_by('date')
    
    # Extract labels (dates) and data for temperature and humidity
    temp_humidity_labels = [x['date'].strftime('%Y-%m-%d') for x in temp_humidity_data]  # Format date as YYYY-MM-DD
    temperature_data = [x['temperature_en_chiffre'] for x in temp_humidity_data]
    humidity_data = [x['humidity_en_chiffre'] for x in temp_humidity_data]

    # 2. Average Delay of Deicing (Bar Chart)
    data_with_delay = AirportData.objects.exclude(atd__isnull=True, std__isnull=True).annotate(
        delay=ExpressionWrapper(
            (F('atd') - F('std')),
            output_field=DurationField()
        )
    )

    # 2. Group by date and calculate the average delay in minutes for each day
    avg_delay_per_day = data_with_delay.values('date').annotate(
        avg_delay=Avg('delay')
    ).order_by('date')

    # Convert the delay to minutes, handling possible None values in 'delay'
    avg_delay_labels = [x['date'].strftime('%Y-%m-%d') for x in avg_delay_per_day]
    avg_delay_data = [(x['avg_delay'].total_seconds() / 60) if x['avg_delay'] else 0 for x in avg_delay_per_day]  # Convert seconds to minutes

    # For temperature and humidity (assuming these are needed for another chart)
    temp_humidity_data = AirportData.objects.values('date', 'temperature_en_chiffre', 'humidity_en_chiffre').order_by('date')
    temp_humidity_labels = [x['date'].strftime('%Y-%m-%d') for x in temp_humidity_data]
    temperature_data = [x['temperature_en_chiffre'] for x in temp_humidity_data]
    humidity_data = [x['humidity_en_chiffre'] for x in temp_humidity_data]

    # 3. Deicing Fluid Usage Distribution (Pie Chart)
    fluid_usage = AirportData.objects.values('fluid').annotate(count=Count('fluid'))
    fluid_labels = [str(x['fluid']) for x in fluid_usage]
    fluid_pie_data = [x['count'] for x in fluid_usage]


    # 5. Weather Conditions Breakdown (Radar Chart)
    weather_conditions = (
    AirportData.objects
    .values('meteo')
    .annotate(avg_duration=Avg('duration'))
    .order_by('meteo')
)

    # Extract the labels and data for weather conditions
    weather_labels = [x['meteo'] for x in weather_conditions]
    weather_radar_data = [x['avg_duration'] for x in weather_conditions]
    # 6. Daily Aircraft Count (Line Chart)
    daily_aircraft_count = AirportData.objects.values('date').annotate(count=Count('date'))
    daily_aircraft_labels = [str(x['date']) for x in daily_aircraft_count]
    daily_aircraft_data = [x['count'] for x in daily_aircraft_count]

    # 7. Aircraft Length vs Duration (Bubble Chart)
    aircraft_length_bubble = AirportData.objects.values('length_ft', 'duration')
    print(aircraft_length_bubble)
    aircraft_length_bubble_data = [{'x': x['length_ft'], 'y': x['duration'], 'r': 10} for x in aircraft_length_bubble]

    # 8. Monthly Deicing Operations (Bar Chart)
    monthly_deicing = (
    AirportData.objects
    .annotate(month=ExtractMonth('date'))
    .values('month')
    .annotate(count=Count('id'))
    .order_by('month')
)

    # Convert month numbers to month names and create labels and data lists
    monthly_labels = [calendar.month_name[x['month']] for x in monthly_deicing]
    monthly_deicing_data = [x['count'] for x in monthly_deicing]

    # 9. Average Fluid Usage per FAA Designator (Radar Chart)
    faa_designators = AirportData.objects.values('faa_designator').annotate(avg_fluid=Avg('fluid'))
    faa_labels = [x['faa_designator'] for x in faa_designators]
    faa_fluid_data = [x['avg_fluid'] for x in faa_designators]

    # 10. Temperature and Duration (Line Chart)
    temp_duration = AirportData.objects.values('temperature_en_chiffre', 'duration')
    temp_duration_labels = list(range(len(temp_duration)))
    temperature_data = [x['temperature_en_chiffre'] for x in temp_duration]
    duration_data = [x['duration'] for x in temp_duration]

    context = {
        'temp_humidity_labels': json.dumps(temp_humidity_labels),
        'temperature_data': json.dumps(temperature_data),
        'humidity_data': json.dumps(humidity_data),
        'avg_delay_labels': json.dumps(avg_delay_labels),
        'avg_delay_data': json.dumps(avg_delay_data),
        'fluid_labels': json.dumps(fluid_labels),
        'fluid_pie_data': json.dumps(fluid_pie_data),
        
        'weather_labels': json.dumps(weather_labels),
        'weather_radar_data': json.dumps(weather_radar_data),
        'daily_aircraft_labels': json.dumps(daily_aircraft_labels),
        'daily_aircraft_data': json.dumps(daily_aircraft_data),
        'aircraft_length_bubble_data': json.dumps(aircraft_length_bubble_data),
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_deicing_data': json.dumps(monthly_deicing_data),
        'faa_labels': json.dumps(faa_labels),
        'faa_fluid_data': json.dumps(faa_fluid_data),
        'temp_duration_labels': json.dumps(temp_duration_labels),
        'duration_data': json.dumps(duration_data)
    }

    return render(request, 'airport.html', context)




def ModelView(request):

    aircraft_list = AirportData.objects.values('faa_designator').distinct()
    selected_craft = None
    aircraft_info = None

    temp = None
    hum = None
    temp1 = None
    hum1 = None
    algorithm_choice = None
    

    if request.method== 'POST':

        if 'faa_designator' in request.POST:
            # Aircraft selection
            selected_aircraft = request.POST.get("faa_designator")
            aircraft_info = AirportData.objects.filter(faa_designator=selected_aircraft).first()
            stage = "meteorological_data"  # Move to the meteorological data stage

        elif 'temp' in request.POST and 'hum' in request.POST:
            # Meteorological data input
            temp = request.POST.get("temp")
            hum = request.POST.get("hum")
            temp1 = request.POST.get("temp1")
            hum1 = request.POST.get("hum1")
            stage = "algorithm_choice"  # Move to the algorithm choice stage

        elif 'algorithm_choice' in request.POST:
            # Algorithm choice
            algorithm_choice = request.POST.get("algorithm_choice")
            stage = "complete"  # Final stage


    context={'aircraft_list':aircraft_list, 
             'selected_aircraft':selected_craft,
             'selected_aircraft':selected_craft,
             'aircraft_info':aircraft_info,
             'temp': temp,
            'hum': hum,
            'temp1': temp1,
            'hum1': hum1,
            'algorithm_choice': algorithm_choice,
            
             }
    return render(request,'model.html',context)
