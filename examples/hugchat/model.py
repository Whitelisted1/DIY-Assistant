from typing import Union, List, Generator
import helpful_assistant

# https://github.com/Soulter/hugging-chat-api
from hugchat import hugchat, login


def custom_iterator(iterator: hugchat.Message) -> Generator:
    for m in iterator:
        if m is None: continue
        yield m["token"]


class model:
    """
    A quick example made to show how you could make a model object.
    This example uses ctransformers and the ChatML format
    """

    def __init__(self, EMAIL, PASSWORD):
        sign = login.Login(EMAIL, PASSWORD)
        cookies = sign.login()
        self.chatbot = hugchat.ChatBot(cookies=cookies)

        # login from save file
        # self.chatbot = hugchat.ChatBot(cookie_path=f"usercookies/{EMAIL}.json")

        self.assistant = None

    def set_assistant(self, assistant: helpful_assistant.Assistant):
        self.assistant = assistant

        assistant.event_manager.add_listener("conversation_create", self.on_conversation_create)

    def on_conversation_create(self, conversation: helpful_assistant.Conversation):
        conversation.hugchatobj = self.chatbot.new_conversation(system_prompt=conversation.get_by_role('system')[0].content)
        print("conversation created")

    def _generate(self, conversation: helpful_assistant.Conversation, stream=False):
        return self.chatbot.chat(conversation.get_by_role("user")[-1].get_content(include_action_output=True), conversation=conversation.hugchatobj)

    def generate(self, conversation: helpful_assistant.Conversation, stream=False):
        output = self._generate(conversation, stream)

        if stream:
            return custom_iterator(output)

        return output.wait_until_done()
