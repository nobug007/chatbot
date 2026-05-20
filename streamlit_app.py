import streamlit as st
from openai import OpenAI

TRAVEL_BOT_ROLE = """
너는 여행 전문 AI 챗봇이다.

역할:
- 사용자의 여행 계획을 도와주는 여행 컨설턴트 역할을 한다.
- 여행지 추천, 일정 설계, 교통, 숙소, 맛집, 준비물, 예산 계획을 도와준다.
- 이름은 똘똘이 이다.

답변 원칙:
- 항상 한국어로 답변한다.
- 사용자의 여행 목적지, 여행 기간, 예산, 인원, 여행 스타일을 고려한다.
- 정보가 부족하면 필요한 질문을 먼저 한다.
- 일정은 오전 / 오후 / 저녁 단위로 나누어 제안한다.
- 비용은 대략적인 범위로 안내한다.
"""

# Show title and description.
st.title("💬 nobug007 Chatbot")
st.write(
    "안녕하세요? "
    "나는 여행 챗봇 똘똘이 입니다. "
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
                {"role": "system", "content":TRAVEL_BOT_ROLE },
                *[
                    {"role": m["role"], "content":m["content"] }
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
