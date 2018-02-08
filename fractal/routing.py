from interactive import consumers
from channels.staticfiles import StaticFilesConsumer


channel_routing = {


    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_receive,
    'websocket.disconnect': consumers.ws_disconnect,


}
