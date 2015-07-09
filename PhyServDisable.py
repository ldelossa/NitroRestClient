import sys
import os
from bin import NitroRestClient



# Script should be passed 4 arguments
# [strings]: netscalerIP, username, password, servername

# Check to see that 4 items were passed in, remove script name from arguments
# print (os.path.basename(__file__))
sys.argv.remove(os.path.basename(__file__))
# print sys.argv
# print len(sys.argv)
if len(sys.argv) != 4:
    print ("Please provide the following arguments(strings): netscalerip, username, password, servername")
    sys.exit(1)


# Parse out arguments
netscalerip = sys.argv[0]
username = sys.argv[1]
password = sys.argv[2]
servername = sys.argv[3]


# Attempt instantiation of NitroRestClient
try:
    Client = NitroRestClient.NitroRestClient(netscalerip, username, password)
except:
    print "Couldn't create Nitro Session, check username and password and network connectivity"
    sys.exit(1)

#Check servername for validity

try:
    normalizedservername = Client.servernamecheck(servername)
except ValueError, e:
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
        print normalizedservername + " No longer has connections"
        break
sys.exit(0)
