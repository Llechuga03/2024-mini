import network
from machine import Pin
import time
import random
import json
import urequests  

N = 10  
on_ms = 500  

wific = 'Apt214'
wifi_pass = 'Apt214123'


conc = network.WLAN(network.STA_IF)
conc.active(True)
conc.connect(wific, wifi_pass)

timeout = 10  
start_time = time.time()
while not conc.isconnected():
    if time.time() - start_time > timeout:
        print("Could not connect to Wi-Fi")
        break
    time.sleep(1)

url_link= "https://ec463-74dcf-default-rtdb.firebaseio.com/response_times.json"

def random_time_interval(tmin: float, tmax: float) -> float:
    return random.uniform(tmin, tmax)

def blinker(led: Pin, times: int):
    for _ in range(times):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)

def write_json(json_filename: str, data: dict):
    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(times: list):
    t_good= [x for x in times if x is not None]  
   
    if t_good:
        mini= min(t_good)
        maxi= max(t_good)
        avg= sum(t_good) / len(t_good)
    else:
        mini= maxi= avg= None

   
    data = {
        "minimum time:": mini,
        "maximum time:": maxi,
        "average time:": avg,
        "misses:": times.count(None),
        "num of flashes:": len(times),
        "successful presses:": len(t_good),
        "score:": len(t_good) / len(times) if times else 0
    }

   
    cur= time.localtime()
    curt= "-".join(map(str,cur[:3])) +"T"+ "_".join(map(str, cur[3:6]))
    fil= f"response_times_{curt}.json"
    write_json(fil,data)
   
    return data  


def upload_to_cloud(data: dict):
    try:
        r1 = urequests.post(url_link, json=data)
        print("status code:", r1.status_code)
        print("text:", r1.text)
        r1.close()  
    except OSError as e:
        print("wifi error:", str(e))
    except ValueError as e:
        print("Data error:", str(e))
    except Exception as e:
        print("didnt upload:", str(e))

if __name__ == "__main__":
    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)
   
    t2 = []

    blinker(led, 3)  

    for _ in range(N):
        time.sleep(random_time_interval(0.5, 5.0))  

        led.high()
        tic = time.ticks_ms()
        t0 = None

       
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:  
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
       
        t2.append(t0)
        led.low()

    blinker(led, 5)

   
    data= scorer(t2)
    print(f"saved in the json file.")

   
    upload_to_cloud(data)
