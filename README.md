ShadowParser
============

###Parsing framework for ShadowBuster.

The project started out with something simple in mind for just one server. 
There's no reason to design it that way though, so it is being organized 
to use a central ShadowParser server consisting of a parser with plugins
and a websocket server to connect with ShadowBuster. Separate lients can 
push events to the central ShadowParser server for processing.

Tornado was chosen for the websocket server for scalability and RabbitMQ
is being considered for the client-server message queue.

For plugins, currently a simple Nginx access log parser plugin is written.

###Some dependencies:

sudo apt-get install libgeoip-dev python3 python3-pip

sudo pip3 install GeoIP tornado websocket-client