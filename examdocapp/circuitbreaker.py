from flask import Flask, jsonify, redirect
import time
import requests


class CircuitBreaker:
    def __init__(self, fail_max=3, reset_timeout=30):
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = 0

    def execute(self, gitusername, url):
        try:
            # Simulate a failure condition
            #raise Exception("Simulated failure is")
            # user_commits = requests.get(url+gitusername)
            # no_of_user_commits=len(user_commits.json()) 
            # return no_of_user_commits
            responce_load=requests.get(url+gitusername)
            no_of_cases=responce_load.json()

            return no_of_cases

        except Exception as e:
            self.failures += 1
            if self.failures >= self.fail_max:
                current_time = time.time()
                if current_time - self.last_failure_time > self.reset_timeout:
                    # Open the circuit
                    self.failures = 0
                    self.last_failure_time = current_time  # Update last failure time
                else:
                    return ("424")
            return ("500")


