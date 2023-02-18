import requests
import threading
from dev_info import *
from urllib3.exceptions import InsecureRequestWarning
import time
start = time.perf_counter()
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def configure_device(xml_payload,**dev_inf):
    with threading.Lock(): # lock used to avoid race condition 
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

def loobackN (xml_payload,**dev_inf):
    with threading.Lock():
        for i in range(1,254):
            xml_payload1= xml_payload.format(name=i,ip_address= i )
            response = requests.patch(
	    url = dev_inf["host"] ,
	    auth = (dev_inf["username"],dev_inf["password"]),
	    headers = dev_inf["headers"],
	    data = xml_payload1 ,
	    verify = False)
            if response.status_code == 204:
             print(" loopback",i," successful",dev_inf["name"])
            else:
             print("Error configuring : " + str(response.status_code) + " " + response.text)


threads = []
dev=["ciscoA","ciscoB","ciscoC","R21","R22","R11"]
for i in dev :
    xml_file_name=str(i)+".xml"
    dic_name=i
    threads.append(threading.Thread(target=configure_device,args=[open(xml_file_name).read()],kwargs=eval(dic_name)))
    threads.append(threading.Thread(target=loobackN,args=[open("loopback.xml").read()],kwargs=eval(dic_name)))

for t in threads:
    print(t,"is started")
    t.start()

# Wait for all the threads to finish
for t in threads:
    print(t,"is waiting to be finishied")
    t.join()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')

# interface gigabitEthernet 2
# shutdown
# interface gigabitEthernet 3
# shutdown
# interface gigabitEthernet 4
# shutdown
# exit
# no router ospf 40
# no router bgp 20
