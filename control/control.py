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
        self.wake_up()
        return super().start_cleaning()

    def turn_off_power(self):
        self.wake_up()
        return super().turn_off_power()

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
            print('Cleaning, as requested!')
            rb.start_cleaning()
            socket.send(b"ok")
        elif message == 'stop':
            print('Halting to a stop, as requested!')
            rb.turn_off_power()
            socket.send(b"ok")
        elif message == 'wake_up':
            rb.wake_up()
            socket.send(b"ok")
        else:
            print('WTF are you going on about?')
            #  Send reply back to client
            socket.send(b"fail")
