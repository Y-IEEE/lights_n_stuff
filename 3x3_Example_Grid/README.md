# 3x3 Static Grid Example
Intended to be used as an example implementation of final version on a static 3x3 grid

## Setup:
  - Web Interface <---> cloudMQTT <---> Arduino
  - Using Bootstrap CSS for the cards and Paho MQTT

## Web Interace:
### Paho Javascript Client
  - Uses the paho javascript client to subscribe and publish messages to the cloudMQTT topic /lights
### Grid
  - Buttons convert to array of numbers valued 0,1,2,3 which are white,red,green,blue respectively
  - Grid changes color based on button presses, if client is subscribed to topic it will also "sync" when a new message from a different client is received
### Javascript Topic as ID
  - Because we were having issues with the size of the message the arduino could receive we are looking into sending each message in a different topic so each arduino only has to subscribe to the topic of its id
  - There is a default limit to the size of the message (see [Configuration Options](https://pubsubclient.knolleary.net/api.html#configoptions))
  - [This link](https://github.com/knolleary/pubsubclient/issues/501) appears promising for changing the size of the message
  - Each LED requires 136 bits (17 bytes) to transmit its id and color MAX is default 128 bytes

## cloudMQTT:
  - cloudMQTT free version is being used as a broker between website and arduino
  - using Websocket implementation
  
## Important Note:
  - Because of the static nature of the grid this implementation needs a lot of work in order to become scalable
