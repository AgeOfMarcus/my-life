# my life

This is a dashboard / command center that aims to integrate all online aspects of my life. Including hardwired IPs of computers on my local network, adb access to connected phones from agent omen, and can turn the flashlight on on all my devices at once.

Very modularized but the code is mostly spaghetti. A lot of it is unfinished. Uses IFTTT and web requests for I/O.

## environment variables

* IFTTT: ifttt key for webhooks
* adminpass: master password
* apikeys: a colon-separated list of api keys
* dropbox: dropbox api key (not needed)
* phone_*: these are my personal phone number keys (not needed)
* ring_user: ring doorbell username (not needed)
* ring_pass: ring doorbell password (not needed)
* twilio_sid: pretty self explanitory (not needed)
* twilio_secret: see above (not needed)

For any of the keys that are not added, you probably definitely need to remove them from the code. 

## modules (most of them)

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