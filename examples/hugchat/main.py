import helpful_assistant

# local files
import model, add_modules

# define EMAIL and PASSWORD constants
EMAIL = ""
PASSWORD = ""

# make the model
llm = model.model(EMAIL, PASSWORD)

app = helpful_assistant.Assistant(llm)
add_modules.init(app)

# set an assistant object for the llm
# this allows for the model.py file to add listeners
llm.set_assistant(app)

# make a new conversation
conversation = app.new_conversation()

# preset messages to test the model
messages = ["Hi! How are you?", "What is the weather right now?", "How are you?"]
for i in range(len(messages)):
    out = conversation.generate(messages[i], stream=True, allow_action_execution=True)

    for resp in out:
        print(resp, end="", flush=True)
    print()
