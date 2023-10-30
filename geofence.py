import math

def haversine(lat1, lon1, lat2, lon2):
    earth_radius = 6371000
    
    #convert lat and lon to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    #Haversine Formular
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2 ) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    #distance for fence
    distance = earth_radius * c
    
    return distance

def inside_geofence(lat1, lon1, geofence_lat, geofence_lon, radius):
    
    distance = haversine(lat1, lon1, geofence_lat, geofence_lon)
    
    return distance <= radius



