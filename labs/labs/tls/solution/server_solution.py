from pathlib import Path
import socket
import ssl


def verify_client_certificate(conn) -> bool:
    client_cert = conn.getpeercert()
    if not client_cert:
        return False  # No client certificate presented

    subject = dict(item[0] for item in client_cert["subject"])
    client_cn = subject.get("commonName")
    alt = client_cert["subjectAltName"]
    if client_cn == "incorrect_client":
        print(client_cn)
    if "invalid_san.com" in str(alt):
        print(alt)

    # Check if the CN matches the expected value
    return client_cn != "incorrect_client" and "invalid_san.com" not in str(alt)


def create_tls_server(
    certfile_path: Path,
    keyfile_path: Path,
    cafile_path: Path,
    hostname: str = "localhost",
    port: int = 4443,
) -> None:
    certfile = str(certfile_path)
    keyfile = str(keyfile_path)
    cafile = str(cafile_path)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    context.load_verify_locations(cafile=cafile)
    context.verify_mode = ssl.CERT_REQUIRED

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((hostname, port))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            print(f"TLS server running on {hostname}:{port}")
            while True:
                try:
                    conn, addr = ssock.accept()
                    with conn:
                        if not verify_client_certificate(conn):
                            print(
                                f"Connection from {addr} rejected: "
                                "Invalid CN in client certificate"
                            )
                            conn.close()
                            continue
                        print(f"Connected by {addr}")
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            print(f"Received: {data.decode()}")
                            conn.sendall(data)
                except ssl.SSLError as e:
                    print(f"SSL error: {e}")


if __name__ == "__main__":
    certs_dir = Path(__file__).parent.parent / "certs"
    server_dir = certs_dir / "server"
    ca_dir = certs_dir / "ca"
    create_tls_server(
        server_dir / "server_cert.pem",
        server_dir / "server_key.pem",
        ca_dir / "ca_cert.pem",
    )
