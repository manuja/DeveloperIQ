# app.py

from flask import Flask, jsonify, redirect
from product_service import product_api
from auth_service import auth_api
from user_service import user_api
from metrics_service import metrics_api
from viewmetrics_service import view_metrics_api
import time
import requests


app = Flask(__name__)


app.register_blueprint(product_api)
app.register_blueprint(auth_api)
app.register_blueprint(user_api)
app.register_blueprint(metrics_api)
app.register_blueprint(view_metrics_api)

class CircuitBreaker:
    def __init__(self, fail_max=3, reset_timeout=30):
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = 0

    def execute(self, gitusername):
        try:
            # Simulate a failure condition
            #raise Exception("Simulated failure is")
            user_commits = requests.get('https://api.github.com/repos/manuja/LASMS/commits?author='+gitusername)
            no_of_user_commits=len(user_commits.json()) 
            return str(no_of_user_commits)
        except Exception as e:
            self.failures += 1
            if self.failures >= self.fail_max:
                current_time = time.time()
                if current_time - self.last_failure_time > self.reset_timeout:
                    # Open the circuit
                    self.failures = 0
                    self.last_failure_time = current_time  # Update last failure time
                else:
                    return jsonify(error="Circuit is open"), 500
            return jsonify(error=str(e)), 500


breaker = CircuitBreaker()

# def greeting():
#     return jsonify(message="Hello, Circuit Breaker!")


@app.route('/')
def hello_world():
       return breaker.execute("manuja")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)