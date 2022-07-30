# now
* make modules/twitter.py (direct message as notification etc)
* add ring chime in alerting
* make octoprint plugin for matthew (https://docs.octoprint.org/en/master/plugins/gettingstarted.html#saying-hello-how-to-make-the-plugin-actually-do-something)
* finish modules/whatsapp.py
* add instagram module
* make some agent modules
    * periodic photos, so i can view all at once on a webpage of "last seen"
    * would be cool to get video streaming to work, 

# soon
* make a server on my laptop at home that links up (via a webhook made for uploading data from post requests so i dont have to worry about forwarding) to this and sends data about:
    * network traffic (so i can add monitors like when martin goes on youtube)
    * network members (so i can see when my phone disconnects from network)
* [add aws to modules/storage.py](https://repl.it/@MarcusWeinberger/aws-mysql-test)

# ideas
* make web api with password protection and changing settings of active modules (setattr for that one) 
* all sorts of viewing data
* maybe run a server at home or on the laptop, constantly checking network and stuff i can maybe only do from here like LAN, security cams, pinging, maybe have physicall button or NFC phone thing on my desk that I tap with my phone, sends webhook, and does action
* integrage the deauther to the local server (add functions to send requests to it, maybe use that for monitoring devices - or look for new firmware specifically for monitoring wifi)
* [get vpn](https://repl.it/@MarcusWeinberger/VPN-Gate-Listing-Scraper) - might be cool if any agents/servers need to send gated requests
* add in [minecraft bot](https://repl.it/@MarcusWeinberger/Minecraft-Bot) - notify when username joins maybe? let people send me notifications maybe


# module ideas
* if i can work with our security cams that would allow for sick facial recognition
* wifi monitoring (as people connect and disconnect)
* see what i can get from facebook, google, maybe use whatsapp any status



# completed
* turn some of my devices into "agents", and make a "phone_agents" module. use termux python script for agent so we have termux-api. agents can:
    * record (maybe add in streaming) from mic / camera
    * take photo / record video
    * geolocate
    * use info from sensors
    * buzz (notifications to different devices)
    * play audio/video on screen (done via using termux to open web browser to a page of the server that has video, or youtube)
    * send text (/ call? audio streaming?)
    * do tts and stt (speech-to-text)