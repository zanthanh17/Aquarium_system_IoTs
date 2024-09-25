import urequests
import ntptime
import time
import sensor.turbidity as TUR
import sensor.Temp as Temp
import sensor.PH as ph


ntptime.host = 'pool.ntp.org'  # Use this or another known NTP server

server_url = 'https://script.google.com/macros/s/AKfycbwEBDMV7npCrkxAaN1BUHYQaHLqwUZRsOI8U5uhgOT5i89fABizurx9U6Zq6vz7RizY/exec'

def get_ntp_time():
    try:
        ntptime.settime()  # Synchronize the system time with NTP
        tm = time.localtime(time.time())  # Get local time
        formatted_time = "{:02d}:{:02d}:{:02d}".format(tm[3], tm[4], tm[5])
        return formatted_time
    except Exception as e:
        print("Error getting NTP time:", e)
        return None
    
def get_data():
    NTU = TUR.read_turbidity()
    phValue = ph.read_ph() 
    # temp = Temp.read_temperature()

    timestamp = get_ntp_time()
    # Prepare JSON payload
    json_data = {
        "method": "append",
        # "temp": temp,
        "NTU": NTU,
        "phValue": phValue,
        "timestamp": timestamp,
    }
    # Send HTTP POST request
    try:
        response = urequests.post(server_url, json=json_data)
        print("Response:", response.status_code, response.text)
        response.close()
    except Exception as e:
        print("Error sending data:", e)