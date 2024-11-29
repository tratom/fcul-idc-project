import datetime
from config import get_users_data, count_activities_by_filter

def mesure_burned_calories(body_weight,velocity,height,coeff):
    res = 0.035*body_weight + velocity*velocity/height *0.029*body_weight
    return  round(res * coeff, 2)

def mesure_velocity(is_male,age,is_running):
    if(is_male):
        if (age < 29):
            velocity =  (1.36)
        elif(age <39):
            velocity = (1.43)
        elif(age <49):
            velocity = (1.43)    
        elif(age <59):
            velocity = (1.43)   
        elif(age <69):
            velocity = (1.34)       
        elif(age <79):
            velocity = (1.26)  
        else:
            velocity = (0.97)
    else:
        if (age < 29):
            velocity = (1.34)
        elif(age <39):
            velocity = (1.34)
        elif(age <49):
            velocity = (1.39)    
        elif(age <59):
            velocity = (1.31)   
        elif(age <69):
            velocity = (1.24)       
        elif(age <79):
            velocity = (1.13)  
        else:
            velocity = (0.94)
    if(is_running):
        return velocity*2
    else :
        return velocity

def calculate_duration_and_calories(current_date,is_running):
    # Get the user personal data
    users = get_users_data()[0]
    is_male = users[2]
    age = users[1]
    weight = users[3]
    height = users[4]
    threshold_running = users[5]
    threshold_walking = users[6]

    # Calculate the user velocity
    velocity_running = mesure_velocity(is_male,age,True)
    velocity_walking = mesure_velocity(is_male,age,True)

    # Get the user activity
    day_counts = count_activities_by_filter(current_date, filter_type='day')
    month_counts = count_activities_by_filter(current_date, filter_type='month')
    week_counts = count_activities_by_filter(current_date, filter_type='week')

    # Get the calories burned
    calories_day = mesure_burned_calories(weight,velocity_running,height,day_counts['running']) + mesure_burned_calories(weight,velocity_walking,height,day_counts['walking'])
    calories_week = mesure_burned_calories(weight,velocity_running,height,week_counts['running']) + mesure_burned_calories(weight,velocity_walking,height,week_counts['walking'])
    calories_month = mesure_burned_calories(weight,velocity_running,height,month_counts['running']) + mesure_burned_calories(weight,velocity_walking,height,month_counts['walking'])

    # Calculate the threshold percent
    walking_threshold_percent = day_counts['walking']/threshold_walking*100
    running_threshold_percent = day_counts['running']/threshold_running*100

    # Send a message to the user interface
    message = {
        "time_day_run": day_counts['running'],
        "time_day_walk": day_counts['walking'],
        "time_week_run": week_counts['running'],
        "time_week_walk": week_counts['walking'],
        "time_months_run": month_counts['running'],
        "time_months_walk": month_counts['walking'],
        "calories_day": calories_day,
        "calories_week": calories_week,
        "calories_month": calories_month,
        "walking_threshold_percent": round(walking_threshold_percent, 2),
        "running_threshold_percent": round(running_threshold_percent, 2),
        "is_running": is_running
    }

    return (message)