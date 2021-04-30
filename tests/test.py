import pytest
import os
import json
import sqlite3
from application import create_app, get_db
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
            
def test_order_total_avg(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/report?date=2019-09-29')
        try:
            data = json.loads(response.data.decode('utf-8'))
            assert int(data['order_total_avg']) == 12515188 
            assert data['order_total_avg'] == 12515188.458531145 
        except json.decoder.JSONDecodeError:
            pytest.fail("JSON Not received")
        except KeyError:
            pytest.fail("JSON Without appropriate data")
       
def test_total_discount_amount(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/report?date=2019-09-29')
        try:
            data = json.loads(response.data.decode('utf-8'))
            assert int(data['total_discount_amount']) == 12999485
            assert data['total_discount_amount'] == 12999485.945880124   # Checks precision levels
        except json.decoder.JSONDecodeError:
            pytest.fail("JSON Not received")
        except KeyError:
            pytest.fail("JSON Without appropriate data")

def test_values_when_date_has_no_orders(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/report?date=2019-02-31')  # This day will have no results as it is not a real day (Feb 31st)
        try:
            data = json.loads(response.data.decode('utf-8'))
            assert data['items'] == 0
            assert data['customers'] == 0
            assert data['order_total_avg'] == 0
            assert data['total_discount_amount'] == 0
        except json.decoder.JSONDecodeError:
            pytest.fail("JSON Not received")
        except KeyError:
            pytest.fail("JSON Without appropriate data")