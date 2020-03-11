import os
import requests
from rpi_streamer.rpi_streamer import StreamingHandler, StreamingServer


class RoombaStreamingHandler(StreamingHandler):
    INDEX_TEMPLATE = 'roomba.html'

    @property
    def template_paths(self):
        return [
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
        ] + super().template_paths

    def __call_control(self, command):
        return requests.get('http://control/%s' % command).status_code

    def __handle_command(self, command):
        self.send_response(self.__call_control(command))
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', 0)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/clean':
            self.__handle_command('clean')
            return

        if self.path == '/api/dock':
            self.__handle_command('dock')
            return

        if self.path == '/api/stop':
            self.__handle_command('stop')
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
