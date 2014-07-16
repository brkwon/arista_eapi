# Arista EAPI caller main program
# 2014-07 by boram.kwon@kt.com

from modules.arista_eapi_urllib2 import *
from modules.check_ip import ip_address_is_valid

print ("Arista eAPI controller program v0.1, using urllib2")

# Gather Credentials
username = raw_input("\nPlease enter username = ")
password = raw_input("Please enter password = ")
enable_password = raw_input("Please enter enable password = ")

# Gather Switch IP Addresses
print ("\nPlease add switch IP addresses (in dotted decimal please).")

# Init list for storing switch IPs
switches = []

# Check if user_input is correct IP address.
# If IP is valid, append it to the switch list.
while True:
    switch = raw_input("Switch IP ('end' to finish') = ")
    if switch == "end":
        break
    if ip_address_is_valid(switch) == False:
        print ("Your input \' " +switch+ "\' is invalid IP")
        continue
    switches.append(switch)

# Print out all the VLANs from switches
print
for switch in switches:
    print("Your Switch " +switch+ "has following VLANS") 
    print(show_vlan(switch, username, password))


# Check if user like to add/delete VLAN 
answer = raw_input("\nWould you like to add/delete VLANs to above switches? (y/n) = ")

if answer == "y":
    for switch in switches:
        print("\nYour Switch " +switch+ " has following VLANs")
        print(show_vlan(switch, username, password))
        
        while True:
            vlans = raw_input("\nEnter VLAN (2-4094), else enter 'end' to finish = ")

            if vlans.isdigit() == True and 1 < int(vlans) < 4095:
                if check_vlan(switch, username, password, vlans) == True:
                    answer = raw_input("Delete VLAN " +vlans+ "? (y/n) = ")
                    if answer == 'y':
                        del_vlan(switch, username, password, enable_password, vlans)
                        print("\nYour Switch " +switch+ " has following VLANs")
                        print(show_vlan(switch, username, password))        
                else:
                    answer = raw_input("Add VLAN " +vlans+ "? (y/n) = ")
                    if answer == 'y':
                        add_vlan(switch, username, password, enable_password, vlans) 
                        print("\nYour Switch " +switch+ " has following VLANs")
                        print(show_vlan(switch, username, password))          
            elif vlans == "end":
                break
            else:
                print("Please enter integer between 2 to 4094, else enter 'end' to finish.\n")

print("\n*** Script Finished ***")




