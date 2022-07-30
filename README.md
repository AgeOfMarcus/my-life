# command

This is a dashboard / command center that aims to integrate all online aspects of my life. Including hardwired IPs of computers on my local network, adb access to connected phones from agent omen, and can turn the flashlight on on all my devices at once.

Very modularized but the code is mostly spaghetti. A lot of it is unfinished. Uses IFTTT and web requests for I/O.

## modules

* **agents**
    * controls over connected 'agents' (devices)
* **hooks**
    * provides routes for notify hooks
    * routes to download agent scripts for windows and android
* **ring**
    * uses ring doorbell api
    * list of events
    * alerts
* **webdisplay**
    * controls over webdisplay.html
    * when a device has the web display open, content can be updated programatically
* **whatsapp**
    * using twilio
    * adds messaging functionality
    * route to trigger invite message