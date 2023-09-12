import os
import streamlit as st
from streamlit_chat import message
# enter gpt-4 key here guys
os.environ['OPENAI_API_KEY']=openaikey

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

def get_ai_response(human_input):
    template = """act as a code generator that generates html and css codes for the given prompts based on the user inpput.display only html and css as output.
    {history}
    User: {human_input}
    bot:
    """
    prompt = PromptTemplate(
        input_variables=["history","human_input"],
        template=template,
    )

    chain = LLMChain(llm=OpenAI(temperature=1), prompt=prompt, verbose=False,memory=ConversationBufferWindowMemory(k=2))

    ai_reply = chain.predict(human_input=human_input)
    # print(story)
    return ai_reply



def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)

    # Generate AI response using user input (replace this with your AI model)
    ai_response = get_ai_response(user_input)
    st.session_state.generated.append(ai_response)

    # Display the AI response
    message(user_input, is_user=True, key=f"{len(st.session_state.past)-1}_user")
    message(ai_response, key=f"{len(st.session_state.generated)-1}_{ai_response}")


def on_btn_click():
    st.session_state.past.clear()
    st.session_state.generated.clear()


st.session_state.setdefault('past', [])
st.session_state.setdefault('generated', [])

st.title("Chatbot")

chat_placeholder = st.empty()

with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):                
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user_{st.session_state['past'][i]}")
        message(st.session_state['generated'][i], key=f"{i}")
    
    st.button("Clear messages", on_click=on_btn_click)


with st.container():
    st.text_input("", on_change=on_input_change, key="user_input")

