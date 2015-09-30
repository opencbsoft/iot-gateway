from workers.generic_worker import iot_publish


iot_publish('play_sound', {'file':'ceva.mp3'})
iot_publish('speak', {'message':'Salut'})