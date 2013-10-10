https-multiplexer
===================

This script forwards a number of configured local ports to other local or remote socket servers based on stream content.
Most notably it is able to allow serving HTTP and HTTPS traffic from the same port.
It can be used to extend Apache web server and automatically choose which actual port (HTTP or HTTPS) to use.
This works perfectly transparently, without the client or server knowing, without interference or performance penalties.

Configuration:
Add to the config file multiplexer.config lines with contents as follows:

<src port> <dest hostname> <dest http port> <dest https port>

Start the application at command line with 'sudo python port-forward.py' and stop the application by keying in &lt;ctrl-c&gt;.

Error messages are stored in file 'error.multiplexer.log'.
