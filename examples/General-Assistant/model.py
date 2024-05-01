from ctransformers import AutoModelForCausalLM
import torch
from typing import Union, List
import helpful_assistant


class model:
    """
    A quick example made to show how you could make a model object.
    This example uses ctransformers and the ChatML format
    """

    def __init__(self, model_path: str):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        self.model = AutoModelForCausalLM.from_pretrained(model_path, gpu_layers=35, context_length=10000)

        # stop sequences for ChatML
        self.stop_sequences = [
            "<|im_end|>"
        ]

    # generate the output
    def generate(self, conversation: helpful_assistant.Conversation, *args, **kwargs):
        # a high level function for simplicity
        return self.model(
            self.form_prompt(conversation.history),
            stop=self.stop_sequences,
            *args,
            **kwargs
        )

    # forms a prompt. In this case the format is ChatML
    def form_prompt(self, messages: List[helpful_assistant.Message], add_assistant_preprompt=True) -> str:
        """ChatML format
        <|im_start|>system
        {system_message}<|im_end|>
        <|im_start|>user
        {prompt}<|im_end|>
        <|im_start|>assistant
        """

        out_prompt = ""
        for message in messages:
            out_prompt += f"<|im_start|>{message.role}\n{message.get_content(include_action_output=True)}<|im_end|>\n"

        if add_assistant_preprompt:
            out_prompt += "<|im_start|>assistant\n"

        return out_prompt
