import os
from rpi_streamer.rpi_streamer import StreamingHandler, StreamingServer


class RoombaStreamingHandler(StreamingHandler):
    INDEX_TEMPLATE = 'roomba.html'

    @property
    def template_paths(self):
        return [
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
        ] + super().template_paths

    def do_POST(self):
        # TODO: actually implement the functions
        if self.path == '/api/clean':
            content = '{"status": "ok", "filename": "%s"}' % (filename)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            return

        if self.path == '/api/stop':
            content = '{"status": "ok", "filename": "%s"}' % (filename)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            return

        self.send_error(404)
        self.end_headers()

        return super().do_POST()

if __name__ == '__main__':
    try:
        server = StreamingServer(handler=RoombaStreamingHandler)
        print('Starting camera server')
        server.serve_forever()
    except Exception as e:
        print(str(e))
    print('Stopping camera server')
