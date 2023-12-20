from pathlib import Path
from pprint import pprint
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
if __name__ == "__main__":
    err_dict = dict()

    cert_dir = Path(__file__).parent.parent / "certs"

    # For each of the certificate directories
    for dir_ in cert_dir.iterdir():
        if dir_.name in ("ca", "server", "openssl.cnf"):
            continue
        try:
            # Try to create the TLS client and connect to server
            resp = create_tls_client(
                "localhost",
                4443,
                dir_ / "cert.pem",
                dir_ / "key.pem",
                cert_dir / "ca" / "ca_cert.pem",
            )
            # If it succeeds, write success
            err_dict[dir_.name] = resp
        # If it fails, write the error
        except Exception as e:
            err_dict[dir_.name] = str(e)

    # Read the errors and list the certs in order
    pprint(err_dict)
