from src import lab_templates, LabTemplate

import pytest


@pytest.mark.parametrize("LabTemplateCls", lab_templates)
def test_labs(LabTemplateCls: type[LabTemplate], tmp_path):
    """This should definitely be expanded but I'll continue next semester"""

    LabTemplateCls(tmp_path).generate_lab()
