def main():
    import socket

    assert url.startswith("http://")
    url = url[len("https://"):]
    host, path = url.split("/", 1)
    path = "/" + path

    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )

    s.connect((host, 80))
    return

if __name__ == '__main__':
    main()
