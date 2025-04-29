import pytest
from common.requests_util import RequestsUtil

@pytest.fixture(scope="session")
def api_client():
    """全局初始化请求工具"""
    client = RequestsUtil()
    client._force_login()
    yield client
    # 下方可做其它操作，比如清理测试数据