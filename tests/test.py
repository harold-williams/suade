import pytest
import os
import json
from application import create_app
from flask import request

@pytest.fixture
def app():
    application = create_app()
    return application

def test_no_date(app):
    
    with app.test_client() as test_client:
        response = test_client.get('/api/report')
        assert b"No Date Provided" in response.data
        assert b"Example Query:" in response.data
        
def test_invalid_date(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/report?date=abc')
        assert b"Invalid Date" in response.data
        assert b"Format: YYYY-MM-DD" in response.data

def test_invalid_date_format(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/report?date=2019/01/02')
        assert b"Invalid Date" in response.data
        assert b"Format: YYYY-MM-DD" in response.data
        
def test_customers_count(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/report?date=2019-09-29')
        try:
            data = json.loads(response.data.decode('utf-8'))
            assert data['customers'] == 5
        except json.decoder.JSONDecodeError:
            pytest.fail("JSON Not received")
        except KeyError:
            pytest.fail("JSON Without appropriate data")
            
       
def test_order_count(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/report?date=2019-09-29')
        try:
            data = json.loads(response.data.decode('utf-8'))
            assert data['items'] == 63
        except json.decoder.JSONDecodeError:
            pytest.fail("JSON Not received")
        except KeyError:
            pytest.fail("JSON Without appropriate data")
            
