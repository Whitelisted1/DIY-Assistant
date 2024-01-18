from __future__ import annotations
from typing import Union, List, TYPE_CHECKING, Optional, Any
from .conversation import Conversation, Message
from .module import Module
from .stream import Stream

if TYPE_CHECKING:
    from .action import Action


class Assistant:
    def __init__(self, llm_class: object, *args, **kwargs) -> None:
        self.llm = llm_class
        self.conversation_list: List[Conversation] = []
        self.module_list: List[Module] = []

    def get_system_message(self) -> str:
        return f'''This application has different modules and actions. Modules contain actions, and are simply categorizers. Actions are able to be run and information.

Here are your available modules:
```
{self.convert_modules_to_llm_readable()}
```

Do not talk about how you are unable to return real-time information. You must ONLY use modules and actions provided in this conversation. Do not assume there are actions available to you, unless provided in this conversation.'''

    def new_conversation(self, name: str = "Conversation", history: Optional[List[Message]] = None) -> Conversation:
        c = Conversation(name=name, history=history, assistant=self)
        self.conversation_list.append(c)
        return c

    def add_module(self, module: Module) -> None:
        self.module_list.append(module)

    def convert_modules_to_llm_readable(self) -> str:
        return "\n".join([f"{module.name} ({module.definition})" for module in self.module_list])

    def generate(self, conversation: Conversation, stream: bool = False, allow_action_execution: bool = True) -> Union[Stream, str]:
        if allow_action_execution:
            task_output, used_module, used_action = self._app_action_cycle(conversation)

            if task_output is not None:
                conversation.history[-1].content += f"\n\n(An action was run. Action Output: ```{task_output}```. Use this output in your response, if applicable.)"

        # Make a Stream object that adds the generation result to history once it has completed
        output = Stream(self.llm.generate(conversation.history, stream=stream), lambda x: conversation._add_to_history(Message("assistant", "".join(x))))

        return output

    def _app_action_cycle(self, conversation: Conversation) -> List[Union[str, None], Union[Module, None], Union[Action, None]]:
        conversation_history = conversation.history.copy()

        user_query = conversation_history[-1].content.replace("`", "'") # not a great fix ¯\_(ツ)_/¯

        modules_prompt = f'''```{user_query}```\n\nGiven the above query, respond with ONLY the name of the module that you would like to find more information about. Any other text or tokens will break the application. If none of the modules are helpful, respond with EXACTLY "null". If a module is not needed, respond with EXACTLY "null". Do not make up modules.'''
        conversation_history[-1] = Message("user", modules_prompt)

        output = self.llm.generate(conversation_history, stream=False)
        conversation_history.append(Message("assistant", output))
        output = output.strip().lower()

        if output == "null":
            return None, None, None

        active_module = None
        for m in self.module_list:
            if m.name.lower() == output:
                active_module = m
                break

        if active_module is None:
            return None, None, None

        conversation_history.append(Message("user", f'''The "Weather" module has the following actions:\n```\n{m.convert_actions_to_llm_readable()}\n```\n\nRespond with ONLY the name of the action that you would like to execute. Any other text or tokens will break the application. If you do not wish to execute any of the given actions, respond with EXACTLY "null".'''))

        output = self.llm.generate(conversation_history, stream=False)
        conversation_history.append(Message("assistant", output))
        output = output.strip().lower()

        if output == "null":
            return None, active_module, None

        active_action = None
        for a in active_module.actions:
            if a.name.lower() == output:
                active_action = a
                break

        if active_action is None:
            return None, active_module, None

        task_out = active_action.task()

        return str(task_out), active_module, active_action
