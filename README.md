# Twilio Payment Processing Simulator for Generic Pay connector

A Python simulator for testing Twilio Generic Pay Connectors


## Prerequisites

1. A [Twilio account](https://www.twilio.com/try-twilio)
1. Generic Pay Connector installed in your add-ons `(Product is currently in beta, so you should be provided instructions by a Twilio contact)`
1. Ngrok
1. A Twilio IVR using the [pay verb](https://www.twilio.com/docs/voice/twiml/pay) or the [pay widget in Studio](https://www.twilio.com/docs/studio/widget-library/capture-payments)

## Getting Started:


## Install the required python packages into a virtual environment

Within the project directory, create a virtual environment for requisite python packages (more on [Python virtual environments](https://docs.python.org/3/library/venv.html))
```
% python3 -m venv env
```

Start the virtual environment
```
% source env/bin/activate
```

Install the required python packages
```
% pip3 install -r requirements.txt
```

## Configure the simulator

Two types of simulators are available.

`pay-sim-simple.py` - This version simply responds with "confirmation" of payment, no matter what it is sent.  There is no validation done on the card details.  Use this version first to ensure you have end-to-end connectivity properly established.

`pay-sim-robust.py` - This version has the framework to do some simple tests on the card number, expiry, etc... to demonstrate the return of various error messages.  Use this version to test error reporting on the IVR code you have created.

Configure in the appropriate version of simulator:
- Edit the Basic Auth to be what you plan to use in the configuration of the pay connector.
```
users = {
    "foo": generate_password_hash("bar"),
  ...
```
- Set the port number (if you prefer different from default, 8081)
```
if __name__ == '__main__':
    app.run(port = '8081', debug = True)
  ...
```


## Setup and configure Ngrok
To be able to have your Twilio pay verb/widget reach out to this connector, it will need to be available on the web.  

- Download and install Ngrork: https://ngrok.com/download


- Startup Ngrok (default port is 8081)
```
% ngrok http 8081
```

- When Ngrok starts, capture the URL represented bye the HTTPS port that is setup (highlighted in blue below).  We'll use this in configuring the pay connector later.
![Sweet configuration image on Github](https://github.com/phundal-twilio/twilio-payment-simulator-generic-pay-python/blob/main/Ngrok-sample.png?raw=true)


## Configure your IVR to use a pay verb or Connector
The scope of this is beyond this writeup, but you can find details on the Twilio pay connector here:

- [Twilio pay verb](https://www.twilio.com/docs/voice/twiml/pay)
- [Twilio pay widget in Studio](https://www.twilio.com/docs/studio/widget-library/capture-payments)

## Configure the Twilio Pay Connector Add-on

- Setup your pay connector with the appropriate `Username/Password` (as defined earlier in your .py file).  Set the `ENDPOINT URL` to the the URL captured from Ngrok
![Sweet configuration image on Github](https://github.com/phundal-twilio/twilio-payment-simulator-generic-pay-python/blob/main/Connector-configure.png?raw=true)

## Start the simulator

To startup a basic payment simulator (no validation of credit card information).

```
% python3 pay-sim-simple.py
```

To startup a more robust payment simulator that includes validation:

```
% python3 pay-sim-robust.py
```


## Tips and Troubleshooting

When running the simulator, the JSON provided by the <pay> module will be dumped to the console.  Verify this is what is expected.
