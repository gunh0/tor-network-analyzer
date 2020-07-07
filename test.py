import sys,os

thread_list = []
print(os.getcwd())
ip_list = []
onion_list = []
print("Now Start Program...\n")
machine = int(input("Select VM Machine PC : 1. 100 , 2. 200 , 3. GCP \n"))

if machine == 1 or machine == 2:
    start_ip = int(input("Start IP : \n"))  # (change)
    last_ip = int(input(" Last IP : \n"))  # (change)

    for i in range(last_ip - start_ip + 1):  # (change)
        input_ip = "192.168.160." + str(start_ip)  # (change)
        start_ip = start_ip + 1  # (change)
        print(input_ip)  # (change)
        ip_list.append(input_ip)  # (change)
