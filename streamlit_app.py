import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 nobug007 Chatbot")
st.write(
    "안녕하세요? "
    "챗봇 테스트 입니다. "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# OpenAI API Key는 Streamlit Secrets에서 가져옴
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": """
너는 여행 전문 상담 챗봇이다.
사용자의 여행 목적지, 일정, 예산, 동행자, 여행 스타일을 먼저 파악한다.
항공권, 숙소, 교통, 맛집, 관광지, 일정표를 현실적으로 추천한다.
답변은 한국어로 한다.
너무 긴 답변보다는 보기 쉽게 정리해서 답변한다.
사용자가 목적지나 날짜를 말하지 않으면 먼저 필요한 정보를 질문한다.
위험 지역, 비자, 날씨, 현지 교통, 환전, 준비물도 필요하면 함께 안내한다.
"""
        },
        *[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    ],
    stream=True,
)

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
