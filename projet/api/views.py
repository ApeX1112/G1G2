from django.shortcuts import render
from .models import AirportData
from django.db.models import F, ExpressionWrapper, DurationField, Avg,Count
import json
from django.db.models.functions import ExtractMonth
import calendar
from django.http import JsonResponse

import joblib
import numpy as np





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
            ( F('duration')),
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

import time 
def predict(input):
    time.sleep(1)
    model=joblib.load('projet/model.pkl')
    return model.predict(input)
    
def encode_carrier_from_abbr(carrier_abbr, carrier_list):
    
    # Create a zero vector with the same length as the carrier list
    one_hot_vector = [0] * len(carrier_list)

    
    # Find the carrier in the list based on abbreviation
    for index, full_carrier in enumerate(carrier_list):
        if full_carrier.endswith(f"_{carrier_abbr}"):  # Match based on the abbreviation
            one_hot_vector[index] = 1
            break  # Exit the loop after finding the match
    
    return one_hot_vector
def encode_month(month, month_list):
    """
    Convert a month name or number to a one-hot encoded vector.
    
    Parameters:
        month (str): The name (e.g., "January") or number (e.g., "1") of the month.
        month_list (list): The ordered list of months (e.g., "Month_January").
    
    Returns:
        list: A one-hot encoded vector with a 1 at the position matching the month.
    """
    # Create a zero vector with the same length as the month list
    one_hot_vector = [0] * len(month_list)

    if month :

        # Normalize the month input (e.g., convert number to name if needed)
        if month.isdigit():
            month = month_list[int(month) - 1]  # Convert to the corresponding month name
        else:
            month = f'Month_{month.capitalize()}'

        # Find the index of the month in the list
        try:
            index = month_list.index(month)
            one_hot_vector[index] = 1  # Set the corresponding index to 1
        except ValueError:
            # Month not found; handle it (e.g., leave as all zeros or raise an error)
            pass
        
        return one_hot_vector

