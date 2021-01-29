from aiogram.utils.helper import Helper, HelperMode, ListItem


class TestStates(Helper):
    mode = HelperMode.snake_case

    Q1 = ListItem()
    Q2 = ListItem()
