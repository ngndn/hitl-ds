import importlib.util
import json
import logging
import operator
import sys
import time
from multiprocessing import Process

import redis

from typing import List


class ConditionValueInvalid(Exception):
    pass


CONDITION_MAPPERS = {
    'lt': operator.lt,
    'lte': operator.le,
    'eq': operator.eq,
    'gte': operator.ge,
    'gt': operator.gt,
}


class IFTTT:
    """The class to define the if this then that recipe."""
    def __init__(
        self,
        redis_server: str,
        redis_port: int,
        condition_clauses: List[dict],
        target_module_file_path: str,
        target_module_name: str,
        target_function_name: str,
        target_function_params: dict,
        num_repeat_recipe: int,
        num_processes: int,
    ):
        self.redis_server = redis_server
        self.redis_port = redis_port
        self.condition_clauses = condition_clauses
        self.target_module_file_path = target_module_file_path
        self.target_module_name = target_module_name
        self.target_function_name = target_function_name
        self.target_function_params = target_function_params
        self.num_repeat_recipe = num_repeat_recipe
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
        repeat = 0
        while True:
            execute = True

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

                for process in self.processes:
                    process.join()
                    logging.info('Main: execution of the process: %s done', process.name)

                repeat += 1
            else:
                time.sleep(1)
                now = int(time.time())
                if now % 10 == 0:
                    logging.info('Conditions are not met. Waiting')

            if repeat >= self.num_repeat_recipe:
                logging.info('Reached the number of repeat of recipe. Stop.')
                break

    def load_the_target_function(self):
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
    def load_recipe_from_json_file(cls, json_file: str):
        """Loads the recipe from a json file."""
        with open(json_file) as f:
            recipe = json.load(f)
            return cls.load_recipe_from_dict(recipe)
