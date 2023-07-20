import requests


class HttpClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def get(self, path, params=None, headers=None):
        url = self.base_url + path
        response = requests.get(url, params=params, headers=headers)
        if response.status_code >= 400:
            raise Exception(f"GET {url} returned status code {response.status_code}")
        return response

    def post(self, path, data=None, json=None, headers=None):
        url = self.base_url + path
        response = requests.post(url, data=data, json=json, headers=headers)
        if response.status_code >= 400:
            raise Exception(f"POST {url} returned status code {response.status_code}")
        return response

    def put(self, path, data=None, json=None, headers=None):
        url = self.base_url + path
        response = requests.put(url, data=data, json=json, headers=headers)
        if response.status_code >= 400:
            raise Exception(f"PUT {url} returned status code {response.status_code}")
        return response

    def delete(self, path, headers=None):
        url = self.base_url + path
        response = requests.delete(url, headers=headers)
        if response.status_code >= 400:
            raise Exception(f"DELETE {url} returned status code {response.status_code}")
        return response
