import math

# Calculate the Euclidean distance between the vehicle and an object
def calculate_distance(vehicle_x, vehicle_y, object_x, object_y):
    dx = vehicle_x - object_x
    dy = vehicle_y - object_y
    distance = math.sqrt(dx**2 + dy**2)
    return distance

# Example usage:
vehicle_x = 0
vehicle_y = 0
object_x = 3
object_y = 4

distance = calculate_distance(vehicle_x, vehicle_y, object_x, object_y)
print("Distance:", distance)
