#%%
import os
from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate
from langchain import HuggingFaceHub
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def LLM_write(text: str, 
              setting: str = 'HuggingFace'):
    assert setting in ["HuggingFace", "OpenAI"]
    load_dotenv()
    if setting == "HuggingFace":
        os.environ['HUGGINGFACEHUB_API_TOKEN'] = os.environ.get('HUGGINGFACE_API_TOKEN')
        llm = HuggingFaceHub(repo_id = "tiiuae/falcon-7b-instruct",
                             model_kwargs = {'temperature': 0.9,
                                             'max_length': 512})
    elif setting == "OpenAI":
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        llm = OpenAI(temperature=0, openai_api_key = OPENAI_API_KEY)
        
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]
    
    prompt_template = """Write a message appreciating a friend
    from the following text":
    
    
        {text}
        
    """
    PROMPT = PromptTemplate(template = prompt_template, input_variables=['text'])
    chain = LLMChain(llm = llm, prompt = PROMPT)
    if setting == "OpenAI":
        return chain.run(docs)
    else: #HuggingFace models might not work if max API calls are exceeded.
        try:
            chain = LLMChain(llm = llm, prompt = PROMPT)
        except:
            llm = HuggingFaceHub(repo_id="google/flan-t5-base")
            chain = LLMChain(llm = llm, prompt = PROMPT)
            return chain.run(docs)

#%%
if __name__ == "__main__":
    with open("./Tests/happybirthdayscript.txt", "r") as f:
        text = f.read()
    summary = LLM_write(text)
    print(summary)
# %%
