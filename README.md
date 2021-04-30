# Suade API Project

## Endpoint Layout

### JSON
An example layout of the response will be as follows:
```
{
    "customers": 877,
    "total_discount_amount": 23207660.62,
    "items": 291544,
    "order_total_avg": 14857290.47,
    "discount_rate_avg": 0.15,
    "commissions": {
        "promotions": {
            "1": 30789016.52,
            "3": 8054710.81,
            "2": 20082936.33,
            "5": 22946449.12,
            "4": 27573451.86
        },
        "total": 2532657169.95,
        "order_average": 2743940.59
    }
}
```
__items__ - The total number of items sold on that day.

__customers__ - The total number of customers that made an order that day.

__total_discount_amount__ - The total amount of discount given that day.

__discount_rate_avg__ - The average discount rate applied to the items sold that day.

__order_total_avg__ - The average order total for that day

__commissions : total__ - The total amount of commissions generated that day.

__commissions : order_average__ - The average amount of commissions per order for that day.

__commissions : promotions : x__ The total amount of commissions earned per each promotion (__x__) that day.

# Setup

To Run the given project, simply clone the repository using:

```
git clone https://github.com/harold-williams/suade.git DIRECTION_DIR 
```

Then, install all pip requirements:

```
pip install -r requirements.txt
```

Depending on your Operating System you will have to do the following:

### Windows CMD
```
set FLASK_APP=application
```
### Linux/MacOs
```
export FLASK_APP=hello
```

Now you can run the server (__inside the cloned directory__) using:

```
flask run
```

It will be served at http://127.0.0.1:5000/ - The endpoint resides at http://localhost:5000/api/report
