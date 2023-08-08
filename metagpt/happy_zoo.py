# -*- coding: utf-8 -*-
"""
 @Author: Zeng Peng
 @Date: 2023-08-08 12:52:56
 @Email: zeng.peng@hotmail.com
"""

from pydantic import BaseModel, Field

from metagpt.environment import Environment
from metagpt.roles import Role
from metagpt.utils.common import NoMoneyException
from metagpt.schema import Message
from metagpt.actions import BossRequirement
from metagpt.config import CONFIG
from metagpt.logs import logger

class HappyZoo(BaseModel):
	"""
	Happy Zoo: a place holds all the animals and their activatives.
	"""
	environment: Environment = Field(default_factory=Environment)
	happy_topic: str = Field(default="") # A topic that animals will discuss.
	investment: float = Field(default=1.0) # You will pay to see those animals talk!

	class Config:
		arbitrary_types_allowed = True
	
	def invite(self, animals: list[Role]):
		"""
		Invite those animals to join the Happy Zoo.
		"""
		self.environment.add_roles(animals)
    
	def invest(self, investment: float):
		"""
        You should pay for them.
	    raise NoMoneyException when exceed max_budget.
		"""
		self.investment = investment
		CONFIG.max_budget = investment
		logger.info(f'Investment: ${investment}.')

	def _check_balance(self):
		if CONFIG.total_cost > CONFIG.max_budget:
			raise NoMoneyException(CONFIG.total_cost, f'Insufficient funds: {CONFIG.max_budget}')
		
	def start_topic(self, happy_topic):
		"""
		It's time to start a topic.
		"""
		self.happy_topic = happy_topic
		self.environment.publish_message(Message(role="Visitor", content=happy_topic, cause_by=BossRequirement))
	
	def _save(self):
		logger.info(self.json())
	
	async def run(self, n_round=3):
		"""
		Animals in the Happy Zoo are starting their activitives.
		And will stop when out of funding.
		"""
		while n_round > 0:
			n_round -= 1
			logger.debug(f"{n_round=}")
			self._check_balance()
			await self.environment.run()
		
		return self.environment.history

