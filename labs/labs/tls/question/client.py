from pathlib import Path
from pprint import pprint  # noqa
import socket
import ssl


def create_tls_client(
    server_hostname: str,
    server_port: int,
    certfile_path: Path,
    keyfile_path: Path,
    cafile_path: Path,
) -> str:
    certfile = str(certfile_path)
    keyfile = str(keyfile_path)
    cafile = str(cafile_path)

    context = ssl.create_default_context()
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    context.load_verify_locations(cafile=cafile)
    context.verify_mode = ssl.CERT_REQUIRED

    with socket.create_connection((server_hostname, server_port)) as sock:
        with context.wrap_socket(sock, server_hostname=server_hostname) as ssock:
            print(f"Connected to TLS server at {server_hostname}:{server_port}")
            message = b"Hello, server!"
            ssock.sendall(message)
            response = ssock.recv(1024)
            print(f"Received: {response.decode()}")
            return response.decode()


# TODO Write the rest of the connections here to determine the rest of the certs
# Submit your solution like so:
# <valid_num>_<expired_num>_<invalid_by_ca_num>_<invalid_by_CN_num>
