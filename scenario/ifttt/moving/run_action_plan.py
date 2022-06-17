"""Runs the action plan in moving data scenario."""
import logging

from action_model.ifttt import IFTTT

# Configs log
logging.basicConfig(
    format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s:%(funcName)s()|%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)


if __name__ == '__main__':
    # Loads the action plan from the action plan file
    moving_action_plan = IFTTT.load_action_plan_from_json_file(
        '../../../action_plan/moving_ifttt.json'
    )
    # Runs the action plan
    moving_action_plan.run()
