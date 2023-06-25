#%%
import os
from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate
from langchain import HuggingFaceHub
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
# import textwrap


def summarise_text(text: str, setting: str = 'HuggingFace'):
    assert setting in ["HuggingFace", "OpenAI"]
    load_dotenv()
    if setting == "HuggingFace":
        os.environ['HUGGINGFACEHUB_API_TOKEN'] = os.environ.get('HUGGINGFACE_API_TOKEN')
        llm = HuggingFaceHub(repo_id = "google/flan-t5-base",
                             model_kwargs = {'temperature': 0.95,
                                             'max_length': 2048})
        # llm = HuggingFaceHub(repo_id = "tiiuae/falcon-7b",
        #                      model_kwargs = {'temperature': 0.99,
        #                                      'max_length': 2048})
    elif setting == "OpenAI":
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        llm = OpenAI(temperature=0, openai_api_key = OPENAI_API_KEY)
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]
    
    prompt_template = """Summarise the following text:


        {text}


    Summary:"""
    PROMPT = PromptTemplate(template = prompt_template, input_variables=['text'])
    chain = load_summarize_chain(llm, chain_type = 'stuff', prompt = PROMPT)
    return chain.run(docs)

#%%
if __name__ == "__main__":
    with open("./Tests/happybirthdayscript.txt", "r") as f:
        text = f.read()
    summary = summarise_text(text)
    print(summary)
# %%
