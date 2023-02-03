# mintqtt

Publish your personal financial account information to an IoT message broker for any number of possible automations!

This application primarily leverages:
* [MintAPI](https://github.com/mintapi/mintapi) to grab your personal financial data from Intuit Mint
* [Paho MQTT](https://github.com/eclipse/paho.mqtt.python) to publish data to MQTT broker
* [CherryStrap](https://github.com/theguardian/CherryStrap/) to serve as web app framework

## How does it work?
**mintqtt** is a fairly straightforward interpretation of MintAPI. The returned information is sent as a preformatted MQTT message to the configured MQTT broker. From there, any consumer of MQTT information can subscribe. The original author integrates this data with [Home Assistant](https://github.com/home-assistant) utilizing MQTT prefix `homeassistant` 

**Net Worth**\
If enabled, creates a sensor called `Net Worth` and displays your net worth in dollars

**Credit Score**\
If enabled, creates a sensor called `Credit Score` and displays your score as a number

**Accounts**\
If enabled, creates one sensor per `ACTIVE` account whose sensor name corresponds to your friendly name configured in Mint and displays the account's present value in dollars. Sensor attributes include all account-specific data returned by MintAPI

**Budgets**\
If enabled, creates one sensor per budget (with corresponding name) as configured in Mint. Each sensor is currently hardcoded to display the present month's *remaining budget* in dollars. Sensor attributes include all budget-specific data returned by MintAPI

**Transactions**\
If enabled, creates one sensor called `Posted Transactions` that sums the total dollar amount of all transactions posted on the present day. Sensor attributes include `merchant`, `amount`, and `category` per posted transaction

**Bills**\
Not currently developed

**Investments**\
Not currently developed

**Initiate Refresh**\
Not currently developed 

## Installation Instructions 
### via GitHub
It is highly recommended you run in a virtual environment!
```
$ git clone https://github.com/theguardian/mintqtt
$ cd mintqtt
$ pip3 install -r requirements.txt
$ python CherryStrap.py
```

### via Docker (preferred)
```
$ docker run --name mintqtt-container-name -p 7889:7889 -v /host/path/data_dir:/srv/mintqtt/data justinevans/mintqtt:latest
```

## Application Manual
By default, this web application runs on port 7889, but is configurable at the application level and/or in docker configuration. Simply point your browser to your host machine's IP address and configured port to enter the web application.

## Settings (the cogwheel in the top right corner)
This is where all the magic happens. The UI exists simply to make configuration changes or view the logs for troubleshooting purposes. There is **no UI functionality** outside of setting variables or viewing logs!

**Server**\
Configuration settings for application name, port, log directory, etc. It is unlikely that these settings need to be changed

**Interface**\
Set a username and password for the UI if desired. `Theme` is undeveloped

**Database**\
Unused for this application

**Update**\
Optionally subscribe to upstream mintqtt app changes on GitHub

**MintAPI**\
MintAPI-specific configuration settings. More information available at [MintAPI on GitHub](https://github.com/mintapi/mintapi) 

**MQTT**\
MQTT-specific configuration settings. More information available at [Paho MQTT on GitHub](https://github.com/eclipse/paho.mqtt.python)

**Scheduler**\
Choose to retrieve/post data on an interval, on a cron schedule, and/or to run on boot. Retrieve from Mint and post to MQTT are currently bundled as a sequential one-shot

**Data Selection**\
Checkboxes to select what Mint information you would like posted to MQTT broker

## Known Issues & Limitations
* This was only tested on `v2` of MintAPI (requiring the new UI at mint.intuit.com)
* When connecting to Mint via MintAPI for the first time, even with MFA disabled, you will likely have to input your MFA code (likely sent to your email address on file) **into the terminal**. If the session directory is set properly, you should not have to enter MFA code on subsequent runs
  * If running via docker, you will have to enter the container's terminal, kill CherryStrap.py process, then start the app again with command `python CherryStrap.py` and wait for MFA prompt
* To-date, this application has only been tested with **Mint MFA disabled**
* All known issues and limitations for upstream packages (e.g. MintAPI, Paho MQTT, etc are inherited)

## Disclaimers
Please understand that the original author is a hobbyist coder with very little formal training in software development. This is built as a hobby project and there are no warranties stated or implied. Some code is likely to be superfluous or "unpythonic" as this entire web application framework has been stitched together over a number of years. Are there faster, better, , more-secure, higher-quality ways to build this app? You betcha! Is that something the original author has time for or wants to continue maintaining? Unlikely!

## License and Copyright

All code is offered under the GPLv3 license, unless otherwise noted. Please see
LICENSE.txt for the full license.
