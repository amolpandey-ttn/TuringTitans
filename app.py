import streamlit as st
from streamlit_chat import message
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

openai_api_key = "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"

st.set_page_config(page_title="Cloud Cost Analyzer", page_icon=":cloud:")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Function to get user input
def get_text():
   input_text = st.text_input("Enter your question...","eg: How much did I spend on AWS last month?")
   return input_text

# Function to generate response to user question
def get_response(query):
   with st.spinner(text="In Progress..."):
       response = agent.run(query)
   return response

# st.header("CloudCost AI Analyzer")
st.title("CloudCost AI Analyzer")
st.markdown("<h3 style='text-align: center;'>Your AI Assistance to Query Cloud Usage  ᵃ⤻ ᶻ</a></h3>", unsafe_allow_html=True)


user_csv = st.sidebar.file_uploader("Upload Your CSV File", type="csv")


if user_csv is not None:
    if 'history' not in st.session_state:
            st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about " + user_csv.name + " 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

    response_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder="Talk to your CSV data here (:", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            llm = OpenAI(openai_api_key=openai_api_key, temperature=0.6,max_tokens = 1000)
            agent = create_csv_agent(llm, user_csv, verbose=True)
            if 'generated' not in st.session_state:
                st.session_state['generated'] = ["Yes, you can!"]
            if 'past' not in st.session_state:
                st.session_state['past'] = ["Can I ask anything about my csv file?"]
            if user_input:
                st.session_state.past.append(user_input)
                # Get the chatbot response
                response = get_response(user_input)
                st.session_state.generated.append(response)
            # st.session_state['past'].append(user_input)
            # st.session_state['generated'].append(output)


    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="bot")

