from generic_worker import iot_publish

#iot_publish('play_sound', {'file':'ceva.mp3'})
#iot_publish('speak', {'message':'Salut'})
iot_publish('lights', {'action':'power-on', 'id':'15'})
