# Main eAPI functions
# Import eAPI's JSON RPC LIB
from jsonrpclib import Server

# Basic urlString for all functions
def switchReq(switch, username, password):
    credential = username+ ":" +password+ "@" +switch
    urlString = "http://" +credential+ "/command-api"
    return Server( urlString )

# display switchs' vlans
def show_vlan(switch, username, password):
    switchRun = switchReq(switch,username,password)
    response = switchRun.runCmds(1,["show vlan"])
    result = [str(item) for item in (response[0]["vlans"].keys())]
    return result

# Check if specified VLAN is in switch or not
def check_vlan(switch, username, password, vlans):
    switchRun = switchReq(switch,username,password)
    response = switchRun.runCmds(1,["show vlan"])
    result = response[0]["vlans"].keys()
    if (str(vlans) in result) == True:
        return True
    else:
        return False

# Add VLAN to a switch
def add_vlan(switch, username, password, enable_password, vlans):
    switchRun = switchReq(switch,username,password)
    switchRun.runCmds( 1, [{ "cmd": "enable", "input": enable_password },
                           "configure" , "vlan " +vlans], "json")
    
# Delete VLAN from a switch
def del_vlan(switch, username, password, enable_password, vlans):
    switchRun = switchReq(switch,username,password)
    switchRun.runCmds( 1, [{ "cmd": "enable", "input": enable_password },
                           "configure" , "no vlan " +vlans, "end"], "json")
