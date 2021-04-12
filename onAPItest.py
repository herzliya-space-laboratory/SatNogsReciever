import requests
import os
import datetime
import socket
import threading

global last_packet_time, api_page


def name():
    global last_packet_time,api_page
    print("name test")
    if check_for_file('last_packet.txt'):
        with open("last_packet.txt","r") as last_packet_file:
            last_packet_time = last_packet_file.read()
    else:
        last_packet_time = None
        api_page = None


def write_to_file(file_name, mode, text):
    with open(file_name, mode) as file:
        file.write(text)


def connect_to_endnode():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 3211))
    s.listen(2)
    conn,addr = s.accept()
    return conn


def check(give_date,conn,norad_id):
    global api_page,last_packet_time
    date = datetime.datetime.strptime(give_date, "%Y-%m-%d %H:%M:%S")
    page_number = 1
    try:
        while True:
            try:
                api_page = requests.get(f"https://db.satnogs.org/api/telemetry/?satellite={norad_id}&page={page_number}",headers={'Authorization': 'Token 460d9df5d3d516a3ecb9964d8c54f6fd31301e3a'})
            except:
                return
            if len(api_page.json()) == 1:
                if dict(api_page.json())["detail"] == "Invalid page.":
                    return
                
            for packet in range(0,len(list(api_page.json()))):
                print(f"page number:{page_number}")
                time = str(dict(api_page.json()[packet]).get("timestamp"))
                packet_date = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
                if packet_date >= date:
                    data_packet = str(dict(api_page.json()[packet]).get("frame"))
                    write_to_file("log.txt", "a", data_packet+"\n")
                    conn.send(bytes.fromhex(data_packet))
                    print("[+]the packet have been writed to file")
                else:
                    print("[-]The packet is not Okay.")
                    return
            page_number += 1
    except:
        print("yafe")


def check_for_file(cfile):
    files = []
    for roots, dirs, file in os.walk(os.getcwd()):
        for i in file:
                files.append(i)
        if cfile in files:
            return True
        else:
            return False


"""def download_packets(conn,norad_id):
    global api_page,last_packet_time
    api_page = None

    print("[+]start running")

    while True:
        api_page = requests.get(f"https://db.satnogs.org/api/telemetry/?satellite={norad_id}",headers={'Authorization': 'Token 460d9df5d3d516a3ecb9964d8c54f6fd31301e3a'})
        api_page = api_page.json()
        for i in range(len(api_page)-1):
            packet_data = api_page[i]
            packet_time = datetime.datetime.strptime(str(packet_data.get("timestamp")), "%Y-%m-%dT%H:%M:%SZ")
            write_to_file("last_packet.txt","w", f"{str(packet_time)}")
            write_to_file("log.txt","w", f"{packet_data["frame"]}")

        while packet_time != last_packet_time:
            api_page = requests.get(f"https://db.satnogs.org/api/telemetry/?satellite={norad_id}",headers={'Authorization': 'Token aee279123330eaef48d0ee5920c02e760fff5132'})

            #api_page = dict(api_page.json()[0])
            telemetry = packet_data["frame"]  #this is the hex
            ptime = packet_data.get("timestamp")
            time = str(packet_data.get("timestamp"))
            conn.send(bytes.fromhex(telemetry))
            write_to_file("log.txt", 'a', f"\n{ptime}\n{telemetry}")
            last_packet_time = datetime.datetime.strptime(ptime, "%Y-%m-%dT%H:%M:%SZ")
            print("A new packet have been writed to file")
            write_to_file("last_packet.txt", "w", f"{str(last_packet_time)}")

        write_to_file("last_packet.txt", "w", f"{str(last_packet_time)}")
"""
def return_packet_time(packet):
    return datetime.datetime.strptime(packet, "%Y-%m-%dT%H:%M:%SZ")

def get_packets_page(norad_id):
    return requests.get(f"https://db.satnogs.org/api/telemetry/?satellite={norad_id}",headers={'Authorization': 'Token 460d9df5d3d516a3ecb9964d8c54f6fd31301e3a'}).json()

def get_packet_element(packet, element):
    return packet[element]


def check_if_last_packet():
    try:
        with open("last_packet.txt", "r") as fin:
            return return_packet_time(fin.read())
    
    except:
        return False


def extract_packet_data(packet):
    return packet["timestamp"], packet["frame"]


def download_packets(conn, norad_id):
    global api_page,last_packet_time
    api_page = None
    last_packet_time = check_if_last_packet()

    print("[+]start running")

    while True:
            api_page = get_packets_page(norad_id)
            if last_packet_time == False:
                last_packet_time = datetime.datetime(1970, 1, 1, 1, 1, 1, 1)

            for i in api_page:
                packet_time = return_packet_time(i["timestamp"])
                #print(f"packet time:{packet_time}\nlast packet time:{last_packet_time}\n{packet_time > last_packet_time}")
                print("last packet",last_packet_time, "next packet:",packet_time)
                if (packet_time > last_packet_time):
                    print("[+]last packet",last_packet_time, "next packet:",packet_time)
                    ptime, telemetry = extract_packet_data(i)
                    ptime = return_packet_time(ptime)
                    conn.send(bytes.fromhex(telemetry))
                    write_to_file("log.txt", 'a', f"\n{str(ptime)}\n{telemetry}")
                    last_packet_time = ptime
                    print("A new packet have been writed to file")
                    write_to_file("last_packet.txt", "w", f"{str(last_packet_time)}")


   # write_to_file("last_packet.txt", "w", f"{str(last_packet_time)}")

def main():
    duchifat_3_norad = 30776
    #duchifat_1_norad = 40021
    conn = connect_to_endnode()
    name()
    print("test")
    if check_for_file('log.txt'):
        with open('last_packet.txt', 'r') as data_read:
            data_file = data_read.read()
            if len(list(data_file)) > 8:
                check(data_file, conn,duchifat_3_norad)
                #check(data_file,conn,duchifat_1_norad)
            download_packets(conn,duchifat_3_norad)
            #download_packets_thread = threading.Thread(target=download_packets)
            #download_packets_thread.start()
    else:
        date = input("Enter the full date including hours in this form yyyy-mm-dd hh:mm:ss</>")
        check(date, conn,duchifat_3_norad)
        #check(date,conn,duchifat_1_norad)
        #------------------------------------#
        download_packets(conn,duchifat_3_norad)
        #download_duchi1_packets_thread = threading.Thread(target=download_packets,args=(conn,duchifat_1_norad))
        #download_duchi1_packets_thread.start()


if __name__ == '__main__':
    print("test")
    main()
