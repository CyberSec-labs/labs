from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines if line and not line.startswith('#') and not line.startswith("-")]

setup(
    name='labs',
    version='0.0.1',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    extras_require={
        'test': [
            "black==23.11.0",
            "pre-commit==3.6.0",
            "types-requests==2.31.0",
            "mypy==1.7.0",
            "tox==4.11.4",
            "pytest-cov==4.1.0",
            "ruff==0.1.7",
        ]
    },
)
