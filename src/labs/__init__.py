from frozendict import frozendict

from .RansomwareAndEncryptionLab import Lab2LabTemplate

from .ChecksumLab import Lab3LabTemplate

from .TLSLab import TLSLabTemplate

from .DownloadLab import DownloadLab

from .RSALab import RSALabTemplate

lab_templates = (
    TLSLabTemplate,
    Lab3LabTemplate,
    DownloadLab,
    Lab2LabTemplate,
    RSALabTemplate,
)

lab_templates_dict = frozendict({x.lab_template_id: x for x in lab_templates})

__all__ = [
    "lab_templates",
    "lab_templates_dict",
    "TLSLabTemplate",
]


"""
# Lab Index
TLS Lab = 0
DownloadLab = 1
Ransomware and Encryption Lab = 2
ChecksumLab = 3
RSALab = 4
Password Lab = 5
"""
