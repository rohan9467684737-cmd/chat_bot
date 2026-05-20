from dotenv import load_dotenv
import os

load_dotenv()

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

print(os.getenv("HUGGINGFACEHUB_API_TOKEN"))

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1"
)

model = ChatHuggingFace(llm=llm)

response = model.invoke("hey")

print(response.content)