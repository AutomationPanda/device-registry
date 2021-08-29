"""
This module provides fixtures for integration tests.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import json
import pytest
import requests
import time


# --------------------------------------------------------------------------------
# Class: BaseUrl
# --------------------------------------------------------------------------------

class BaseUrl:
  
  def __init__(self, base_url):
    self.base_url = base_url
  
  def concat(self, resource):
    return self.base_url + resource


# --------------------------------------------------------------------------------
# Class: User
# --------------------------------------------------------------------------------

class User:

  def __init__(self, username, password):
    self.username = username
    self.password = password


# --------------------------------------------------------------------------------
# Class: TokenHolder
# --------------------------------------------------------------------------------

class TokenHolder:

  def __init__(self, token, start_time):
    self.token = token
    self.start_time = start_time


# --------------------------------------------------------------------------------
# Private Functions
# --------------------------------------------------------------------------------

def _build_user(test_config, index):
  users = test_config['users']
  user = User(users[index]['username'], users[index]['password'])
  return user


# --------------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture(scope='session')
def test_config():
  with open('tests/integration/config.json') as config_json:
    data = json.load(config_json)
  return data


@pytest.fixture
def base_url(test_config):
  return BaseUrl(test_config['base_url'])


@pytest.fixture
def user1(test_config):
  return _build_user(test_config, 0)


@pytest.fixture
def user2(test_config):
  return _build_user(test_config, 1)


@pytest.fixture
def user1_token(base_url, user1):
  url = base_url.concat('/authenticate/')
  auth = (user1.username, user1.password)
  response = requests.get(url, auth=auth)
  data = response.json()

  assert response.status_code == 200
  assert 'token' in data
  return data['token']


@pytest.fixture(scope='session')
def token_holder():
  return TokenHolder(None, None)


@pytest.fixture
def user1_token_shared(test_config, token_holder):
  current_time = time.time()

  if not token_holder.token or current_time - token_holder.start_time >= 3600:    
    base_url = BaseUrl(test_config['base_url'])
    user1 = _build_user(test_config, 0)

    url = base_url.concat('/authenticate/')
    auth = (user1.username, user1.password)
    response = requests.get(url, auth=auth)
    data = response.json()

    assert response.status_code == 200
    assert 'token' in data
    
    token_holder.token = data['token']
    token_holder.start_time = current_time
  
  return token_holder.token
