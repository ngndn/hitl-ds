import logging

from recipe.ifttt import IFTTT


logging.basicConfig(
    format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s:%(funcName)s()|%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)


if __name__ == '__main__':
    ifttt_recipe = IFTTT.load_recipe_from_json_file('../../../config/moving_ifttt_config.json')
    ifttt_recipe.run()
