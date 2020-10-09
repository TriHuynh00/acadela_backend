import requests
import json
class HttpRequest():
    apiVersion = "api/v1/"
    sacmUrl = "http://localhost:8084/" + apiVersion
    sociocortexUrl = "http://localhost:8083/" + apiVersion
    defaultHeader = {
        "Content-Type": "application/json",
        "Authorization": "Basic bXVzdGVybWFubkB0ZXN0LnNjOm90dHRv"
    }

    simulateUserHeader = {
        "Content-Type": "application/json",
        "simulateuser": "mustermann@test.sc"
    }


    def get(baseUrl, requestUrl, header = defaultHeader, body = None):

        r = requests.get(
            baseUrl + requestUrl,
            headers = header,
            json = body)

        return r.json();

    def post(baseUrl, requestUrl, header = defaultHeader, body = None):
        # print("body = ", json.loads(body))
        r = requests.post(
            baseUrl + requestUrl,
            headers=header,
            json=json.loads(json.dumps(body)))
        # print (r.json())
        return r.json();