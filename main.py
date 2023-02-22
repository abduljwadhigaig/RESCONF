import requests
import threading
from dev_info import *
import time
start = time.perf_counter()
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def configure_device(xml_payload,**dev_inf):
    response = requests.patch(
	url = dev_inf["host"] ,
	auth = (dev_inf["username"],dev_inf["password"]),
	headers = dev_inf["headers"],
	data = xml_payload ,
	verify = False)
    if response.status_code == 204:
        print(" configuration successful",dev_inf["name"])
    else:
        print("Error configuring : " + str(response.status_code) + " " + response.text)


threads = []
dev=["ciscoA","ciscoB","ciscoC","R21","R22","R11"]
for i in dev :
    xml_file_name=str(i)+".xml"
    dic_name=i
    threads.append(threading.Thread(target=configure_device,args=[open(xml_file_name).read()],kwargs=eval(dic_name)))

for t in threads:
    t.start()

# Wait for all the threads to finish
for t in threads:
    t.join()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')


