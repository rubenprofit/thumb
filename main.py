def request(url):
    import socket
    assert url.startswith("http://")
    url = url[len("http://"):]
    host, path = url.split("/", 1)
    path = "/" + path
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )
    s.connect((host, 80))
    s.send(f"GET {path} HTTP/1.0\r\n".encode("utf8") + f"Host: {host}\r\n\r\n".encode("utf8"))
    response = s.makefile("r", encoding="utf8", newline="\r\n")
    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)
    assert status == "200", f"{status}: {explanation}"
    headers = {}
    while True:
        line = response.readline()
        if line == "\r\n": break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()
    assert "transfer-encoding" not in headers
    assert "content-encoding" not in headers
    body = response.read()
    s.close()
    return headers, body


def show(body):
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        if c == ">":
            in_angle = False
        elif not in_angle:
            print(c, end="")
    return


def load(url):
    headers, body = request(url)
    show(body)


if __name__ == '__main__':
    import sys
    load(sys.argv[1])
