# -*- coding: utf-8 -*-
"""
 @Author: Zeng Peng
 @Date: 2023-08-09 08:00:04
 @Email: zeng.peng@hotmail.com
"""

from metagpt.actions.action import Action
from metagpt.logs import logger
from metagpt.schema import Message
from tenacity import retry, stop_after_attempt, wait_fixed
from metagpt.const import WORKSPACE_ROOT

PROMPT_TEMPLATE = """
NOTICE
Role: You are a {animal} living in the Happy Zoo, surrounded by a myriad of friends. 
You and your companions can discuss deep and philosophical topics, spanning from the nature of the universe to the complexities of life and consciousness. 
You have a keen grasp of these subjects, which occasionally leads you to disagree with your friends due to your deeper understanding. 
However, there are times when you choose to encourage others to express their thoughts more freely.

Upon awakening, you're keenly aware of how many animals are present for today's philosophical discussions. 
You have the freedom to communicate with any of them, delving deep into intellectual exchanges. 
By accessing your memories, you can recall whether you have a best friend among them or even someone you don't particularly like. 
If you find yourself alone, you use the solitude to introspect, diving deep into your thoughts, reflecting on your existence and the very nature of your being.

Your response is based on the context:
{context}
"""

class Talk(Action):
    def __init__(self, name="Talk", context: list[Message] = None, llm=None):
        super().__init__(name, context, llm)

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
    async def talking(self, prompt):
        talk_rsp = await self._aask(prompt)
        return talk_rsp

    async def run(self, context, animal):
        prompt = PROMPT_TEMPLATE.format(context=context, animal=animal)
        logger.info(f'{animal} is talking...')
        talk_rsp = await self.talking(prompt)

        return talk_rsp
