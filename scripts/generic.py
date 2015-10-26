import sys
from workers.generic_worker import iot_publish


def main(data):
    # 0 means it is successfull
    #iot_publish('play_sound', {'file':'ceva.mp3'})
    iot_publish('speak', {'message': 'The temperature is '+str(data.get('temperature', 25))+' degrees'})
    return 0

