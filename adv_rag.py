
# langchain_per_user_retrieval
ref: https://github.com/sugarforever/Advanced-RAG/blob/main/04_langchain_per_user_retrieval.ipynb
loader = PyPDFLoader("electronic-health-records.pdf")
documents = loader.load_and_split()
vectorstore.add_documents(documents, namespace=USER_1)

