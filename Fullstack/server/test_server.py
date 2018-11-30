import os
import tempfile
import pytest
import server
# from flask.ext.testing import TestCase

@pytest.fixture
def client():
  return server.get_app().test_client()

# def test_index(client):
  # res = client.get('/')
  # assert_template_used('')

def test_downloadFile(client):
  res = client.get("/downloadDataFile")
  assert res.get('Content-Disposition') == "attachment; filename=mypic.jpg"


