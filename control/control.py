import time
import zmq
from gpiozero import LED
from pyroombaadapter import PyRoombaAdapter


BRC = LED('BOARD16')
OUTPUT_ENABLE = LED('BOARD18')


class RoombaControl(PyRoombaAdapter):
    def __init__(self):
        super().__init__(port='/dev/serial0')
        BRC.on()
        OUTPUT_ENABLE.on()

    def start_cleaning(self):
        print('Cleaning, as requested!')
        self.wake_up()
        return super().start_cleaning()

    def turn_off_power(self):
        print('Halting to a stop, as requested!')
        self.wake_up()
        return super().turn_off_power()

    def start_seek_dock(self):
        print('Seeking dock, as requested!')
        self.wake_up()
        return super().start_seek_dock()

    def wake_up(self):
        print('Waking up the Roomba')
        BRC.off()
        time.sleep(0.5)
        BRC.on()


if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    rb = RoombaControl()

    while True:
        #  Wait for next request from client
        message = socket.recv().decode('utf-8')

        if message == 'clean':
            rb.start_cleaning()
            socket.send(b"ok")
        elif message == 'stop':
            rb.turn_off_power()
            socket.send(b"ok")
        elif message == 'dock':
            rb.start_seek_dock()
            socket.send(b"ok")
        elif message == 'wake_up':
            rb.wake_up()
            socket.send(b"ok")
        else:
            print('WTF are you going on about?')
            #  Send reply back to client
            socket.send(b"fail")