def ModelView(request):
    CARRIER_LIST = [
        'CARRIER_AEG', 'CARRIER_AHO', 'CARRIER_AP', 'CARRIER_ATL', 'CARRIER_BV',
        'CARRIER_CAR', 'CARRIER_CCC', 'CARRIER_DC', 'CARRIER_EJM', 'CARRIER_EN',
        'CARRIER_ENT', 'CARRIER_EUR', 'CARRIER_EW', 'CARRIER_EXC', 'CARRIER_FR',
        'CARRIER_FRD', 'CARRIER_GA', 'CARRIER_GAC', 'CARRIER_GTI', 'CARRIER_IFM',
        'CARRIER_IG', 'CARRIER_JDI', 'CARRIER_KLC', 'CARRIER_LH', 'CARRIER_LO',
        'CARRIER_LP', 'CARRIER_LPR', 'CARRIER_LS', 'CARRIER_LX', 'CARRIER_NJE',
        'CARRIER_OY', 'CARRIER_PL', 'CARRIER_ROY', 'CARRIER_SCH', 'CARRIER_SK',
        'CARRIER_SRN', 'CARRIER_STR', 'CARRIER_SWT', 'CARRIER_TOY', 'CARRIER_UPS',
        'CARRIER_USA', 'CARRIER_VJT', 'CARRIER_W6', 'CARRIER_WIL', 'CARRIER_WR'
    ]

    MONTH_LIST = [
        'Month_April','Month_December','Month_February','Month_January' , 'Month_March' , 'Month_May','Month_November','Month_October'
    ]
    aircraft_list = AirportData.objects.values('faa_designator').distinct()
    selected_aircraft = None
    aircraft_info = None
    data={}

    


    # Initialize variables for weather data
    temp = hum = temp1 = hum1 = std = oat = type_ = fluid = water = carrier = algorithm_choice = None

    # Get distinct carriers
    carrier_list = AirportData.objects.values_list('CARRIER', flat=True).distinct().order_by('CARRIER')

    prediction_result = None  # To store prediction result

    if request.method == 'POST':
        form_data = request.POST

        # Handle Aircraft Selection
        if 'faa_designator' in form_data:
            selected_aircraft = form_data.get("faa_designator")
            aircraft_info = AirportData.objects.filter(faa_designator=selected_aircraft).first()
            data = {
                "length_ft": aircraft_info.length_ft,
                "tail_height_at_oew_ft": aircraft_info.tail_height_at_oew_ft,
                "wheelbase_ft": aircraft_info.wheelbase_ft,
                "wingspan_without_winglets": aircraft_info.Wingspan_ft_without_winglets_sharklets,
                "wingspan_with_winglets": aircraft_info.Wingspan_ft_with_winglets_sharklets,
                "cockpit_to_main_gear": aircraft_info.Cockpit_to_Main_Gear_ft,
                "main_gear_width": aircraft_info.Main_Gear_Width_ft
            }

            

            

        # Handle Weather Conditions
        temp = form_data.get("temperature")
        hum = form_data.get("humidity")
        temp1 = form_data.get("humidity2_days_ago")
        hum1 = form_data.get("humidity2_days_ago_2")
        std = form_data.get("std")
        oat = form_data.get("oat")
        type_ = form_data.get("type")
        fluid = form_data.get("fluid")
        water = form_data.get("water")
        carrier = form_data.get("carrier")

        carrier_encoded = encode_carrier_from_abbr(carrier, CARRIER_LIST)

        Wingspan_ft_without_winglets=form_data.get("wingspanWithoutWinglets")
        Wingspan_ft_with_winglets=form_data.get("wingspanWithWinglets")
        Cockpit_to_Main_Gear=form_data.get("cockpitToMainGear")
        Main_Gear_Width=form_data.get("mainGearWidth")
        length=form_data.get("length")
        tailHeight=form_data.get("tailHeight")
        wheelbase=form_data.get("wheelbase")

        month = form_data.get("month")  # Numeric representation of the month
        one_step_fluid = form_data.get("one_step_fluid")
        two_step_i_fluid = form_data.get("two_step_i_fluid")
        two_step_ii_fluid = form_data.get("two_step_ii_fluid")
        meteo_numerical = form_data.get("meteo_numerical")
        deicing_time_shift_1 = form_data.get("deicing_time_shift_1")
        deicing_time_shift_2 = form_data.get("deicing_time_shift_2")
        deicing_time_shift_3 = form_data.get("deicing_time_shift_3")
        if deicing_time_shift_3:
            deicing_time_rolling = (float(deicing_time_shift_1)+float(deicing_time_shift_2)+float(deicing_time_shift_3))/3

        month_encoded = encode_month(month, MONTH_LIST)



        
        

        # Handle Algorithm Selection
        algorithm_choice = form_data.get("algorithm_choice")

        # Debugging Prints (optional)
        if algorithm_choice:
            prediction_input = [
            temp, hum,
            temp1, hum1,
            Wingspan_ft_without_winglets,Wingspan_ft_with_winglets
            ,length,tailHeight,
            wheelbase,Cockpit_to_Main_Gear,
            Main_Gear_Width,std,type_,fluid,water,oat,one_step_fluid
            ,two_step_i_fluid,two_step_ii_fluid,meteo_numerical
        ] + carrier_encoded +[2025]+month_encoded+[deicing_time_shift_1,deicing_time_shift_2,deicing_time_shift_3,deicing_time_rolling]
        
        
            prediction_input=np.array(prediction_input).astype('float')

        # If the request is AJAX, return a JSON response
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if algorithm_choice == 'catboost':

                
                prediction=predict(prediction_input)




                if prediction is not None:
                    response_data = {
                        'message': 'Prediction successful',
                        'prediction': prediction,
                    }
                else:
                    response_data = {
                        'message': 'Invalid input values for prediction',
                        'prediction': None,
                    }
            else:
                response_data = {
                    'message': 'Selected algorithm is not supported yet.',
                    'prediction': None,
                }
            return JsonResponse(response_data)

    context = {
        'aircraft_list': aircraft_list,
        'selected_aircraft': selected_aircraft,
        'data':data,
        'aircraft_info': aircraft_info,
        'temp': temp,
        'hum': hum,
        'temp1': temp1,
        'hum1': hum1,
        'std': std,
        'oat': oat,
        'type_': type_,
        'fluid': fluid,
        'water': water,
        'algorithm_choice': algorithm_choice,
        'carrier_list': carrier_list,
        'prediction_result': prediction_result,
    }

    return render(request, 'model.html', context)