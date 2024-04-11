from frozendict import frozendict

from .RansomwareAndEncryption import Lab2LabTemplate

from .ChecksumLab import Lab3LabTemplate

from .tls import TLSLabTemplate

from .DownloadLab import DownloadLab
lab_templates = (TLSLabTemplate, Lab3LabTemplate, DownloadLab, Lab2LabTemplate)

lab_templates_dict = frozendict({x.lab_template_id: x for x in lab_templates})

__all__ = [
    "lab_templates",
    "lab_templates_dict",
    "TLSLabTemplate",
]
