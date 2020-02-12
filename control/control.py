import zmq
from pyroombaadapter import PyRoombaAdapter


class RoombaControl(PyRoombaAdapter):
    def __init__(self):
        super().__init__(port='/dev/serial0')

    def wake_up(self):
        # TODO: Raise BRC to HIGH to wake up the Roomba
        pass


if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        message = socket.recv().decode('utf-8')

        if message == 'clean':
            print('Cleaning, as requested!')
            RoombaControl().start_cleaning()
            socket.send(b"ok")
        elif message == 'stop':
            print('Halting to a stop, as requested!')
            RoombaControl().turn_off_power()
            socket.send(b"ok")
        else:
            print('WTF are you going on about?')
            #  Send reply back to client
            socket.send(b"fail")
