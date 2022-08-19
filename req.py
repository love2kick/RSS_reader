import requests

def request(url):
    r=requests.get(url)
    code=r.status_code
    try:
        if code!=200:
            raise ConnectionError
        else:
            return code
    except ConnectionError:
        print(f"Request status code not 200 (code: {code}). Exiting")
        raise SystemExit()
    
def request_content(url):
    r=requests.get(url)
    return r.content