import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv().decode('utf-8')

    if message == 'clean':
        print('Cleaning, as requested!')
        socket.send(b"ok")
    elif message == 'stop':
        print('Halting to a stop, as requested!')
        socket.send(b"ok")
    else:
        print('WTF are you going on about?')
        #  Send reply back to client
        socket.send(b"fail")
