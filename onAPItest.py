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

    def check(self, give_date):
        date = datetime.datetime.strptime(give_date, "%Y-%m-%d %H:%M:%S")
        self.api_page = requests.get("https://db.satnogs.org/api/telemetry/?satellite=44854", headers={'Authorization': 'Token 460d9df5d3d516a3ecb9964d8c54f6fd31301e3a'})
        for packet in range(0,len(list(self.api_page.json()))):
            time = str(dict(self.api_page.json()[packet]).get("timestamp"))
            packet_date = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
            if packet_date >= date:
                with open("log.txt","w") as datafile:
                    datafile.write(str(dict(self.api_page.json()[packet]).get("frame")))

                print("[+]writed to the file")
            else:
                print("[-]The packet is not Okay.")
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

    #def connect_to_endnode(self):
        #ip_addr = "127.0.0.1"
        #port = 61016
        #s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #s.bind((ip_addr,port))
        #s.listen(2)
        #conn,addr = s.accept()
        #return conn

    #def send_packet_to_endnode(self,conn,packet):
        #conn.send(bytes.fromhex(packet))

    def download_packets(self):
        self.api_page = api_page = requests.get("https://db.satnogs.org/api/telemetry/?satellite=44854", headers={'Authorization': 'Token 460d9df5d3d516a3ecb9964d8c54f6fd31301e3a'})
        self.api_page = api_page.json()[0]
        #conn = self.connect_to_endnode()
        print("[+]start running")

        while True:
            packet_time = datetime.datetime.strptime(str(dict(self.api_page).get("timestamp")), "%Y-%m-%dT%H:%M:%SZ")
            while packet_time != self.last_packet_time:
                self.api_page = requests.get("https://db.satnogs.org/api/telemetry/?satellite=44854", headers={'Authorization': 'Token 460d9df5d3d516a3ecb9964d8c54f6fd31301e3a'})
                self.api_page = dict(self.api_page.json()[0])
                telemetry = self.api_page["frame"]  #this is the hex
                ptime = self.api_page.get("timestamp")
                time = str(self.api_page.get("timestamp"))
                packet_date = datetime.datetime.strptime(time,'%Y-%m-%dT%H:%M:%SZ')
                #print(f"new_packet_time<{datetime.datetime.now()}>:{list_of_telemetry}\r")
                #self.send_packet_to_endnode(conn,telemetry)
                with open('log.txt','a') as log:
                    log.write(f"\n{ptime}\n{telemetry}")
                self.last_packet_time = datetime.datetime.strptime(ptime, "%Y-%m-%dT%H:%M:%SZ")
                print("A new packet have been writed to file")
                with open('last_packet.txt','w') as last_packet_file:
                    last_packet_file.write(f'{str(self.last_packet_time)}')

            with open('last_packet.txt','w') as last_packet_file:
                last_packet_file.write(f'{str(self.last_packet_time)}')

    def main(self):
        if self.check_for_file('log.txt'):
            with open('last_packet.txt','r') as fread:
                if len(list(fread.read())) > 8:
                    #print(fread.read())
                    self.check(fread.read())
            self.download_packets()
        else:
            date = input("Enter the full date including hours in this form yyyy-mm-dd hh:mm:ss</>")
            self.check(date)
            #------------------------------------#
            self.download_packets()


if __name__ == '__main__':
    glouton = Glouton()
    glouton.main()
