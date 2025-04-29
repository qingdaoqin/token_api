from http.client import responses

import requests
from threading import Lock
from config.env_config import ENV

class RequestsUtil:
    _instance_lock = Lock() # 单例模式锁

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                cls._instance = super(RequestsUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.base_url = ENV.BASE_URL

    def _force_login(self):
        """token失效进行强制重登"""
        login_url = f"{self.base_url}/api/auth/login"
        resp = self.session.post(
            login_url,
            json={"username": ENV.TEST_USER, "passwd": ENV.TEST_PASSWORD}
        ).json()
        self.token = resp["token"]
        return self.token

    def request(self, method, path, **kwargs):
        """统一请求入口"""
        url = f"{self.base_url}{path}"
        headers = kwargs.get("headers", {})
        if self.token:  # 自动添加上token
            headers.update({"Authorization": f"Bearer {self.token}"})

        response = self.session.request(method, url, headers=headers, **kwargs)

        # 处理token失效
        if response.status_code == 401 and "login" not in path:
            self._force_login()
            return self.request(method, path, **kwargs)

        return response
        
