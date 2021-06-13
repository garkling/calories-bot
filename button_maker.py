from __future__ import annotations
from abc import abstractmethod

from typing import List, Optional
from telethon import Button

from formatter import show_dishes_list
from settings import *


class PageMaker:
    instances = {}

    choice = {'next': 1, 'prev': -1}
    next_btn = ('➡', 'next')
    prev_btn = ('⬅', 'prev')

    @abstractmethod
    def make_page(self, direction=None):
        pass

    def __init__(self, content: List):

        self.pages = self.split_on_pages(content)
        self.current_page: Optional[List[str]] = None
        self.pages_len = len(self.pages)
        self.page_counter = 0
        self.buttons = []

    def make_paginator(self) -> None:
        if self.pages_len > 1:
            prev_page = self.make_inline(*self.prev_btn)
            next_page = self.make_inline(*self.next_btn)
            page_number = self.make_inline(f'{self.page_counter + 1}/{self.pages_len}',
                                           'unused')

            self.buttons.append([prev_page, page_number, next_page])

    def turn_page_over(self, direction: Optional[str]) -> None:
        self.page_counter += self.choice.get(direction, 0)

        if self.page_counter >= self.pages_len:
            self.page_counter = 0
        elif self.page_counter < 0:
            self.page_counter = self.pages_len - 1

        self.current_page = self.pages[self.page_counter]

    @abstractmethod
    def split_on_pages(self, content):
        pass

    @staticmethod
    def make_inline(text: str,
                    data: Optional[str, bytes]) -> Button:

        return Button.inline(text, data)

    @classmethod
    def get_pager(cls, key: int):
        return cls.instances[key] if key in cls.instances else False

    @classmethod
    def create_pager(cls, key: int, content: List):
        pager = cls(content)
        cls.instances[key] = pager

        return pager


class SearchPageMaker(PageMaker):

    def make_page(self, direction=None):
        self.turn_page_over(direction)
        self.buttons = []

        self.make_product_list_buttons()
        self.make_paginator()

        return self.buttons

    def make_product_list_buttons(self):
        for text, data in self.current_page:
            btn = self.make_inline(text, data)
            self.buttons.append([btn])

    def split_on_pages(self, content):
        lim = PRODUCTS_PER_PAGE
        pages = [content[x:x + lim] for x in range(0, len(content), lim)]

        return pages


class DayListPageMaker(PageMaker):

    def make_page(self, direction=None):
        self.turn_page_over(direction)
        self.buttons = []

    def split_on_pages(self, content):
        lim = DISHES_PER_PAGE
        pages = [content[x:x + lim] for x in range(0, len(content), lim)]

        return pages


class DiaryPageMaker(PageMaker):

    def make_page(self, direction=None):
        pass

    def split_on_pages(self, content):
        pass
