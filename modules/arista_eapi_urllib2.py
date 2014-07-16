# EAPI call program using urllib2 and json

import urllib2
#import random
import json

# eAPI JSON template 
enableCmd = {"input" : "test", "cmd" : "enable"}
jsonCmd = {"params" : {"format" : "json", "version" : 1, "cmds" : "command"}, "jsonrpc" : "2.0", "method" : "runCmds", "id" : 0}

# Create json based on enable_password and eAPI command
def jsonCreate(eapi_command, enable_password):
    if enable_password == None:
        jsonCmd["params"]["cmds"] = [eapi_command]
        return jsonCmd
    else:
        enableCmd["input"] = enable_password
        jsonCmd["params"]["cmds"] = [enableCmd] + eapi_command
        print(jsonCmd)
        return jsonCmd

# HTTP REST request function for eAPI call 
def switchReq(switch, username, password, jsonCmds):
    urlString = "http://{}/command-api".format(switch)
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, urlString, username, password)
    
    # create an authenticate hander, opener and install opener
    auth = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth)
    urllib2.install_opener(opener)
   
    # create request call
    request = urllib2.Request(urlString, jsonCmds)
    request.add_header("Content-type", "application/json")
        
    # call switch via urillib2, and close ti
    f = urllib2.urlopen(request)
    response = f.read()
    f.close()

    return response

# Add VLAN to a switch
def show_vlan(switch, username, password):
    # Create JSON eapi-command
    json_data = jsonCreate("show vlan", None)
    jsonCmds = json.dumps(json_data)

    # Send JSON command to the switch
    response = switchReq(switch, username, password, jsonCmds)

    # Strip VLAN ids for return
    json_string = json.loads(response)
    result = [str(item) for item in (json_string['result'][0]['vlans'].keys())]
    
    return result

# Check if specified VLAN is in switch or not
def check_vlan(switch, username, password, vlans):
    # Create JSON eapi-command
    json_data = jsonCreate("show vlan", None)
    jsonCmds = json.dumps(json_data)

    # Send JSON command to the switch
    response = switchReq(switch, username, password, jsonCmds)

    # Strip VLAN ids for checkup
    json_string = json.loads(response)
    result = [str(item) for item in (json_string['result'][0]['vlans'].keys())] 
    
    if (str(vlans) in result) == True:
        return True
    else:
        return False

# Add VLAN to a switch
def add_vlan(switch, username, password, enable_password, vlans):
    eapi_command = ["configure", "vlan " +vlans]
    json_data = jsonCreate(eapi_command, enable_password)
    jsonCmds = json.dumps(json_data)

    response = switchReq(switch, username, password, jsonCmds)
    print response

# Delete VLAN to a switch
def del_vlan(switch, username, password, enable_password, vlans):
    eapi_command = ["configure", "no vlan " +vlans]
    json_data = jsonCreate(eapi_command, enable_password)
    jsonCmds = json.dumps(json_data)

    response = switchReq(switch, username, password, jsonCmds)
    print response

