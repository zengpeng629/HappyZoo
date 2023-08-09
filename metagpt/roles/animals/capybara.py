# -*- coding: utf-8 -*-
"""
 @Author: Zeng Peng
 @Date: 2023-08-09 09:15:42
 @Email: zeng.peng@hotmail.com
"""

import asyncio
import shutil
from pathlib import Path

from metagpt.const import WORKSPACE_ROOT
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.actions import Talk
from metagpt.schema import Message

class Capybara(Role):
    def __init__(self, name="Abby",
                 profile="Philosopher",
                 goal="To understand the universe.",
                 constraints="Sometimes you are just too lazy to move, and refuse to argue with others.",
                 n_borg=1):
        super().__init__(name, profile, goal, constraints)
        self._init_actions([Talk])
        self._watch([Talk])
        self.n_borg = n_borg
        self.todos = []
