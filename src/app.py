import streamlit as st
from threading import Thread
from transformers import TextIteratorStreamer
from database import repository
from rag import context_builder, llm_engine

st.set_page_config(page_title="Konoha Archive", page_icon="🍥", layout="centered")

st.title("🍥 NarutoGPT (RAG)")
st.caption("Tanyakan apa saja tentang dunia Naruto berdasarkan Knowledge Graph.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("Mencari di gulungan rahasia...", expanded=False) as status:
            st.write("Menghubungkan ke Neo4j...")
            repository.test_connection()
            
            st.write("Mencari fakta relevan...")
            context = context_builder.build_context(prompt)
            
            st.write("Menyusun jawaban...")
            status.update(label="Data ditemukan!", state="complete", expanded=False)
            
            with st.expander("Lihat Konteks Database"):
                st.code(context)

        response_placeholder = st.empty()
        full_response = ""

        tokenizer = llm_engine.get_tokenizer()
        streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
        thread = Thread(target=llm_engine.generate_answer, args=(context, prompt, streamer))
        thread.start()

        streamer_iterator = iter(streamer)

        try:
            with st.spinner("Merapal jawaban..."):
                first_token = next(streamer_iterator)
                full_response += first_token
                response_placeholder.markdown(full_response + "▌")
        except StopIteration:
            pass

        for new_text in streamer_iterator:
            full_response += new_text
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})