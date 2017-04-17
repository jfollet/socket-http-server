import socket
import sys


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            request = ""
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                while True:
                    data = conn.recv(4096)
                    request += data.decode()
                    print('received "{0}"'.format(data), file=log_buffer)
                    if len(data) < 4096:
                        break
                    parse_request(request)
                    print('sending data back to client', file=log_buffer)
                    response = response_ok()
                    conn.sendall(response)
                    # else:
                    #     msg = 'no more data from {0}:{1}'.format(*addr)
                    #     print(msg, log_buffer)
                    #     break
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


def response_ok():
    """returns a basic HTTP response"""
    response = b"\r\n".join(
        [
            b"HTTP/1.1 200 OK",
            b"Content-Type: text/plain",
            b"",
            b"this is normal response",
        ]
    )
    return response


def parse_request(request):
    first_line = request.split("\r\n")[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("we only accept GET")
    print('request is okay', file=sys.stderr)


def response_method_not_allowed():
    pass


if __name__ == '__main__':
    server()
    sys.exit(0)
