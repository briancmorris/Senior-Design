import os
import tempfile
import pytest
import server
import json
import io

'''Test working flow'''
@pytest.fixture
def client():
  return server.get_app().test_client()

'''Test working flow'''
def test_index(client):
  res = client.get("/")
  assert res.status_code == 200

'''Test working flow'''
def test_post1(client):
  res = client.post("/results", data={})
  assert res.status_code == 200

'''Test working flow'''
def test_post2(client):
  files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
  res = client.post('/results', headers={'Content-Type': 'multipart/form-data'}, data={
    'features' : ['Total Links Clicked'],
    'files': files
  })
  print(res.data)
  assert res.status_code == 200


'''Test working flow'''
def test_setup(client):
  res = client.get("/setUp").data
  resObject = json.loads(res)
  print(resObject)
  assert resObject['setup']['models'] == ['adaboost', 'svc', 'knn', 'mlp', 'decision_tree', 'random_forest', 'gaussian_naive_bayes', 'quad_disc_analysis']
  assert resObject['setup']['features'] == ['Email Frequency', 'Total Links Clicked', 'Proportion Opened', 'Emails Received', 'Emails Opened']

