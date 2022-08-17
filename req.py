import requests

def request(url):
    r=requests.get(url)
    try:
        if r.status_code!=200:
            raise ConnectionError
        else:
            return r.status_code
    except ConnectionError:
        print("Request status code not 200.")
        raise SystemExit()
    
def request_content(url):
    r=requests.get(url)
    return r.content