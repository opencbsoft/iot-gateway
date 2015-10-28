import sys

from generic_worker import iot_publish


    # 0 means it is successfull
    #iot_publish('play_sound', {'file':'ceva.mp3'})
iot_publish('speak', {'message':'Temperature'})

