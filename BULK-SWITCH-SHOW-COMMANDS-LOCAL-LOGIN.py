###################################################################################################
# For use when you need to log into multpile switches with their own unique local user passwords. #
# Reads a CSV with hostname,password format for each switch                                       #
# CSV Column Headers must be 'Switch' & 'Password', other columns are  ignored                    #
# Written by Patrick Reed                                                                         #
###################################################################################################

from netmiko import ConnectHandler
import csv

########ENABLE THIS LOGGING IF YOU NEED TO TSHOOT
#import logging
#logging.basicConfig(filename='test.log', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")


username = 'local-username'

# Defines Function to Return a dictionary to pass parameters to netmiko
def sw_add(switch, username, password):
    return {'device_type': 'cisco_ios',
            'host': switch,
            'username': username,
            'password': password,
            'secret': password,
            'timeout': 5000.0,
            'session_timeout': 10000.0,
            'session_log_file_mode': 'append',
            'session_log': 'switch.txt', }
# SESSION LOG CREATES A LOG FILE WITH THE SESSION OUTPUT, ONLY IF THE SCRIPT IS SUCESSFUL 

# Reads CSV columns containing hostname,password data
with open('reload-test-sw1-2.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        switch_list = []
        for row in csv_reader:
            if not row['Password']:
                pass
            else:
                switch_list.append(sw_add(row['Switch'], username, row['Password']))
        switch = (row['Switch'])
        password = (row['Password'])

#LOOP TO FORCE SCRIPT TO READ EACH ROW OF THE CSV
for X in switch_list:
    net_connect = ConnectHandler(**X)

#######################################################################################################
#                    EXECUTE IOS COMMANDS: UNCOMMENT THE COMMAND YOU WANT TO USE                      #
#                                                                                                     #
# NOTE: net_connect.send_config_set() Issues commands in Configuration Mode!!!                        #
# NOTE: output = net_connect.send_command should send commands in enable mode if not, try:            #
#                  net_connect.enable()                                                               #
#                  output = net_connect.send_command()                                                #
#                                                                                                     #
# NOTE: Y Variable refers to a dictionary, so it must be defined as a string here                     #
#   to Concatenate with the string containing the Cisco Command using  str(if_add(Y)                  #
#######################################################################################################

    output = net_connect.send_command('show ver | i uptime')
    
    print(output)
