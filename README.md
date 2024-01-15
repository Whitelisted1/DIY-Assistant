# DIY-Assistant
 Make your own assistant through the use of LLMs

# Current State
DIY Assistant is still in development, but I hope to make the app usable in a similar manner as the below code:
```python
from helpful_assistant import Assistant

class Model:
    def generate(prompt: str, stream: bool):
        pass # return a generator or a string

    def form_prompt(messages):
        pass # not sure if we want to use. Might get in the way if using an api.


# init the app given a model class
app = Assistant(llm_class=Model, default_stream_response=True)

while True:
    # Gather user input. Could be linked to transcription software, for example
    user_input = input("> ")

    # Allow the LLM to access the modules and actions and get their outputs
    generator = app.generate(user_input, stream=True, allow_action_execution=True)

    # Generate the final output of the model after the data lookups
    for resp in generator:
        print(resp.text, flush=True, end="")
    print()

    # show the data that the model accessed
    print(generator.accessed_actions)

```