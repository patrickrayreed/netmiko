###################################################################################################
# For use when you need to log into multpile switches with their own unique local user passwords. #
# Reads a CSV with hostname,password format for each switch                                       #
# CSV Column Headers must be 'Switch' & 'Password', other columns are  ignored                    #
# Written by Patrick Reed                                                                         #
###################################################################################################
from netmiko import ConnectHandler
import csv
username = 'local-user'

# Defines Function to Return Interface Number
def if_add(ifnum):
    return ifnum
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

#Reads CSV file
with open('matched.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    switch_list = []
    if_num_list = []
    for row in csv_reader:
       # If Password field is blank, skip row
        if not row['Password']:
            pass
        else:
            
###### Reads CSV columns containing hostname,password data - Populates Switch_List & if_num_list ######
####### NOTE: CSV HEADERS MUST MATCH HERE: 'Switch' & 'Password' ###############
            switch_list.append(sw_add(row['Switch'], username, row['Password']))
            # Reads CSV column containing interface number - Populates List
            if_num_list.append(if_add(row['ifnum']))
#######################################################################################################

###################Loop to Read Row of SSH Creds & Interface Number to issue IOS command against#######
for X, Y in zip(switch_list, if_num_list):
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
##############################################################################################
#                       V  REMOVE PORT SECURITY  V
##############################################################################################
   # output = net_connect.send_config_set(
   #     ['interface ' + str(if_add(Y)), ('shutdown'), ('no switchport port-security maximum 1'),
    #     ('no switchport port-security mac-address sticky'), ('no switchport port-security'), ('no shutdown'),
    #     ('do wr mem')])
##############################################################################################
#                       ^  REMOVE PORT SECURITY  ^
##############################################################################################

### Enter IF config mode & issue command: Switch#(if-cfg)shutdown/no shutdown

    #output = net_connect.send_config_set(['interface '+  str(if_add(Y)),('shutdown')])
    #output = net_connect.send_config_set(['interface ' + str(if_add(Y)), ('no shutdown')])

###Show interface up/down status for each interface in the CSV
    output = net_connect.send_config_set('do sh int ' + str(if_add(Y)) + ' | i ' + str(if_add(Y)))

    print(output)

