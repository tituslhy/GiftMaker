#%%
import os
from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate
from langchain import HuggingFaceHub
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
# from langchain.chains.summarize import load_summarize_chain
from langchain.chains import LLMChain
# import textwrap


def LLM_write(text: str, 
              setting: str = 'HuggingFace'):
    assert setting in ["HuggingFace", "OpenAI"]
    load_dotenv()
    if setting == "HuggingFace":
        os.environ['HUGGINGFACEHUB_API_TOKEN'] = os.environ.get('HUGGINGFACE_API_TOKEN')
        # llm = HuggingFaceHub(repo_id = "google/flan-t5-base",
        #                      model_kwargs = {'temperature': 0.90,
        #                                      'max_length': 2048})
        llm = HuggingFaceHub(repo_id = "tiiuae/falcon-7b-instruct",
                             model_kwargs = {'temperature': 0.7,
                                             'max_length': 2048})
    elif setting == "OpenAI":
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        llm = OpenAI(temperature=0, openai_api_key = OPENAI_API_KEY)
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]
    
    prompt_template = """Write a funny happy birthday message
    to Shauna from the following text":
        {text}
    """
    PROMPT = PromptTemplate(template = prompt_template, input_variables=['text'])
    # chain = load_summarize_chain(llm, chain_type = 'stuff', prompt = PROMPT)
    chain = LLMChain(llm = llm, prompt = PROMPT)
    return chain.run(docs)

#%%
if __name__ == "__main__":
    with open("./Tests/happybirthdayscript.txt", "r") as f:
        text = f.read()
    summary = LLM_write(text)
    print(summary)
# %%
