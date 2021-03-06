import json
import re
from django.conf import settings
import requests
from webui.exceptions import BadRequestException, UnauthorizedException, ServerErrorException, RedirectException, \
    UnexpectedException, LocationHeaderNotFoundException, NotFoundException


def validate_response(response):
    if 200 <= response.status_code < 300:
        return True
    return False


def status_code_to_exception(status_code):
    if status_code == 400:
        return BadRequestException()
    if status_code == 401:
        return UnauthorizedException()
    if status_code == 404:
        return NotFoundException()
    if status_code >= 500:
        return ServerErrorException()
    if 300 <= status_code < 400:
        return RedirectException()
    return UnexpectedException()


def get_resource_id_or_raise_exception(resource_name, response):
    if not validate_response(response):
        exception = status_code_to_exception(response.status_code)
        exception.message = response.text
        raise exception
    location = response.headers.get('location')
    pattern = '.+{}\/(?P<id>\w+)'.format(resource_name)
    p = re.compile(pattern)
    m = p.match(location)
    try:
        resource_id = m.group('id')
        return resource_id
    except:
        return UnexpectedException('Could not get the resource ID from the response.')


class Base(object):
    def __init__(self, auth_token=None):
        self.auth_token = auth_token

    def get_url(self, extra=''):
        return '{base_url}{endpoint}{extra}'.format(base_url=settings.API_BASE_URL,
                                                    endpoint=object.__getattribute__(self, '__endpoint__'),
                                                    extra=extra)


class Session(Base):
    __endpoint__ = '/session/'
    __resourcename__ = 'session'

    def create(self, data):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        resource_id = get_resource_id_or_raise_exception(self.__resourcename__, response)
        return resource_id

    def get(self, resource_id):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        session = json.loads(response.text)
        return session

    def start(self, resource_id):
        url = self.get_url(extra='{}/{}/'.format(resource_id, 'start'))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.post(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception

    def stop(self, resource_id):
        url = self.get_url(extra='{}/{}/'.format(resource_id, 'stop'))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.post(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception


class TestPlan(Base):
    __endpoint__ = '/testplan/'
    __resourcename__ = 'testplan'

    def create(self, data):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        resource_id = get_resource_id_or_raise_exception(self.__resourcename__, response)
        return resource_id

    def update(self, resource_id, data):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.put(url, headers=headers, data=json.dumps(data))
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception

    def get(self, resource_id):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        testplan = json.loads(response.text)
        return testplan

    def get_all(self):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        testplans = json.loads(response.text)
        return testplans

    def delete(self, resource_id):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.delete(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception


class Rule(Base):
    __endpoint__ = '/testplan/{testplan_id}/rule/'
    __resourcename__ = 'rule'

    def __init__(self, testplan_id, auth_token=None):
        self.auth_token = auth_token
        self.__endpoint__ = self.__endpoint__.format(testplan_id=testplan_id)

    def create(self, data):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        resource_id = get_resource_id_or_raise_exception(self.__resourcename__, response)
        return resource_id

    def update(self, resource_id, data):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.put(url, headers=headers, data=json.dumps(data))
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception

    def get(self, resource_id):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        rule = json.loads(response.text)
        return rule

    def get_all(self):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        resource = json.loads(response.text)
        return resource


class Recording(Base):
    __endpoint__ = '/recording/'
    __resourcename__ = 'recording'

    def create(self, data):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        resource_id = get_resource_id_or_raise_exception(self.__resourcename__, response)
        return resource_id

    def get(self, resource_id):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        recording = json.loads(response.text)
        return recording

    def get_all(self):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        recordings = json.loads(response.text)
        return recordings

    def update(self, resource_id, data):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.put(url, headers=headers, data=json.dumps(data))
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception

    def start(self, resource_id):
        url = self.get_url(extra='{}/{}'.format(resource_id, 'start'))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.post(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception

    def stop(self, resource_id):
        url = self.get_url(extra='{}/{}'.format(resource_id, 'stop'))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.post(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception


class QoS(Base):
    __endpoint__ = '/qos/'
    __resourcename__ = 'qos'

    def create(self, data):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        resource_id = get_resource_id_or_raise_exception(self.__resourcename__, response)
        return resource_id

    def update(self, resource_id, data):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.put(url, headers=headers, data=json.dumps(data))
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception

    def get(self, resource_id):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        qos = json.loads(response.text)
        return qos

    def get_all(self):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        qos = json.loads(response.text)
        return qos

    def delete(self, resource_id):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.delete(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception


class ServerOverload(Base):
    __endpoint__ = '/serveroverload/'
    __resourcename__ = 'serveroverload'

    def create(self, data):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        resource_id = get_resource_id_or_raise_exception(self.__resourcename__, response)
        return resource_id

    def update(self, resource_id, data):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.put(url, headers=headers, data=json.dumps(data))
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception

    def get(self, resource_id):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        profile = json.loads(response.text)
        return profile

    def get_all(self):
        url = self.get_url()
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        profile = json.loads(response.text)
        return profile

    def delete(self, resource_id):
        url = self.get_url(extra=str(resource_id))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.delete(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception


class Logs(Base):
    __endpoint__ = '/log/'
    __resourcename__ = 'log'

    def stats(self):
        url = self.get_url(extra='stats')
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        stats = json.loads(response.text)
        return stats

    def get(self, start, length, component, levels, date_from, date_to, msg):
        url = self.get_url(
            extra='?start={}&limit={}&component={}&levels={}&from={}&to={}&msg={}'.format(start, length, component,
                                                                                          levels,
                                                                                          date_from, date_to, msg))
        headers = {'X-Auth-Token': self.auth_token}
        response = requests.get(url, headers=headers)
        if not validate_response(response):
            exception = status_code_to_exception(response.status_code)
            exception.message = response.text
            raise exception
        logs = json.loads(response.text)
        return logs