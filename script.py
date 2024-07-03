from datetime import datetime

# Open the file in append mode and use 'with' for automatic handling
with open("Calorie_Tracker.txt", "a") as file:
    currentDate = datetime.now().strftime("%A %B %d, %Y - %I:%M %p")
    print(currentDate)
    
    dailyCaloriesConsumed = input("Enter calories consumed today: ")
    dailyCaloriesBurned = input("Enter calories burned today: ")
    
    print("Daily calories consumed: " + dailyCaloriesConsumed)
    print("Daily calories burned: " + dailyCaloriesBurned)
    
    netCalories = int(dailyCaloriesConsumed) - int(dailyCaloriesBurned)
    weightChangeInPounds = netCalories / 3500
    weightChangeInPounds = round(weightChangeInPounds, 2)
    
    # Log the date and results to the file
    file.write(f"{currentDate}\n")
    file.write(f"Calories Consumed: {dailyCaloriesConsumed}, Calories Burned: {dailyCaloriesBurned}\n")
    file.write(f"Weight change: {weightChangeInPounds} pounds\n")
    
    if weightChangeInPounds <= 0:
        file.write(f"Congratulations you lost {weightChangeInPounds} pounds today! Keep going!\n")
    else:
        file.write(f"You gained {weightChangeInPounds} pounds today. Take it easy tomorrow and get more exercise!\n")
