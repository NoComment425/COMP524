from collect_data import get_device_list, get_ip_range, DB, DB_TABLE
from operator import itemgetter
from alert_window import AlertWindow
from PyQt4.QtGui import QApplication
import sqlite3, re, sys


def compare_lists(cursor, curr, prev):
    
    msg = ""
    #compare two device lists to determine any differences
    i = j = 0
    c_len = len(curr)
    p_len = len(prev)
    while i < c_len or j < p_len:
        if i < c_len and j < p_len: #compare elements
            if curr[i][1] == prev[j][1]: #mac addresses match
                if curr[i][0] != prev[j][0]: #check ip address field
                    msg = msg +"Device IP change...\n\tMAC: "+curr[i][1]+"\n\tPrevious IP: "+prev[j][0]+"\n\tCurrent IP: "+curr[i][0]+"\n"
                    cursor.execute("UPDATE "+DB_TABLE+" SET ip = '"+curr[i][0]+"' WHERE mac = '"+prev[i][1]+"'")
                j = j + 1
                i = i + 1
            elif curr[i][1] > prev[j][1]:
                msg = msg +"Device left...\n\tMAC: "+prev[j][1]+"\n\tIP: "+prev[j][0]+"\n"
                cursor.execute("DELETE FROM "+DB_TABLE+" WHERE mac = '"+prev[j][1]+"'")
                j = j + 1
            elif curr[i][1] < prev[j][1]:
                msg = msg +"New device...\n\tMAC: "+curr[i][1]+"\n\tIP: "+curr[i][0]+"\n"
                cursor.execute("INSERT INTO "+DB_TABLE+" VALUES (?, ?)", curr[i])
                i = i + 1
            else:
                print "error- should never execute"
                sys.exit(1)
        elif i < c_len and j >= p_len: #current device list has more entries
            msg = msg +"New device...\n\tMAC: "+curr[i][1]+"\n\tIP: "+curr[i][0]+"\n"
            cursor.execute("INSERT INTO "+DB_TABLE+" VALUES (?, ?)", curr[i])
            i = i + 1
        elif i >= c_len and j < p_len: #previous device list has more entries
            msg = msg +"Device left...\n\tMAC: "+prev[j][1]+"\n\tIP: "+prev[j][0]+"\n"
            cursor.execute("DELETE FROM "+DB_TABLE+" WHERE mac = '"+prev[j][1]+"'")
            j = j + 1
        else:
            print "error- should never execute!!"
            sys.exit(1)
    msg  = str(j)+" device(s) previously in network.\n"+str(i)+" device(s) currently in network.\n\n"+msg
    return msg


try:
    #check if ip range specified
    if len(sys.argv) > 1:
        print "IP range specified."
        ip_range = ' '.join(sys.argv[1:len(sys.argv)])
    else:
        print "No IP range specified.  Using default network interface."
        ip_range = get_ip_range()
        
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    #create database on first run
    cursor.execute("CREATE TABLE IF NOT EXISTS "+DB_TABLE+ " (ip VARCHAR(50), mac VARCHAR(50) primary key)")

    print "Gathering network information...\n"
    #sort by mac address
    current_devices = sorted(get_device_list(ip_range), key=itemgetter(1))

    cursor.execute('SELECT * FROM '+DB_TABLE+' order by mac asc')
    previous_devices =  cursor.fetchall()

    if previous_devices != current_devices:
        print "\tThe network has changed.\n"
        alert_text = compare_lists(cursor, current_devices, previous_devices)
        print alert_text

        #save any modifications to database
        conn.commit()

        #display alert window
        app = QApplication(sys.argv)
        window = AlertWindow()
        window.setup("Network alert", alert_text)
        window.show()
        sys.exit(app.exec_())
    
    else:
        print "\tNo difference in network.\n"

finally:
    print "Closing connections..."
    #close connections
    cursor.close()
    conn.close()
    print "Finished!"


