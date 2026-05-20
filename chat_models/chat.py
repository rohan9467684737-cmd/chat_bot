from dotenv import load_dotenv

load_dotenv()

#from langchain.chat_models import init_chat_model
#model = init_chat_model("google_genai:gemini-2.5-flash-lite")
#print(model)
#response = model.invoke("write 13 tabel in form of 13*1=13 till 10 ")
#print(response.content)

from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model="mistral-small-2506")

response = model.invoke("give a 10 lines on gen-AI")

print(response.content)