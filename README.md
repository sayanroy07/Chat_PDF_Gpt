# Chat_PDF_Gpt
This repository has all details to create an application using Streamlit with LLM &amp; importing external PDFs.
All you need to do is bring in any PDF file, & with the gpt 3.5 turbo model we can do question/answering.
Now, lets talk about the process flow:
  - import any pdf file & read the content, keep as text tokens/documents
  - bring in any Vector Database, we have used FAISS
  - use langchain to merge, LLM eg, OpenAIs GPT with the embedded Vector database
  - Use a new chain to intake user queries & eventually do a similarity check with the vector database using LLM
![1](https://github.com/sayanroy07/Chat_PDF_Gpt/assets/39030649/6c10f365-f9f1-4d04-9158-1435de20c75e)

![2](https://github.com/sayanroy07/Chat_PDF_Gpt/assets/39030649/a15e02ff-420a-4efa-b56e-fba68e698902)

![3](https://github.com/sayanroy07/Chat_PDF_Gpt/assets/39030649/abd47056-ef34-4138-a5eb-f6990a8b9e8d)
