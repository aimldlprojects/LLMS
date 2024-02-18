
# langchain_per_user_retrieval
ref: https://github.com/sugarforever/Advanced-RAG/blob/main/04_langchain_per_user_retrieval.ipynb
loader = PyPDFLoader("electronic-health-records.pdf")
documents = loader.load_and_split()
#add document per user in pine cone
vectorstore.add_documents(documents, namespace=USER_1)
retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"namespace": USER_1, "score_threshold": .9})
relevant_documents = retriever.get_relevant_documents(question)


