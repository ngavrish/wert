import pytest
from utils.utils import get_config_dict


@pytest.fixture(scope="session",autouse=True)
def env_config(request):
    """
    Config fixture
    :param request:
    :return: Dict
    """
    return get_config_dict()
