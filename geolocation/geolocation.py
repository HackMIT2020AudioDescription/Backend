import socket  
import ipinfo
access_token= 'e987e3fa6c6b87'
handler = ipinfo.getHandler(access_token)


def get_location():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname) 
    details = handler.getDetails(IPAddr)
    print(details.city)
    return (details.city)
