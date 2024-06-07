from functools import cached_property
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys

from src.utils import Grade, LabTemplate, Lab, CLIHandler


class TLSLabTemplate(LabTemplate):
    # DB properties
    lab_template_id: int = 0
    # Used only when seeding for the first time
    seed_name: str = "TLS Lab"
    seed_section: str = "Ch5"
    seed_short_description: str = (
        "In this lab users will learn about TLS and Certificate Authorities"
    )
    seed_long_description: str = "TLS Lab, long desc TODO"
    seed_active: bool = True
    # Static dir
    static_dir: Path = Path(__file__).parent

    @staticmethod
    def _grade(submitted_solution: str, solution: str) -> Grade:
        """Grades a submissions

        Give 25% for each correct cert
        Submissions are supposed to be in the form of:
        0_1_2_3
        """

        # NOTE: this should be dynamic, but is currently staticmethod
        # should point to len(self.client_dirs) in the future
        total_certs = 9
        submitted_solution_nums = submitted_solution.split("_")
        solution_nums = solution.split("_")
        if set(submitted_solution_nums) != set([str(x) for x in range(0, total_certs)]):
            return Grade(
                score=0,
                feedback=f"Solution must be in form of 0_1_2_3: {
                    submitted_solution}",
            )
        else:
            score: float = 0
            for user_num, gt_num in zip(submitted_solution_nums, solution_nums):
                if user_num == gt_num:
                    score += 100 / total_certs
            score = round(score)
            if score == 100:
                feedback = "Great job!"
            else:
                missed = round((100 - score) / (100 / total_certs))
                feedback = f"Missed {missed} certs, try again :)"
            return Grade(score=score, feedback=feedback)

    def generate_lab(self, *, user_id: int = 0, seed: str = "abcd", debug: bool = False) -> Lab:  # type: ignore
        random.seed(seed)
        # Generate all certs
        self.gen_all_certs()
        # Shuffle certs to get solution
        shuffled_client_cert_dirs = list(self.client_cert_dirs)
        random.shuffle(shuffled_client_cert_dirs)
        # Solution is valid, expired, invalid_ca, invalid_cn
        solution = "_".join(
            str(shuffled_client_cert_dirs.index(x)) for x in self.client_cert_dirs
        )
        # Don't cover this since this is never called unless a developer manually sets it
        if debug:  # pragma: no cover
            # For debugging - don't rename dirs
            for i, cert_dir_path in enumerate(shuffled_client_cert_dirs):
                shutil.move(
                    str(cert_dir_path), str(
                        cert_dir_path.parent / cert_dir_path.name)
                )

        else:
            # Rename the cert paths to match the solution
            for i, cert_dir_path in enumerate(shuffled_client_cert_dirs):
                shutil.move(str(cert_dir_path), str(
                    cert_dir_path.parent / str(i)))

        # Copy the question folder into the directory that will be given to users
        self._copy_q_dir_into_lab_generated_dir()

        return Lab(
            lab_template_id=self.lab_template_id,
            user_id=user_id,
            seed=seed,
            unique_question_file=self._zip_temp_lab_dir_and_read(),
            solution=solution,
        )

    ################################
    # Certificate generation funcs #
    ################################

    def gen_all_certs(self) -> None:
        """Generates server, valid, invalid_by_ca, invalid_by_cn, and expired certs"""

        # Generate CA certificate and key
        self.gen_ca_cert()

        # server cert
        self.gen_cert(self.server_cert_path,
                      self.server_key_path, "/CN=localhost")
        # Valid cert
        self.gen_cert(self.valid_cert_path,
                      self.valid_key_path, "/CN=CLIENT_ID")
        # Expired cert
        self.gen_expired_cert(
            self.expired_cert_path, self.expired_key_path, "/CN=CLIENT_ID"
        )
        # Invalid CA cert
        self.gen_unsigned_cert(
            self.invalid_ca_cert_path, self.invalid_ca_key_path, "/CN=CLIENT_ID"
        )
        # Invalid CN cert
        self.gen_cert(
            self.invalid_cn_cert_path, self.invalid_cn_key_path, "/CN=incorrect_client"
        )

        self.gen_cert_with_md5(
            self.md5_cert_path, self.md5_key_path, "/CN=CLIENT_ID")
        self.gen_cert_with_unknown_extension(
            self.unknown_ext_cert_path, self.unknown_ext_key_path, "/CN=CLIENT_ID"
        )
        self.gen_cert_with_incorrect_usage(
            self.incorrect_usage_cert_path,
            self.incorrect_usage_key_path,
            "/CN=CLIENT_ID",
        )
        self.gen_cert(
            self.invalid_san_cert_path,
            self.invalid_san_key_path,
            "/CN=CLIENT_INVALID_SAN",
            "DNS:invalid_san.com",
        )
        # The next two go together
        self.gen_untrusted_ca_cert()
        self.gen_cert_with_invalid_chain(
            self.invalid_chain_cert_path, self.invalid_chain_key_path, "/CN=CLIENT_ID"
        )

    def create_openssl_conf(
        self, san: str = "", unknown_ext: bool = False, incorrect_usage: bool = False
    ) -> Path:
        """This is needed for Herzberg's custom commands"""

        conf_content = """
        [ req ]
        distinguished_name = req_distinguished_name
        req_extensions = v3_req
        x509_extensions = v3_ca  # For self-signed certificates

        [ req_distinguished_name ]

        [ v3_req ]
        basicConstraints = CA:FALSE
        keyUsage = digitalSignature, keyEncipherment
        subjectAltName = @alt_names

        [ v3_ca ]
        # Adjust these as needed for CA certs
        subjectKeyIdentifier = hash
        authorityKeyIdentifier = keyid:always,issuer
        basicConstraints = critical, CA:true
        keyUsage = critical, digitalSignature, cRLSign, keyCertSign

        [ alt_names ]
        """
        if san:
            conf_content += f"DNS.1 = {san}\n"
        else:
            conf_content += "DNS.1 = localhost\n"

        if unknown_ext:
            conf_content += """
            [ unknown_ext ]
            1.2.3.4.5.6.7.8 = critical,ASN1:UTF8String:Unknown Extension Value
            """

        if incorrect_usage:
            conf_content += """
            [ incorrect_usage ]
            keyUsage = nonRepudiation
            """

        conf_path = self.cert_dir / "openssl.cnf"
        with open(conf_path, "w") as conf_file:
            conf_file.write(conf_content)
        return conf_path

    def run_openssl_command(self, command: str) -> None:
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise Exception(
                f"Error executing command: {command}\n{result.stderr.decode()}"
            )

    def gen_ca_cert(self) -> None:
        # Generate CA private key
        self.run_openssl_command(
            f"openssl genrsa -out {self.ca_key_path} 2048")
        # Generate CA certificate
        self.run_openssl_command(
            f"openssl req -x509 -new -nodes -key {self.ca_key_path} "
            f"-sha256 -days 1024 -out {self.ca_cert_path} "
            "-subj '/CN=Certificate Authority'"
        )

    def gen_cert(self, cert_path: Path, key_path: Path, subject: str, san: str = ""):
        openssl_conf_path = self.create_openssl_conf(san)
        self.run_openssl_command(f"openssl genrsa -out {key_path} 2048")
        self.run_openssl_command(
            f"openssl req -new -key {key_path} -out {cert_path}.csr "
            f"-subj '{subject}' -config {openssl_conf_path}"
        )
        self.run_openssl_command(
            f"openssl x509 -req -in {cert_path}.csr -CA {self.ca_cert_path} "
            f"-CAkey {self.ca_key_path} -CAcreateserial -out {cert_path} "
            f"-days 500 -sha256 -extfile {
                openssl_conf_path} -extensions v3_req"
        )
        self.run_openssl_command(f"rm {cert_path}.csr")

    def gen_unsigned_cert(self, cert_path: Path, key_path: Path, subject: str) -> None:
        # Generate private key
        self.run_openssl_command(f"openssl genrsa -out {key_path} 2048")
        # Generate a self-signed certificate (not signed by the CA)
        self.run_openssl_command(
            f"openssl req -new -x509 -key {key_path} "
            f"-out {cert_path} -days 365 -subj '{subject}'"
        )

    def gen_expired_cert(self, cert_path: Path, key_path: Path, subject: str) -> None:
        # Generate private key
        self.run_openssl_command(f"openssl genrsa -out {key_path} 2048")
        # Generate CSR (Certificate Signing Request)
        self.run_openssl_command(
            f"openssl req -new -key {key_path} -out {
                cert_path}.csr -subj '{subject}'"
        )
        # Sign the certificate with the CA with a past date for expiration
        self.run_openssl_command(
            f"openssl x509 -req -in {cert_path}.csr -CA {self.ca_cert_path} "
            f"-CAkey {self.ca_key_path} -CAcreateserial "
            f"-out {cert_path} -days -1 -sha256"
        )
        # Cleanup CSR
        self.run_openssl_command(f"rm {cert_path}.csr")

    def gen_cert_with_md5(self, cert_path: Path, key_path: Path, subject: str) -> None:
        self.run_openssl_command(f"openssl genrsa -out {key_path} 2048")
        self.run_openssl_command(
            f"openssl req -new -key {key_path} -out {
                cert_path}.csr -subj '{subject}'"
        )
        self.run_openssl_command(
            f"openssl x509 -req -in {cert_path}.csr -CA {self.ca_cert_path} "
            f"-CAkey {self.ca_key_path} -CAcreateserial -out {cert_path} "
            f"-days 500 -md5"
        )
        self.run_openssl_command(f"rm {cert_path}.csr")

    def gen_cert_with_unknown_extension(
        self, cert_path: Path, key_path: Path, subject: str
    ):
        openssl_conf_path = self.create_openssl_conf(unknown_ext=True)
        self.run_openssl_command(f"openssl genrsa -out {key_path} 2048")
        self.run_openssl_command(
            f"openssl req -new -key {key_path} -out {
                cert_path}.csr -subj '{subject}'"
        )
        self.run_openssl_command(
            f"openssl x509 -req -in {cert_path}.csr -CA {self.ca_cert_path} "
            f"-CAkey {self.ca_key_path} -CAcreateserial -out {cert_path} "
            f"-days 500 -sha256 -extfile {
                openssl_conf_path} -extensions unknown_ext"
        )
        self.run_openssl_command(f"rm {cert_path}.csr")

    def gen_cert_with_incorrect_usage(
        self, cert_path: Path, key_path: Path, subject: str
    ) -> None:
        openssl_conf_path = self.create_openssl_conf(incorrect_usage=True)
        self.run_openssl_command(f"openssl genrsa -out {key_path} 2048")
        self.run_openssl_command(
            f"openssl req -new -key {key_path} -out {
                cert_path}.csr -subj '{subject}'"
        )
        self.run_openssl_command(
            f"openssl x509 -req -in {cert_path}.csr -CA {self.ca_cert_path} "
            f"-CAkey {self.ca_key_path} -CAcreateserial -out {cert_path} "
            f"-days 500 -sha256 -extfile {openssl_conf_path} "
            "-extensions incorrect_usage"
        )
        self.run_openssl_command(f"rm {cert_path}.csr")

    def gen_untrusted_ca_cert(self) -> None:
        # Generate untrusted CA private key
        untrusted_ca_key_path = self.cert_dir / "untrusted_ca_key.pem"
        self.run_openssl_command(
            f"openssl genrsa -out {untrusted_ca_key_path} 2048")

        # Generate untrusted CA certificate
        untrusted_ca_cert_path = self.cert_dir / "untrusted_ca_cert.pem"
        self.run_openssl_command(
            f"openssl req -x509 -new -nodes -key {untrusted_ca_key_path} "
            f"-sha256 -days 1024 -out {untrusted_ca_cert_path} "
            "-subj '/CN=Untrusted Certificate Authority'"
        )

    def gen_cert_with_invalid_chain(
        self, cert_path: Path, key_path: Path, subject: str
    ) -> None:
        untrusted_ca_key_path = self.cert_dir / "untrusted_ca_key.pem"
        untrusted_ca_cert_path = self.cert_dir / "untrusted_ca_cert.pem"

        # Generate private key for the certificate
        self.run_openssl_command(f"openssl genrsa -out {key_path} 2048")

        # Generate CSR (Certificate Signing Request)
        self.run_openssl_command(
            f"openssl req -new -key {key_path} -out {
                cert_path}.csr -subj '{subject}'"
        )

        # Sign the certificate with the untrusted CA
        self.run_openssl_command(
            f"openssl x509 -req -in {cert_path}.csr -CA {untrusted_ca_cert_path} "
            f"-CAkey {untrusted_ca_key_path} -CAcreateserial "
            f"-out {cert_path} -days 500 -sha256"
        )

        # Cleanup CSR
        self.run_openssl_command(f"rm {cert_path}.csr")
        self.run_openssl_command(f"rm {untrusted_ca_key_path}")
        self.run_openssl_command(f"rm {untrusted_ca_cert_path}")

    #################
    # Path properties
    #################

    @cached_property
    def cert_dir(self) -> Path:
        cert_dir = self.temp_lab_dir / "certs"
        assert isinstance(cert_dir, Path), "for mypy"
        cert_dir.mkdir(exist_ok=True, parents=True)
        return cert_dir

    # CA Cert path properties
    @cached_property
    def ca_cert_dir(self) -> Path:
        ca_cert_dir = self.cert_dir / "ca"
        ca_cert_dir.mkdir(exist_ok=True, parents=True)
        return ca_cert_dir

    @cached_property
    def ca_cert_path(self) -> Path:
        return self.ca_cert_dir / "ca_cert.pem"

    @cached_property
    def ca_key_path(self) -> Path:
        return self.ca_cert_dir / "ca_key.pem"

    # Server path properties
    @cached_property
    def server_cert_dir(self) -> Path:
        server_cert_dir = self.cert_dir / "server"
        server_cert_dir.mkdir(exist_ok=True, parents=True)
        return server_cert_dir

    @cached_property
    def server_cert_path(self) -> Path:
        return self.server_cert_dir / "server_cert.pem"

    @cached_property
    def server_key_path(self) -> Path:
        return self.server_cert_dir / "server_key.pem"

    # Client cert dirs
    @cached_property
    def client_cert_dirs(self) -> tuple[Path, ...]:
        return (
            self.valid_cert_dir,
            self.expired_cert_dir,
            self.invalid_ca_cert_dir,
            self.invalid_cn_cert_dir,
            self.md5_cert_dir,
            self.unknown_ext_cert_dir,
            self.incorrect_usage_cert_dir,
            self.invalid_san_cert_dir,
            self.invalid_chain_cert_dir,
        )

    # Valid cert path properties
    @cached_property
    def valid_cert_dir(self) -> Path:
        valid_cert_dir = self.cert_dir / "valid"
        valid_cert_dir.mkdir(exist_ok=True, parents=True)
        return valid_cert_dir

    @cached_property
    def valid_cert_path(self) -> Path:
        return self.valid_cert_dir / "cert.pem"

    @cached_property
    def valid_key_path(self) -> Path:
        return self.valid_cert_dir / "key.pem"

    # invalid_ca cert path properties
    @cached_property
    def invalid_ca_cert_dir(self) -> Path:
        invalid_ca_cert_dir = self.cert_dir / "invalid_ca"
        invalid_ca_cert_dir.mkdir(exist_ok=True, parents=True)
        return invalid_ca_cert_dir

    @cached_property
    def invalid_ca_cert_path(self) -> Path:
        return self.invalid_ca_cert_dir / "cert.pem"

    @cached_property
    def invalid_ca_key_path(self) -> Path:
        return self.invalid_ca_cert_dir / "key.pem"

    # invalid_cn cert path properties
    @cached_property
    def invalid_cn_cert_dir(self) -> Path:
        invalid_cn_cert_dir = self.cert_dir / "invalid_cn"
        invalid_cn_cert_dir.mkdir(exist_ok=True, parents=True)
        return invalid_cn_cert_dir

    @cached_property
    def invalid_cn_cert_path(self) -> Path:
        return self.invalid_cn_cert_dir / "cert.pem"

    @cached_property
    def invalid_cn_key_path(self) -> Path:
        return self.invalid_cn_cert_dir / "key.pem"

    # expired cert path properties
    @cached_property
    def expired_cert_dir(self) -> Path:
        expired_cert_dir = self.cert_dir / "expired"
        expired_cert_dir.mkdir(exist_ok=True, parents=True)
        return expired_cert_dir

    @cached_property
    def expired_cert_path(self) -> Path:
        return self.expired_cert_dir / "cert.pem"

    @cached_property
    def expired_key_path(self) -> Path:
        return self.expired_cert_dir / "key.pem"

    # MD5 cert path properties
    @cached_property
    def md5_cert_dir(self) -> Path:
        md5_cert_dir = self.cert_dir / "md5"
        md5_cert_dir.mkdir(exist_ok=True, parents=True)
        return md5_cert_dir

    @cached_property
    def md5_cert_path(self) -> Path:
        return self.md5_cert_dir / "cert.pem"

    @cached_property
    def md5_key_path(self) -> Path:
        return self.md5_cert_dir / "key.pem"

    # Unknown extension cert paths
    @cached_property
    def unknown_ext_cert_dir(self) -> Path:
        unknown_ext_cert_dir = self.cert_dir / "unknown_ext"
        unknown_ext_cert_dir.mkdir(exist_ok=True, parents=True)
        return unknown_ext_cert_dir

    @cached_property
    def unknown_ext_cert_path(self) -> Path:
        return self.unknown_ext_cert_dir / "cert.pem"

    @cached_property
    def unknown_ext_key_path(self) -> Path:
        return self.unknown_ext_cert_dir / "key.pem"

    # Incorrect usage cert paths
    @cached_property
    def incorrect_usage_cert_dir(self) -> Path:
        incorrect_usage_cert_dir = self.cert_dir / "incorrect_usage"
        incorrect_usage_cert_dir.mkdir(exist_ok=True, parents=True)
        return incorrect_usage_cert_dir

    @cached_property
    def incorrect_usage_cert_path(self) -> Path:
        return self.incorrect_usage_cert_dir / "cert.pem"

    @cached_property
    def incorrect_usage_key_path(self) -> Path:
        return self.incorrect_usage_cert_dir / "key.pem"

    # Invalid SAN cert paths
    @cached_property
    def invalid_san_cert_dir(self) -> Path:
        invalid_san_cert_dir = self.cert_dir / "invalid_san"
        invalid_san_cert_dir.mkdir(exist_ok=True, parents=True)
        return invalid_san_cert_dir

    @cached_property
    def invalid_san_cert_path(self) -> Path:
        return self.invalid_san_cert_dir / "cert.pem"

    @cached_property
    def invalid_san_key_path(self) -> Path:
        return self.invalid_san_cert_dir / "key.pem"

    # Invalid chain
    @cached_property
    def invalid_chain_cert_dir(self) -> Path:
        invalid_chain_cert_dir = self.cert_dir / "invalid_chain"
        invalid_chain_cert_dir.mkdir(exist_ok=True, parents=True)
        return invalid_chain_cert_dir

    @cached_property
    def invalid_chain_cert_path(self) -> Path:
        return self.invalid_chain_cert_dir / "cert.pem"

    @cached_property
    def invalid_chain_key_path(self) -> Path:
        return self.invalid_chain_cert_dir / "key.pem"


class spoof:
    def __init__(self, f) -> None:
        self.file = f
        pass

def main(args: list[str]):
    args.pop(0)
    
    cmd = args[0]
    settings = CLIHandler.handle(args)
    ## ============================================================ ##
    if len(args) == 0:
        print("No arguments specified, defaulting to new lab gen...")
        TLSLabTemplate(settings.destination).generate_lab()
        return
    
    if cmd == "gen":
        TLSLabTemplate(generated_dir=settings.destination).generate_lab()
    elif cmd == "grade":
        destination = (settings.input is not None) and settings.input or "./solutions"
        if os.path.exists(destination) == False:
            print("Failed to get solutions folder. Either specify it via ./python main grade [folder path] or drag your solutions folder into the current working directory.")
            return
        # if run locally, should use non random solutions
        template = TLSLabTemplate().generate_lab().solution
        toDelete = f"{os.getcwd()}/temp_solutions.zip"
        shutil.make_archive("temp_solutions", 'zip', base_dir=destination, root_dir=os.getcwd())
        with open(toDelete, "rb") as f:
            print(TLSLabTemplate().grade("", template, spoof(f)))
        os.remove(toDelete)

if __name__ == "__main__":
    main(sys.argv)
