import helpful_assistant

# local files
import model, add_modules

llm = model.model(r"C:\Users\dacoo\Offline Documents\llm_models\dolphin-2.6-mistral-7b.Q4_K_M.gguf")

app = helpful_assistant.Assistant(llm)
add_modules.init(app)

conversation = app.new_conversation()

while True:
    for m in conversation.history:
        print(f"{m.role:-^20}\n{m.content}\n---------------------")
        print()
    out = conversation.generate(input("> "), stream=True)

    for resp in out:
        print(resp, end="", flush=True)
    print()

# https://hf.co/chat/r/5JRvkmF
