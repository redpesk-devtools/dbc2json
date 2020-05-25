#!/usr/bin/python

# Script to convert a Vector CANoe ".dbc" file in the right json format for Automotive Grade Linux (AGL), these software is a the moment a feasability study
# created 16. May 2020 by walzert version 0.1 
# the python3 requirements are noted in requirements.txt 
# the software is based on cantools https://github.com/eerimoq/cantools
# it converts messages from a dbc file -i (input) and add the dataheader for agl on top of the messages

import sys, getopt
import cantools
from pprint import pprint
import json 

# plain coded data header for AGL as json-file, needs a proper file like example_header.json 
with open('header.json') as json_file:
    data_header = json.load(json_file)

# dictonary for the messages starting with messages prepared to add new messages in that

messages_dict = {"messages" : {}}
#print(messages_json["messages"])
# = json.dumps(messages_json)
#rint("---------------------------------------------------")
#print(y) 
#print("---------------------------------------------------")


# the main method expect on argument which is the input-file as ".dbc", a parameter for the bus and the mode
def main(argv):
    mode = False
    inputfile = ''
    bus = ''
    try:
        opts, args = getopt.getopt(argv,"hi:b:w",["ifile=", "bus=", "mode="])
    except getopt.GetoptError:
        print ('dbc2json.py -i <inputfile> -m <writeable(true|false) -b <canbus>')
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print ('dbc2json.py -i <inputfile> -m <writeable(true|false)> -b <canbus>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-b", "--bus"):
            bus = arg
        elif opt in ("-w", "--writeable"):
            mode = True
            print (mode)
    # load the can database file in cantools to work on the db
    db = cantools.database.load_file(inputfile)
    # load the messages to iterate over them altough print number of lines as output
    messages = db.messages
    print("Number of messages " +str(len(messages)))
    # in the iteration a base message ist created, it is adapted by the agl demo signal.json file and don't contain all information
    # { "name" : message.name, "bus" : message.bus_name, "is_fd": False, "is_j1939" : False, "is_extended" : message.is_extended_frame, "signals" : {}}
    # in the interation process are all the messages that are interpreted by cantools (list is not complete)
    for message in messages:
        #print(hex_value)
        #print(type(hex_value))
        #print(type(message_json[str(hex(message.frame_id))]["signals"]))
        #message_json[str(hex(message.frame_id))]["signals"].append()
        #messages_length = len(messages_json)
        #messages_json[messages_length] = message_json
        #pprint(signal_dict)
        #pprint(message.frame_id)
        #pprint(hex(message.frame_id))
        #pprint(message.name)
        #pprint(message.length)
        #pprint(signals)
        #pprint(message.comment)
        #pprint(message.senders)
        #pprint(message.send_type)
        #pprint(message.cycle_time)
        #pprint(message.dbc_specifics)
        #pprint(message.is_extended_frame)
        #pprint(message.bus_name)
        #pprint(message.signal_groups)
        #pprint(message.strict)
        #pprint(message.protocol)
        #pprint(message_json)

        # the message is built by the informations through cantools conversion the hex-string will be used as message id , the message_json will be saved in messages_dict
        # working object signal_dict will be created to work later on, singals object with all signals in that messages is created
        message_json =  { "name" : message.name, "bus" : bus, "is_fd": False, "is_j1939" : False, "is_extended" : message.is_extended_frame, "signals" : {}}
        hex_value = str(hex(message.frame_id))
        messages_dict["messages"][hex_value] = message_json
        signal_dict = messages_dict["messages"][hex_value]["signals"]
        signals = message.signals
    
        # all signal informations that are known through  cantools are printed (uncommented) as a for loop in all signals of a message
        for signal in signals:
            #signal_length = len(signal_dict)
            #print(signal_json)
            #pprint(signal_json)z
            #pprint(len(signal_dict))
            #signal_dict[signal_json] = signal_json
            #pprint(signal.name)
            #pprint(signal.start)
            #pprint(signal.length)
            #pprint(signal.byte_order)
            #pprint(signal.is_signed)
            #pprint(signal.initial)
            #pprint(signal.scale)
            #pprint(signal.offset)
            #pprint(signal.minimum)
            #pprint(signal.maximum)
            #pprint(signal.unit)
            #pprint(signal.choices)
            #pprint(signal.dbc_specifics)
            #pprint(signal.comment)
            #pprint(signal.receivers)
            #pprint(signal.is_multiplexer)
            #pprint(signal.multiplexer_ids)
            #pprint(signal.multiplexer_signal)
            #pprint(signal.is_float)
            #pprint(signal.decimal)
            #
            #
            # a new signal in agl format will be created 
            # { "generic_name" : signal.name, "bit_position" : signal.start, "bit_size" : signal.length, "factor" : signal.scale, "offset" : signal.offset }
            # it is just a subset and not complete 
            # after the creation it will be pushed in the messages:messages:signal
            signal_json = { "generic_name" : signal.name, "bit_position" : signal.start, "bit_size" : signal.length, "factor" : signal.scale, "offset" : signal.offset, "writeable" : mode }
            signal_dict[signal.name] = signal_json


    #z = json.dumps(messages_dict)

    # all files for the output will be added  it starts with the agl header and is followed by the messages
    # file will be saved as singal.json
    output_all = data_header 
    output_all.update(messages_dict)
    #print(output_all)
    #z = json.dumps(output_all)
    #pprint(z)
    with open('signals.json', 'w') as outfile:
        json.dump(output_all, outfile)
    print("Finished")
        #db.get_message_by_name(message.signals)
        #print(messages.signals)
    #pprint(db)
    #db.messages
    #print(len(db.messages))
    #print(db.messages)
    #example_message = db.get_message_by_name('P_Engine_Sensoric')
    #pprint(example_message.signals)

    # self,name,start,length,byte_order='little_endian',is_signed=False,initial=None,scale=1,offset=0,minimum=None,maximum=None,unit=None,choices=None,dbc_specifics=None,comment=None,receivers=None,is_multiplexer=False,multiplexer_ids=None,
    #                 multiplexer_signal=None,is_float=False,decimal=None)



if __name__ == '__main__':
   main(sys.argv[1:])