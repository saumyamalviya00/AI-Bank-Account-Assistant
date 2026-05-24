from langchain_community.llms import Ollama

llm = Ollama(model="qwen2.5:0.5b")

response = llm.invoke(
    "What is a bank transaction?"
)

print(response)