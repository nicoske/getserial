import bottle
from bottle import get, post, request, template, route
bottle.TEMPLATE_PATH.insert(0,'/var/www/cgi-bin/')

#@get('/getserial')
@route('/', method='GET')
def show_form():
    return '''
<form action="/getserial" method="POST">
 <div>
  <label>IP address of device:</label>
  <input type="text" name="ip"/>
 </div>
 <div>
  <label>Type of device:</label>
   <select name="type">
    <option value="biamp_audia">Biamp Audia</option>
    <option value="corio">Corio</option>
   </select>
</div>
<input type="submit"/>
</form>'''

#@post('/getserial')
@route('/', method='POST')
def run():
 type = request.forms.get('type')
 address = request.forms.get('ip')

 if type == 'biamp_audia':
    import os
    from socket import socket, AF_INET, SOCK_STREAM
    import struct
    import re
    import sys
    port = 12001
    data = '000000100100000000010a000822000030010001'.decode('hex')

    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(5)
    s.connect((address, port))
    s.send(data.encode('utf-8'))
    output = s.recv(32)
    s.close()

    output = output[17:32]
    output = str(output)
    serial = re.sub('[^0-9]','', output)
    #return output, address, type
    """results"""
    info = {'type' : type,
    'serial' : serial,
    'address' : address
     }
    return template('standard.tpl', info)

 elif type == 'corio':
  import telnetlib
  serialcard = []
  session = telnetlib.Telnet(address, 10001, 5)
  #session.set_debuglevel(9) # enable telnet debugging
  response = session.read_until("'login(username,password)'",5)
  session.write("login(admin,adminpw)" + "\r\n")
  response = session.read_until("!Info : User admin Logged In",5)
  session.write("CORIOmax.Serial_Number" + "\r\n")
  data = session.read_until("!Done", 1)
  serial = data.splitlines()[1]  

  for x in range(1, 17):
   session.write("Slots.Slot" + str(x) + ".Carddata" + "\r\n")
   data =  session.read_until("!Done", 1)
   if "BaseNo" not in data:
    continue
   card = data.splitlines()[1]
   serialcard.append(card)

  info = {'type' : type,
   'serial' : serial,
   'serialcard' : serialcard,
   'address' : address
    } 

  return template('corio.tpl', info)

  session.close()

application=bottle.default_app() 
#bottle.run(host='s-scic-stats2', port=8000, debug=True) # run in a local test server

