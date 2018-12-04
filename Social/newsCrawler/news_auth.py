import os
from dotenv import load_dotenv
from requests.auth import AuthBase

class NewsAuth(AuthBase):
    """
    This class is responsible for perfoming an authentication with newsapi
    The api key has to be specified in a .env file
    """

    def __init__(self):
        """
        loads the .env and the included api key
        """
        load_dotenv('.env')
        self.NEWS_API_KEY = os.getenv('NEWS_API_KEY')


    def __call__(self, request):
        """
        Adds auth header
        :param request:
        :return:
        """
        request.headers.update(get_auth_headers(self.NEWS_API_KEY))
        return request

def get_auth_headers(key):
    """
    Returns the auth header
    :param key:
    :return: Dict The auth header
    """
    return {
        'Content-Type': 'Application/JSON',
        'Authorization': key
    }