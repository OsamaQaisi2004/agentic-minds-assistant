import os

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub

load_dotenv()

token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not token:
    raise RuntimeError("Set HUGGINGFACEHUB_API_TOKEN in your local .env file.")

llm = HuggingFaceHub(
    huggingfacehub_api_token=token,
    repo_id="tiiuae/falcon-7b-instruct",
)

prompt = PromptTemplate(
    template="Answer this question in detail: {question}",
    input_variables=["question"],
)
chain = LLMChain(prompt=prompt, llm=llm)
print(chain.run(question="Tell me about Amman"))
