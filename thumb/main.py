def request(url):
    import socket
    import ssl

    scheme, url = url.split("://", 1)

    assert scheme in ["http", "https"], \
        f"Unsupported / Unknown scheme: '{scheme}'"

    host, path = url.split("/", 1)
    path = "/" + path
    port = 80 if scheme == "http" else 443

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
        print("PORT", port)

    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )

    if scheme == "https":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)

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
