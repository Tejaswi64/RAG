import streamlit as st
import requests
from datetime import datetime

# Page config
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="centered")

# API Configuration
API_URL = "http://localhost:8000/query"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🤖 RAG Chatbot")
    n_results = st.slider("Number of sources", 1, 5, 3)
    show_sources = st.checkbox("Show sources", value=True)
    
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption(f"💬 {len(st.session_state.messages)} messages")

# Main chat interface
st.title("💬 RAG Chatbot")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        # Show sources for assistant messages
        if message["role"] == "assistant" and show_sources and "sources" in message:
            with st.expander("📄 Sources"):
                for i, source in enumerate(message["sources"], 1):
                    st.caption(f"**Source {i}:**")
                    st.text(source[:200] + "..." if len(source) > 200 else source)
                    st.divider()

# Chat input
if prompt := st.chat_input("Ask a question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": prompt, "n_results": n_results},
                    timeout=3000
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data["sources"]
                    
                    st.write(answer)
                    
                    # Add to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                    
                    # Show sources
                    if show_sources:
                        with st.expander("📄 Sources"):
                            for i, source in enumerate(sources, 1):
                                st.caption(f"**Source {i}:**")
                                st.text(source[:200] + "..." if len(source) > 200 else source)
                                st.divider()
                else:
                    st.error(f"API Error: {response.status_code}")
            
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Cannot connect to API. Is it running on port 8000?")
            except Exception as e:
                st.error(f"Error: {str(e)}")