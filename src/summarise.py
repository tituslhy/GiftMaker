#%%
import os
from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate
from langchain import HuggingFaceHub
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from hugchat.login import Login
from hugchat import hugchat

def LLM_write(text: str, 
              star: str = None,
              setting: str = 'HugChat'):
    assert setting in ["HuggingFace", "OpenAI", "HugChat"]
    load_dotenv()
    
    if setting == 'HugChat':
        assert star is not None
        # Instantiate chatbot
        email = os.environ["email"]
        password = os.environ["password"]
        sign = Login(email, password)
        cookie_path_dir = "./cookies/"
        if not os.path.exists(cookie_path_dir):
            os.mkdir(cookie_path_dir)
        cookies = sign.login()
        sign.saveCookiesToDir(cookie_path_dir)
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        
        # Create new conversation
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        
        # Get output
        summary = chatbot.chat(f"What are the top adjectives used in the text: {text}")
        PROMPT = f"""Write a funny self-introduction for a job interview referencing the text: {summary}. 
        State your name as {star} and praise yourself for your python and machine learning skills and say that you want marry python as your spouse.
        Add a funny line stating that all other programming languages are horrible.
        Keep your response to between 70-80 words.
        """
        return chatbot.chat(PROMPT, 
                            max_new_tokens = 2048)
        
    else:
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
