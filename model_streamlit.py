import streamlit as st
import ollama
from typing import Dict, Generator
from utils import URLget_contacts,URLdata_get1

available_functions = {
  'URLget_contacts': URLget_contacts,
#   'URLdata_get1': URLdata_get1
}


def ollama_generator(model_name: str, messages: Dict) -> Generator:
    response = ollama.chat(
        model=model_name,  tools=[URLget_contacts],messages=messages)
    if response.message.tool_calls:
  # There may be multiple tool calls in the response
      for tool in response.message.tool_calls:
        # Ensure the function is available, and then call it
        if function_to_call := available_functions.get(tool.function.name):
          print('Calling function:', tool.function.name)
          print('Arguments:', tool.function.arguments)
          output = function_to_call(**tool.function.arguments)
          print('Function output:', output)
          messages.append(response.message)
          # print("messages append",messages)
          messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})
          # print("messages append1111111",messages)

          # Get final response from model with function outputs
          final_response = ollama.chat(model_name, messages=messages)
          # print('Final response:', final_response.message.content)
          return final_response['message']['content']
        else:
          print('Function', tool.function.name, 'not found')
    return response['message']['content']












st.title("Ollama with Streamlit demo")
if "selected_model" not in st.session_state:
    st.session_state.selected_model = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
st.session_state.selected_model = st.selectbox(
    "Please select the model:", [model["model"] for model in ollama.list()["models"]])
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("How could I help you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write(ollama_generator(
            st.session_state.selected_model, st.session_state.messages))
    st.session_state.messages.append(
        {"role": "assistant", "content": response})