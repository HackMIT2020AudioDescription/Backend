#pip install -U googlemaps
#pip install ipinfo


import socket  
import ipinfo
import googlemaps



access_token= 'e987e3fa6c6b87'
handler = ipinfo.getHandler(access_token)


def get_location():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname) 
    details = handler.getDetails(IPAddr)
    lat,long= details.latitude, details.longitude
    #TimeZone= details.Timezone()
    city= details.city
    gmaps = googlemaps.Client(key='AIzaSyD9zSrMqSoG4L6BkT-6eH5-XOiv5lfwJTU')
    reverse_geocode_result = gmaps.reverse_geocode((lat, long))
    address= reverse_geocode_result[0]['formatted_address']
    return city, address




get_location()