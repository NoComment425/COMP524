from subprocess import Popen, PIPE, STDOUT
import sys, socket, re

INITALIZE_HOSTS = "nmap -sP -PO "
IP_PATTERN = "((?:\d{1,3}\.){3}\d{1,3})"
MAC_ADDRESS_PATTERN = "((?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})"

DB = "localnetwork.db"
DB_TABLE = "localnetwork"

def get_ip_range():
    ip = socket.gethostbyname(socket.gethostname())
    addr = re.match("(\d{1,3}\.){3}", ip)
    if addr:
        print "Local IP address was determined to be:", ip
    else:
        print "Error: Failed to determine machine's local IP address..."
        sys.exit(1)
    return addr.group(0) + "0-255"


def execute_command(cmd):
    try:
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        stdout, stderr = p.communicate(input=None)
        retcode = p.returncode
        if retcode < 0:
            print stdout, stderr, "Error: Child was terminated by signal ", retcode
            sys.exit(1)
    except Exception, e:
        print "Execution failed: ", e
        sys.exit(1)
    return stdout

def get_device_list(ip_range):
    #get list of hosts which are up
    data = execute_command(INITALIZE_HOSTS + ip_range)
    #extract ip/mac address data
    device_list = re.findall(IP_PATTERN+".*?(?:"+MAC_ADDRESS_PATTERN+"|Nmap)", data, re.DOTALL)
    return device_list
    
