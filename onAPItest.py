import requests
import os
import datetime
import socket


class Glouton:
    def __init__(self):
        if self.check_for_file('last_packet.txt'):
            with open("last_packet.txt","r") as last_packet_file:
                self.last_packet_time = last_packet_file.read()
        else:
            self.last_packet_time = None
        self.api_page = None


    #def connect_to_endnode(self):
     #   ip = "127.0.0.1"
     #   port = 61616
     #   s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     #   s.bind((ip,port))
     #   s.listen(2)
     #   conn,addr = s.accept()
     #   return conn


    #def send_packets_to_endnode(self,conn,packet):
        #conn.send(packet)

    def check(self, give_date):
        date = datetime.datetime.strptime(give_date, "%Y-%m-%d %H:%M:%S")
        self.api_page = requests.get("https://db.satnogs.org/api/telemetry/?satellite=44854", headers={'Authorization': 'Token 460d9df5d3d516a3ecb9964d8c54f6fd31301e3a'})
        for packet in range(0,len(list(self.api_page.json()))):
            time = str(dict(self.api_page.json()[packet]).get("timestamp"))
            packet_date = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
            if packet_date >= date:
                data_packet = str(dict(self.api_page.json()[packet]).get("frame"))
                with open("log.txt","a") as data_file:
                    data_file.write(data_packet+"\n")
                print("[+]writed to the file")
            else:
                print("[-]The packet is not Okay.")
                print(packet_date)
                return


    def check_for_file(self,cfile):
        files = []
        for roots, dirs, file in os.walk(os.getcwd()):
            for i in file:
                files.append(i)
        if cfile in files:
            #check this
            return True
        else:
            return False

    def download_packets(self):
        #self.api_page = api_page = requests.get("https://db.satnogs.org/api/telemetry/?satellite=44854", headers={'Authorization': 'Token 460d9df5d3d516a3ecb9964d8c54f6fd31301e3a'})
        #self.api_page = api_page.json()[0]
        print("[+]start running")
        #conn = self.connect_to_endnode()
        while True:
            self.api_page = api_page = requests.get("https://db.satnogs.org/api/telemetry/?satellite=44854", headers={'Authorization': 'Token 460d9df5d3d516a3ecb9964d8c54f6fd31301e3a'})
            self.api_page = api_page.json()[0]
            packet_time = datetime.datetime.strptime(str(dict(self.api_page).get("timestamp")), "%Y-%m-%dT%H:%M:%SZ")
            while packet_time != self.last_packet_time:
                self.api_page = requests.get("https://db.satnogs.org/api/telemetry/?satellite=44854", headers={'Authorization': 'Token 460d9df5d3d516a3ecb9964d8c54f6fd31301e3a'})
                self.api_page = dict(self.api_page.json()[0])
                telemetry = self.api_page["frame"]  #this is the hex
                ptime = self.api_page.get("timestamp")
                time = str(self.api_page.get("timestamp"))
                packet_date = datetime.datetime.strptime(time,'%Y-%m-%dT%H:%M:%SZ')
                #print(f"new_packet_time<{datetime.datetime.now()}>:{list_of_telemetry}\r")
                with open('log.txt','a') as log:
                    log.write(f"\n{ptime}\n{telemetry}")
                self.last_packet_time = datetime.datetime.strptime(ptime, "%Y-%m-%dT%H:%M:%SZ")
                print("A new packet have been writed to file")
                #self.send_packets_to_endnode(conn,telemetry)
                with open('last_packet.txt','w') as last_packet_file:
                    last_packet_file.write(f'{str(self.last_packet_time)}')
                print("GitSDFGHJKL")
            with open('last_packet.txt','w') as last_packet_file:
                last_packet_file.write(f'{str(self.last_packet_time)}')

    def main(self):
        if self.check_for_file('log.txt'):
            with open('last_packet.txt', 'r') as data_read:
                data_file = data_read.read()
                if len(list(data_file)) > 8:
                    print(data_file)
                    self.check(data_file)
            self.download_packets()
        else:
            date = input("Enter the full date including hours in this form yyyy-mm-dd hh:mm:ss</>")
            self.check(date)
            #------------------------------------#
            self.download_packets()


if __name__ == '__main__':
    glouton = Glouton()
    glouton.main()

