"""The module implements the action model if-this-then-that.

Each action model object (with concrete values of attributes) is called action plan.
"""
import importlib.util
import json
import logging
import operator
import sys
import time
from multiprocessing import Process

import redis

from typing import List, Callable


# Defines the exception used in the action model if-this-then-that
class ConditionValueInvalid(Exception):
    pass


# Defines the condition supported in the action model if-this-then-that
CONDITION_MAPPERS = {
    'lt': operator.lt,
    'lte': operator.le,
    'eq': operator.eq,
    'gte': operator.ge,
    'gt': operator.gt,
}


class IFTTT:
    """Defines the if-this-then-that action model.

    Attributes:
        redis_server (str): A redis server address for communication method.
        redis_port (int): A redis port for communication method.
        condition_clauses (list of dict): A list of condition clauses in dictionary.
        target_module_file_path (str): A module file path contain the function to run.
        target_module_name (str): A name of the to be run module.
        target_function_name (str): A name of the function to run.
        target_function_params (dict): An inputs of the target function in dictionary (key-value).
        num_repeat (int): A number repeat of the action plan.
        num_processes (int): A number process to run the action plan.
        target_function (Callable): A target function to run.
    """
    def __init__(
        self,
        redis_server: str,
        redis_port: int,
        condition_clauses: List[dict],
        target_module_file_path: str,
        target_module_name: str,
        target_function_name: str,
        target_function_params: dict,
        num_repeat: int,
        num_processes: int,
    ):
        self.redis_server = redis_server
        self.redis_port = redis_port
        self.condition_clauses = condition_clauses
        self.target_module_file_path = target_module_file_path
        self.target_module_name = target_module_name
        self.target_function_name = target_function_name
        self.target_function_params = target_function_params
        self.num_repeat = num_repeat
        self.num_processes = num_processes

        # Load the target function by using the importlib and
        #  target_module_file_path and target_function_name
        self.target_function = self.load_the_target_function()
        self.processes = []

        self.redis_client = redis.Redis(
            host=self.redis_server,
            port=self.redis_port
        )

    def run(self):
        """Runs the action plan."""
        repeat = 0
        while True:
            execute = True

            # Checking the conditions through the communication methods (here is Redis)
            for condition_clause in self.condition_clauses:
                condition_variable = condition_clause['condition_variable']
                condition_operator = condition_clause['condition_operator']
                threshold_value = condition_clause['threshold_value']

                condition_value = float(self.redis_client.get(condition_variable))

                if condition_value is None:
                    execute = False

                condition_function = CONDITION_MAPPERS[condition_operator]
                condition_result = condition_function(condition_value, threshold_value)

                if not condition_result:
                    execute = False

            # If the conditions are all met. Run the target function.
            if execute:
                for i in range(self.num_processes):
                    process_name = f'{self.target_function.__name__}-{i + 1}'

                    process = Process(
                        target=self.target_function,
                        kwargs=self.target_function_params,
                        name=process_name
                    )

                    self.processes.append(process)
                    process.start()

                # Waiting for all the processes to end
                for process in self.processes:
                    process.join()
                    logging.info('Main: execution of the process: %s done', process.name)

                repeat += 1
            else:
                # The conditions are not all met. Waiting.
                time.sleep(1)
                now = int(time.time())
                if now % 10 == 0:
                    logging.info('Conditions are not met. Waiting')

            # Stop if the number of repeat times have reached.
            if repeat >= self.num_repeat:
                logging.info('Reached the number of repeat of recipe. Stop.')
                break

    def load_the_target_function(self) -> Callable:
        """Loads the target function from file."""
        spec = importlib.util.spec_from_file_location(
            self.target_module_name,
            self.target_module_file_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[self.target_module_name] = module

        # return function
        return getattr(module, self.target_function_name)

    @classmethod
    def load_recipe_from_dict(cls, recipe_in_dict: dict):
        """Loads the recipe from a dictionary."""
        return cls(**recipe_in_dict)

    @classmethod
    def load_action_plan_from_json_file(cls, json_file: str):
        """Loads the recipe from a json file."""
        with open(json_file) as f:
            recipe = json.load(f)
            return cls.load_recipe_from_dict(recipe)
