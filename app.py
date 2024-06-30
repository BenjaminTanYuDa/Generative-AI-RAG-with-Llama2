# Import User Interface Python Framework
import streamlit as st

# Import Langchain Libraries
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler # Streaming output to the terminal
from langchain_community.llms import Ollama # LLM
from langchain.vectorstores import MongoDBAtlasVectorSearch # Mongo Vector Search / Vector Store
from langchain.embeddings import HuggingFaceEmbeddings # Embedding models from Huggingface
from langchain.prompts import PromptTemplate # Prompt Template to add context
from langchain.chains import ConversationalRetrievalChain # For creating LLM Chain (putting context, )
from langchain.memory import ConversationBufferWindowMemory

# Import Sentence Transformer
from sentence_transformers import SentenceTransformer # Load Sentence transformer library to improve embedding performance

# Import pymongo Libraries
import pymongo

# Import parsing library
from urllib.parse import quote_plus 

# import config
# import pandas as pd
# import json
# import os

username = quote_plus('<ENTER_YOUR_USERNAME>')
password = quote_plus('<ENTER_YOUR_PASSWORD')
cluster = 'cluster0'

mongo_uri = "mongodb+srv://" + username + ":" + password + "@" + cluster + ".ypsyghd.mongodb.net/?retryWrites=true&w=majority&appName=" + cluster
db_name = "<ENTER_YOUR_DB_NAME>"
coll_name = "<ENTER_YOUR_COLLECTION_NAME>"

# initialize db connection
connection = pymongo.MongoClient(mongo_uri)
collection = connection[db_name][coll_name]

# Initialize the SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Initialize text embedding model (encoder)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
index_name = "vector_index"
vector_field_name = "content_embedding"
text_field_name = "content"

# Specify the MongoDB Atlas database and collection for vector search
vectorStore = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embeddings,
    index_name=index_name,
    embedding_key=vector_field_name,
    text_key=text_field_name,
)

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Initialize the LLM
llm = Ollama(model="llama2", 
             callback_manager=callback_manager, 
             temperature=0.1, # Creativity level of LLM)
             verbose=False)

# Context to be added to the prompt
prompt=PromptTemplate(
        input_variables=["chat_history", "question", "context"],
        template="""
        You are the best financial analyst in the market. You are an expert in finding out the companies' outlook and looking at sentiment analysis from the earnings call transcript. 
        From the Earning Call Transcipt, points out key insights that you find positive in the future growth of the company and points out negative sentiments that might arise from the investors during the question and answer  
        Give examples of questions and answers that support your analysis. Answer the questions in a professional and friendly tone.

        chat_history: {chat_history},
        context: {context},
        Human: {question},
        AI:"""
    )

# Retriever that uses a vector store to retrieve documents
retriever = vectorStore.as_retriever() 

# Create the LLM (putting together everything)
llm_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    combine_docs_chain_kwargs={"prompt": prompt},
    memory=ConversationBufferWindowMemory(memory_key="chat_history", k=4)
)

# Streamlit App
def main():
    st.set_page_config(page_title="Stock Stock Financial Analyst Chat", page_icon="🤖", layout="wide")
    st.title("Stock Stock Financial Analyst Chat")
    
    def conversational_chat(query):
        result = llm_chain({"question": query, "chat_history": st.session_state['history']})
        return result["answer"]
       
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Container for the chat history
    response_container = st.container()

    # Container for the user's text input
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder="Talk to the AI financial analyst here...")
            submit_button = st.form_submit_button(label='Send')
            
        if submit_button and user_input:
            output = conversational_chat(user_input)
            st.session_state['history'].append((user_input, output))

    if st.session_state['history']:
        with response_container:
            for query, answer in st.session_state['history']:
                st.write("😰 : " + query)
                st.write("🤖 : " + answer)

if __name__ == "__main__":
    main()