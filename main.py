import warnings
warnings.filterwarnings("ignore")
import pickle
import os, os.path
import time, random
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
os.environ["OPENAI_API_KEY"]="XXXXXXXXX"

#Sidebar Details
with st.sidebar:
    # Set the background image
    background_image = """
            <style>
            [data-testid="stAppViewContainer"] > .main {
             background-image: url("https://upload.wikimedia.org/wikipedia/commons/c/cb/Sumatra_PDF_logo.svg");
             background-size: 17vw 20vh;  # This sets the size to cover 20% of the viewport width and height
             background-position: center;  
             background-repeat: no-repeat;
            }
            </style>
            """

    st.markdown(background_image, unsafe_allow_html=True)

    input_style = """
            <style>
            input[type="text"] {
                background-color: transparent;
                color: #a19eae;  // This changes the text color inside the input box
            }
            div[data-baseweb="base-input"] {
                background-color: transparent !important;
            }
            [data-testid="stAppViewContainer"] {
                background-color: transparent !important;
            }
            </style>
            """
    st.title("Interactive QnA Chat Bot")
    st.markdown('''
    # About
    The purpose of this application is to be able to extract & consume any input pdf doc. Tools & technologies used here:
    - Llama2 - https://llama.meta.com/
    - FAISS - https://ai.meta.com/tools/faiss/#:~:text=FAISS%20(Facebook%20AI%20Similarity%20Search,are%20similar%20to%20each%20other.
    - Langchain - https://www.langchain.com/
    ''')
    add_vertical_space(10)
    st.write("Developed by Sayan Roy")



def main():
    st.write('''
    # Chat with the document✨
    ''')

    def response1(response):
        #sa = """Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
        #                incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
        #                nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

    #Upload a PDF Document
    pdf = st.file_uploader("Select a pdf file",type="pdf")

    if pdf is not None:
        text = ""
        pdf_reader = PdfReader(pdf)
        no_of_pages = len(pdf_reader.pages)
        for page in pdf_reader.pages:
            text = text + page.extract_text()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len

        )
        chunks = text_splitter.split_text(text)

        storename = pdf.name[:-4]
        #db.embedding_function

        if os.path.exists(f"{storename}.pkl"):
            with open(f"{storename}.pkl", "rb") as f:
                db = pickle.load(f)
            #st.write(db," Loaded from Disk")
        else:
            # Embeddings
            #api_key = "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"
            embeddings = HuggingFaceEmbeddings()
            db = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f"{storename}.pkl", "wb") as f:
                pickle.dump(db, f)
            #st.write(db," created")

        # Question & Answers
        #llm = CTransformers(
        #    model=r"C:\Users\User\PycharmProjects\003_Streamlit_ChatPdf\llama-2-7b-chat.ggmlv3.q8_0.bin",
        #    model_type="llama",
        #    max_new_token = 64
        #)

        # Set gpu_layers to the number of layers to offload to GPU.
        # Set to 0 if no GPU acceleration is available on your system.
        #llm = CTransformers(
        #        model="TheBloke/Llama-2-7B-Chat-GGUF",
        #        model_type="llama",
        #        max_new_token = 64
        #     )

        # Accept user query
        query = st.text_input("Please ask any question regarding "+storename)
        #openai.api_key='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'
        #st.write(query)
        if query:
            docs = db.similarity_search(query=query, k=3)
            chain = load_qa_chain(OpenAI(), chain_type="stuff")
            response = chain.run(input_documents=docs, question=query)
            st.write_stream(response1(response))






if __name__ == '__main__':
      main()
