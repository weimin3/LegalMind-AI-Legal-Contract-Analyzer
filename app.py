from PyPDF2 import PdfReader
import streamlit as st
from knowledge_base import KnowledgeBaseService
from rag import RagService
from io import BytesIO
import config


st.set_page_config(page_title = "LegalMind",layout="wide")
st.title("LegalMind: AI Legal Contract Analyzer")
st.divider()

# initialize knowledgebase

if "kb_service" not in st.session_state:
    st.session_state["kb_service"] = KnowledgeBaseService()

if "rag_service"  not in st.session_state:
    st.session_state["rag_service"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "collection_name" not in st.session_state:
    st.session_state["collection_name"] = None

if "contract_summary" not in st.session_state:
    st.session_state["contract_summary"] = None

# left: upload + summary  right: chat
left_col, right_col = st.columns([1,1])

with left_col:
    st.subheader("Upload Contract")

    uploaded_file = st.file_uploader(
        "Upload a contract",
        type= ["txt","pdf"],
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_size = uploaded_file.size/1024
        file_type = uploaded_file.type
        st.write(f"{file_name} : {file_size:.2f} KB")

        file_content = uploaded_file.getvalue()

        if st.button("Analyze Contract"):
            with st.spinner("Uploading and analyzing....."):
                if file_type == "text/plain":
                    data = file_content.decode("utf-8")
                elif file_type == "application/pdf":
                        pdf_reader = PdfReader(BytesIO(file_content))
                        data = ""
                        for page in pdf_reader.pages:
                            text = page.extract_text()
                            if text:
                                data += text

                collection_name, upload_msg = st.session_state["kb_service"].upload_contract(data, file_name)


                if collection_name is not None:
                    st.session_state["collection_name"] = collection_name
                    st.session_state["rag_service"] = RagService(collection_name)

                    session_config = {
                        "configurable": {
                            "session_id": collection_name  # 基于合同的唯一标识
                        }
                    }
                    st.session_state["session_config"] = session_config

                    st.session_state["messages"] = [
                        {"role": "assistant", 
                        "content": f"{file_name} has been analyzed, you can ask me anything about the contract"}
                    ]

                    # 5. auto extract key information
                    summary_prompt = """Please analyze this contract and provide a structured summary with the following:

                        1. **Parties Involved**: Who are the contracting parties?
                        2. **Contract Type**: What type of contract is this?
                        3. **Key Obligations**: What are the main obligations of each party?
                        4. **Important Dates**: Any deadlines, expiration dates, or key milestones?
                        5. **Financial Terms**: Any payment terms, amounts, or penalties?
                        6. **Termination Conditions**: How can this contract be terminated?
                        7. **Risk Assessment**: 
                            - 🔴 High Risk clauses
                            - 🟡 Medium Risk clauses  
                            - 🟢 Low Risk clauses
                        
                        Be concise and structured in your response."""
                
                    summary_chunks = []
                    for chunk in st.session_state["rag_service"].chain.stream(
                            {"input": summary_prompt},
                            st.session_state["session_config"] 
                        ): summary_chunks.append(chunk)

                    st.session_state["contract_summary"] = "".join(summary_chunks)
                    st.success(upload_msg)
                else:
                    st.error(upload_msg)

        if st.session_state["contract_summary"]:
            st.divider()
            st.subheader("Contract Summary")
            st.markdown(st.session_state["contract_summary"])
                

 
 
with right_col:
    st.subheader("Ask About this Contract")
    
    if st.session_state["rag_service"] is None:
        st.info("Please upload and analyze a contract first.")
    else:
         # show cchat history
        
        for message in st.session_state["messages"]:
            st.chat_message(message["role"]).write(message["content"])
        #
        prompt = st.chat_input("Ask anything about the contract:")


       
        if prompt:
            
            st.session_state["messages"].append(
                {
                    "role": "user",
                    "content": prompt
                }
            )
            st.chat_message("user").write(prompt)

            ai_res_list = []
            with st.spinner("Aynlyzing ..."):
                res_stream = st.session_state["rag_service"].chain.stream(
                    {"input" : prompt},
                    st.session_state["session_config"] 
                )

                def capture(generator, cache_list):
                    for chunk in generator:
                        cache_list.append(chunk)
                        yield chunk

            st.chat_message("assistant").write(
                capture(res_stream,ai_res_list)
            )

            st.session_state["messages"].append(
                {
                    "role":"assistant",
                    "content":"".join(ai_res_list)
                }
            )











