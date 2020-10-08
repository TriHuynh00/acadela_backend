import requests

class HttpRequest():
    apiVersion = "api/v1/"
    sacmUrl = "http://localhost:8084/" + apiVersion
    sociocortexUrl = "http://localhost:8083/" + apiVersion
    defaultHeader = {
        "Content-Type": "application/json",
        "Authorization": "Basic bXVzdGVybWFubkB0ZXN0LnNjOm90dHRv"
    }


    def get(baseUrl, requestUrl, header = defaultHeader, body = None):

        r = requests.get(
            baseUrl + requestUrl,
            headers = header,
            json = body)

        return r.json();