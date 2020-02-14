import os
import zmq
from rpi_streamer.rpi_streamer import StreamingHandler, StreamingServer


class RoombaStreamingHandler(StreamingHandler):
    INDEX_TEMPLATE = 'roomba.html'

    @property
    def template_paths(self):
        return [
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
        ] + super().template_paths

    def __send_to_zmq(self, command):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://control:5555')
        socket.send(command)
        return socket.recv().decode('utf-8')

    def __handle_command(self, command):
        reply = self.__send_to_zmq(command)
        content = '{"status": "%s"}' % reply
        self.send_response(200 if reply == 'ok' else 500)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def do_POST(self):
        if self.path == '/api/clean':
            self.__handle_command(b'clean')
            return

        if self.path == '/api/dock':
            self.__handle_command(b'dock')
            return

        if self.path == '/api/stop':
            self.__handle_command(b'stop')
            return

        return super().do_POST()


if __name__ == '__main__':
    try:
        server = StreamingServer(handler=RoombaStreamingHandler)
        print('Starting camera server')
        server.serve_forever()
    except Exception as e:
        print(str(e))
    print('Stopping camera server')
