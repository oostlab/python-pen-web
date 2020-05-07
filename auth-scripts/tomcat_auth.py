import requests
#

url = basicAuthCredentials = ('admin', 'password')
http_timeout = (5, 5)
url = 'http://192.168.2.5:8080/manager'


def check_for_basicauth(url):
    """Checks if the site uses basic Authentication."""
    try:
        response = requests.get(url,
                                timeout=http_timeout)
    except requests.exceptions.Timeout:
        return False
    except requests.exceptions.TooManyRedirects:
        return False
    except requests.exceptions.RequestException:
        return False
    print(response.headers)
    if 'WWW-Authenticate' in response.headers:
        return True
    else:
        return False


if check_for_basicauth(url):
    try:
        # Send HTTP GET request to server and attempt to receive a response
        response = requests.get(url,
                                timeout=http_timeout,
                                auth=basicAuthCredentials)

        auth_header = 'WWW-Authenticate'
        # If the HTTP GET request can be served
        if response.headers[auth_header] == 'Basic realm="Tomcat manager Application"' and response.status_code == 401:
            print('Authentication is succesvol')
        else:
            print('Authentication failed')
    except BaseException as err:
        print('Basic error')
        print(err)
else:
    print('site does not uses basic authentication')

#
