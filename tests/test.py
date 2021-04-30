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
       
def test_discount_rate_avg(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/report?date=2019-09-29')
        try:
            data = json.loads(response.data.decode('utf-8'))
            assert int(data['discount_rate_avg']*100) == 17           # Checking first 2 decimal places
            assert data['discount_rate_avg'] == 0.17648554006271688   # Checks precision levels
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
            
def test_commission_total(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/report?date=2019-09-29')
        try:
            data = json.loads(response.data.decode('utf-8'))
            assert int(data['commissions']['total']) == 8787396
            assert data['commissions']['total'] == 8787396.853026928   # Checks precision levels
        except json.decoder.JSONDecodeError:
            pytest.fail("JSON Not received")
        except KeyError:
            pytest.fail("JSON Without appropriate data")
            
def test_commission_average(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/report?date=2019-09-29')
        try:
            data = json.loads(response.data.decode('utf-8'))
            assert int(data['commissions']['order_average']) == 155764
            assert data['commissions']['order_average'] == 155764.04473993252   # Checks precision levels
        except json.decoder.JSONDecodeError:
            pytest.fail("JSON Not received")
        except KeyError:
            pytest.fail("JSON Without appropriate data")
            
def test_promotion_commission(app):
    with app.test_client() as test_client:
        response = test_client.get('/api/report?date=2019-09-29')
        try:
            data = json.loads(response.data.decode('utf-8'))
            for i in range(1,6):    # Yields only possible values 1-5, would change this to not be hardcoded given more time
                if i in [1,2,4]:
                    assert int(data['commissions']['promotions'][str(i)]) == 0
                elif i == 3:
                    assert int(data['commissions']['promotions'][str(i)]) == 2315809
                    assert data['commissions']['promotions'][str(i)] == 2315809.798012205   # Checks precision levels
                else: # i = 5
                    assert int(data['commissions']['promotions'][str(i)]) == 3099795
                    assert data['commissions']['promotions'][str(i)] == 3099795.0700236196   # Checks precision levels
                    
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
            assert data['discount_rate_avg'] == 0
            assert data['commissions']['total'] == 0
            assert data['commissions']['order_average'] == 0
            for i in range(1,6):    # Yields only possible values 1-5, would change this to not be hardcoded given more time
                assert int(data['commissions']['promotions'][str(i)]) == 0
        except json.decoder.JSONDecodeError:
            pytest.fail("JSON Not received")
        except KeyError:
            pytest.fail("JSON Without appropriate data")