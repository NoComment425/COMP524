from collect_data import execute_command
import sys
from time import sleep
from datetime import datetime

SLEEP_TIME = 900 #15 minutes (900 seconds)

try:
        if len(sys.argv) > 1:
                params = ' '.join(sys.argv[1:len(sys.argv)])
                print "daemon: parameters included:",params
        else:
                print "daemon: No parameters included."
                params = ''

        while(True): 
                print "daemon: "+str(datetime.today())
                print execute_command("python network_diff.py "+params)
                print "daemon: sleeping for",SLEEP_TIME, "seconds.\n"
                sleep(SLEEP_TIME)
except Exception, e:
        print "Error:",e
