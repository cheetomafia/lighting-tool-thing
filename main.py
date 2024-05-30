import socket
import csv
import time

from pythonosc import udp_client

createCueString = "$ Record Cue {cuenumber} \r"

UDP_IP = "192.168.0.137"
UDP_PORT = 2000
UDP_PORT_OSC = 2002

oscClient = udp_client.SimpleUDPClient(UDP_IP, UDP_PORT_OSC)
sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
lightCuesFile = open("lightcues.csv", "r", encoding="utf-8")

reader = csv.DictReader(lightCuesFile, delimiter=',')

commands = []
oscCommands = []

# Parse row
for row in reader:
    cmd = createCueString.format(cuenumber=row['Cue #'])
    commands.append(cmd)

    if row['Name'] != "":
        oscCmd = ("/eos/set/cue/1/{cuenumber}/label".format(cuenumber=row['Cue #']), row['Name'])
        oscCommands.append(oscCmd)

    if row['Other Notes'] != "":
        oscCmd = ("/eos/set/cue/1/{cuenumber}/notes".format(cuenumber=row['Cue #']), row['Other Notes'])
        oscCommands.append(oscCmd)

    if row['Scene Name'] != "":
        oscCmd = ("/eos/set/cue/1/{cuenumber}/scene".format(cuenumber=row['Cue #']), row['Scene Name'])
        oscCommands.append(oscCmd)
		
# Cue creation commands
for command in commands:
    sock.sendto(bytes(command.encode("utf-8")), (UDP_IP, UDP_PORT))
    time.sleep(0.005)

print("Created cues.")
	
# Cue detail commands
for cmd in oscCommands:
    oscClient.send_message(cmd[0], cmd[1])
    time.sleep(0.005)
	
print("Created cue details.")

