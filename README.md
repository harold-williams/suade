# Suade API Project

1. Endpoint Layout
2. Setup
3. If I had more time


## Endpoint Layout
<a name="section-1"></a> 

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

<a name="section-2"></a> 
To Run the given project, simply clone the repository using:

```
git clone https://github.com/harold-williams/suade.git DESTINATION_DIR 
```
Change directory into the newly created directory:

```
cd DESTINATION_DIR
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
export FLASK_APP=application
```

Now you can run the server (__inside the cloned directory__) using:

```
flask run
```

It will be served at http://127.0.0.1:5000/ - The endpoint resides at http://localhost:5000/api/report

## Future Extensions

As advised I only spent the time designated on this task and would like to describe a few things I would've done time permitting:

Created more test cases and done more manual calculations. I created my test cases by querying the SQL database, however would have liked to double check these myself manually checking the numbers to understand whether the precision was completely correct. I also would have liked to create more edge cases to check for errors.

Refactored my code to be divided into smaller functions. I would have liked to make a report object more polished and created smaller functions for the whole codebase to serpate out purposes. I would have also liked to add greater comments to explain different components in more depth.

Finally, if the dataset was larger I could have used a database server or integrated SQLAlchemy into my program, however it wasn't necessary in order to complete the task, however could be done in future. I could have also added more setting configurations if needed.

