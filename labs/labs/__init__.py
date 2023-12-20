from frozendict import frozendict

from .tls import TLSLabTemplate

lab_templates = (TLSLabTemplate,)

lab_templates_dict = frozendict({x.lab_template_id: x for x in lab_templates})

__all__ = [
    "lab_templates",
    "lab_templates_dict",
    "TLSLabTemplate",
]
