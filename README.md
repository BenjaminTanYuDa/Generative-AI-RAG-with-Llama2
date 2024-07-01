# Video Demo
https://github.com/BenjaminTanYuDa/Generative-AI-RAG-with-Llama2/assets/3131019/cc0bdfb5-ead3-4fec-8723-9bc83799694c

# Technology Stack
![image](https://github.com/BenjaminTanYuDa/Generative-AI-RAG-with-Llama2/assets/3131019/dfc73731-ae23-4822-9171-5be8fc12fb24)

# Retrieval Augmented Generation (RAG) Process
![image](https://github.com/BenjaminTanYuDa/Generative-AI-RAG-with-Llama2/assets/3131019/8d7e16ef-cca6-4a41-b242-00ce2480d88f)

# Technology needed for local LLM with RAG
1. Ollama 
(AI tool designed to enable users to set up and execute large language models like Llama 2 locally)

Navigate to https://ollama.com/download. Choose your Operating System.
![image](https://github.com/BenjaminTanYuDa/Generative-AI-RAG-with-Llama2/assets/3131019/b49aa823-1d48-4e2b-8e70-3741c522e4f3)


2. MongoDB Atlas (Database)
- Create MongoDB account
- Insert JSON files into collection
- Create content embeddings 
- Go to MongoDB Atlas Search Tab
  ![image](https://github.com/BenjaminTanYuDa/Generative-AI-RAG-with-Llama2/assets/3131019/51365289-53ad-4fe1-987f-85b9ff7d9583)
- Create Atlas Vector Search and Vector Search Index to parse data in the collection of interest
  ![image](https://github.com/BenjaminTanYuDa/Generative-AI-RAG-with-Llama2/assets/3131019/ad8857f0-d766-4532-8efc-c213fd0819b3)
```
{
  "fields": [
    {
      "numDimensions": 384,
      "path": "content_embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}
```

3. Streamlit (Front-End)
https://docs.streamlit.io/get-started/installation
