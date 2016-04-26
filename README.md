# airos-config

```
$ ./configure.py -h
usage: configure.py [-h] [-u USERNAME] [-p PASSWORD] host hostname ipaddress

positional arguments:
  host                  The address of your device.
  hostname              The hostname you want to configure.
  ipaddress             IP address.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        The username. Default 'ubnt'.
  -p PASSWORD, --password PASSWORD
                        The password. Default 'ubnt'.
```

## What it does

* Takes `system.cfg` (backup of your config from the AirOS-device)
* Replaces hostname and IP-address
* scp's the file to the device
* Saves the config
* Reboot
