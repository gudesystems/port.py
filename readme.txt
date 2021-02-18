- Query / Switch state of powerport(s) by HTTP
  - HTTP Authentification and SSL encryption supported by optional command line parameters
- show OVP state

Example, where device 192.168.0.2 has 4 ports:

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


  # show OVP sate
  ./port.py -H 192.168.0.2 --ovp 1
  1

