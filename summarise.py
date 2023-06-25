#%%
import os
from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
import textwrap


def summarise_text(text: str):
    load_dotenv()
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    llm = OpenAI(temperature=0, openai_api_key = OPENAI_API_KEY)
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]
    prompt_template = """Write a funny summary of the following:


        {text}


    Funny summary:"""
    PROMPT = PromptTemplate(template = prompt_template, input_variables=['text'])
    chain = load_summarize_chain(llm, chain_type = 'stuff', prompt = PROMPT)
    return chain.run(docs)

#%%
if __name__ == "__main__":
    with open("./Tests/happybirthdayscript.txt", "r") as f:
        text = f.read()
    summary = summarise_text(text)
# %%
