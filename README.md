# Converter for dbc files for AGL


Script to convert a Vector CANoe ".dbc" file in the right json format for Automotive Grade Linux (AGL), these software is a the moment a feasability study
created 16. May 2020 by walzert version 0.1 

The python3 requirements are noted in requirements.txt 

The software is based on cantools https://github.com/eerimoq/cantools,
it converts messages from a dbc file -i (input) and add the dataheader for agl on top of the messages

'' python3 dbc2json_converter -i FILENAME.DBC  -b canbus '' 
will create an output with the number of messages in that dbc file and will create a signals.json 
