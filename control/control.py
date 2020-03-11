import time
from gpiozero import LED
from pyroombaadapter import PyRoombaAdapter
from flask import Flask


BRC = LED('BOARD16')
OUTPUT_ENABLE = LED('BOARD18')
app = Flask('RoombaControl')


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


@app.route('/clean')
def clean():
    global rb
    rb.start_cleaning()
    return '', 200


@app.route('/stop')
def stop():
    global rb
    rb.turn_off_power()
    return '', 200


@app.route('/dock')
def dock():
    global rb
    rb.start_seek_dock()
    return '', 200


@app.route('/wake_up')
def wake_up():
    global rb
    rb.wake_up()
    return '', 200


if __name__ == '__main__':
    global rb
    rb = RoombaControl()
    app.run(host='0.0.0.0', port=80)
