import streamlit as st

from chat import ChatBot
from memory import extract_memory
from vector_store import build_index


st.set_page_config(
    page_title="LLM Memory-RAG",
    page_icon="🧠",
    layout="centered"
)


st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #888;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .metric-title {
        font-size: 13px;
        color: #888;
        margin-bottom: 2px;
    }

    .metric-value {
        font-size: 22px;
        font-weight: 600;
    }

    .performance-box {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-top: 15px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="main-title">🧠 LLM Memory-RAG</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Persistent Memory System for Conversational AI'
    '</div>',
    unsafe_allow_html=True
)


if "bot" not in st.session_state:
    st.session_state.bot = ChatBot()

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and "metrics" in message:

            metrics = message["metrics"]

            with st.expander("📊 RAG Performance"):

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Memory Used",
                        "YES"
                        if metrics["memory_used"]
                        else "NO"
                    )

                    st.metric(
                        "Token Reduction",
                        f"{metrics['token_reduction']:.2f}%"
                    )

                    st.metric(
                        "Retrieval Latency",
                        f"{metrics['retrieval_time']:.2f} ms"
                    )

                with col2:

                    st.metric(
                        "Generation Latency",
                        f"{metrics['generation_time']:.2f} ms"
                    )

                    st.metric(
                        "Total Latency",
                        f"{metrics['total_time']:.2f} ms"
                    )


user = st.chat_input(
    "Ask something about your memories..."
)


if user:

    st.session_state.messages.append({
        "role": "user",
        "content": user
    })

    with st.chat_message("user"):

        st.markdown(user)

    with st.chat_message("assistant"):

        with st.spinner("Searching memory..."):

            try:

                reply, metrics = st.session_state.bot.ask(user)

                st.markdown(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                    "metrics": metrics
                })

                with st.expander("📊 RAG Performance"):

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Memory Used",
                            "YES"
                            if metrics["memory_used"]
                            else "NO"
                        )

                        st.metric(
                            "Token Reduction",
                            f"{metrics['token_reduction']:.2f}%"
                        )

                        st.metric(
                            "Retrieval Latency",
                            f"{metrics['retrieval_time']:.2f} ms"
                        )

                    with col2:

                        st.metric(
                            "Generation Latency",
                            f"{metrics['generation_time']:.2f} ms"
                        )

                        st.metric(
                            "Total Latency",
                            f"{metrics['total_time']:.2f} ms"
                        )

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )


st.divider()


col1, col2 = st.columns(2)


with col1:

    if st.button(
        "💾 Save Memory",
        use_container_width=True
    ):

        if not st.session_state.messages:

            st.warning(
                "There is no conversation to save."
            )

        else:

            conversation_text = "\n\n".join(
                f"{message['role'].capitalize()}: "
                f"{message['content']}"
                for message in st.session_state.messages
            )

            try:

                with st.spinner(
                    "Extracting memory..."
                ):

                    memory = extract_memory(
                        conversation_text
                    )

                if memory:

                    with st.spinner(
                        "Updating FAISS index..."
                    ):

                        build_index()

                    st.success(
                        "Memory saved successfully."
                    )

                else:

                    st.info(
                        "No new memory was identified."
                    )

            except Exception as e:

                st.error(
                    f"Could not save memory: {str(e)}"
                )


with col2:

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.bot = ChatBot()

        st.rerun()


st.caption(
    "Powered by Gemini • Sentence Transformers • FAISS"
)