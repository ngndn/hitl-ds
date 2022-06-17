"""Runs the action plan in streaming data scenario."""
import logging

from action_model.ifttt import IFTTT


# Configs the log
logging.basicConfig(
    format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s:%(funcName)s()|%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)


if __name__ == '__main__':
    # Loads the action plan from file
    streaming_action_plan = IFTTT.load_action_plan_from_json_file(
        '../../../action_plan/streaming_ifttt.json'
    )
    # Runs the action plan
    streaming_action_plan.run()
