import os

ips = {
    "192.168.0.81":"Martin's PC",
    "192.168.0.91":"Matthew's iPad",
    "192.168.0.76":"[?] Martin's Galaxy S5",
    "192.168.0.49":"s5bedroom",
    "192.168.0.71":"[?] Galaxy",
    "192.168.0.85":"Matthew's LG-G5",
    "192.168.0.40":"Marcus's S9+",
}

numbers = {
    'matthew':os.getenv("phone_matthew"), # twilio verified
    'marcus':os.getenv("phone_marcus"), # twilio verified
}