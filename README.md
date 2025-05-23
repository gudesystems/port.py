# Functions
 - Query / Switch state of powerport(s) by HTTP (batch wise)
 - HTTP Authentification and SSL encryption supported by optional command line parameters
 - show OVP state

# Examples
## Example for device (192.168.0.2) with 4 ports:

    ./port.py -H 192.168.0.2
    1
    0
    0
    0

    ./port.py -H 192.168.0.2 --port 2
    0

    ./port.py -H 192.168.0.2 --port 2 --switch 1
    1

    ./port.py -H 192.168.0.2
    1
    1
    0
    0

## Batch wise switching of first port with ssl-encryption and credentials

To switch port 1 on, off, on and off in a 2 seconds delay:

    ./port.py -H 192.168.210.163 --ssl --username admin --password pw123 -p 1 -b 2 -a 1 0 1 0 

## show OVP sate
    ./port.py -H 192.168.0.2 --ovp 1
    1

# Info
Following devices are not supported (see [issue 1](https://github.com/gudesystems/port.py/issues/1) for alternative):
 - _Expert Power Control 8080_
 - _EMC Professional_
