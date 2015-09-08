import sys
from bin import NitroRestClient
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("netscalerip", help="The IP address of the netscaler appliance")
parser.add_argument("username", help="Username of service account")
parser.add_argument("password", help="Password of service account")
parser.add_argument("servername", help="The server's name in which you'd like to disable")
args = parser.parse_args()


# Attempt instantiation of NitroRestClient
try:
    Client = NitroRestClient.NitroRestClient(args.netscalerip, args.username, args.password)
except:
    print("Couldn't create Nitro Session, check username and password and network connectivity")
    sys.exit(1)

#Check servername for validity

try:
    normalizedservername = Client.servernamecheck(args.servername)
except ValueError as e:
    print("Invalid server name was provided. Please check server name and try again.")
    sys.exit(2)

# normalizedservername = Client.servernamecheck(servername)
# if normalizedservername is None:
#     print("Server name is invalid")
#     sys.exit(2)

# gracefully disable server
Client.disablephysicalserver(normalizedservername)


# Main logic, creates on the fly generator comprehension, if all are true break, if any are false continue loop.
while True:
    ServerStats = Client.getmemberserverstatsbyserver(normalizedservername)

    print("looping")

    if all(ServerStat['curclntconnections'] == '0' and
           ServerStat['cursrvrconnections'] == '0' and
           ServerStat['svrestablishedconn'] == '0'
           for ServerStat in ServerStats):
        print(normalizedservername + " No longer has connections")
        break
sys.exit(0)
