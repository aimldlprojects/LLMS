
import streamlit as st
import replicate

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

# Replicate credentials
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')
    st.subheader('Models and parameters')

    # Select models
    selected_models = st.sidebar.multiselect('Choose Llama2 models', ['Llama2-7B', 'Cohere'], default=['Llama2-7B'])

    # Parameters for each model
    model_parameters = {}
    for model in selected_models:
        model_parameters[model] = {
            'temperature': st.sidebar.slider(f'{model} temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01),
            'top_p': st.sidebar.slider(f'{model} top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01),
            'max_length': st.sidebar.slider(f'{model} max_length', min_value=32, max_value=128, value=120, step=8),
        }

    # Mode selection: 'instruction' or 'comparison'
    mode = st.sidebar.radio('Select Mode', ['instruction', 'comparison'])

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

def generate_llama2_response(model, prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += f"User: {dict_message['content']}\n\n"
        else:
            string_dialogue += f"Assistant: {dict_message['content']}\n\n"

    try:
        output = replicate.run(
            model,
            input={
                "prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                "temperature": model_parameters[model]['temperature'],
                "top_p": model_parameters[model]['top_p'],
                "max_length": model_parameters[model]['max_length'],
                "repetition_penalty": 1,
            }
        )
        return output
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate responses based on the selected mode
if mode == 'instruction':
    # Instruct one or both models based on the user prompt
    for model in selected_models:
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message(model):
                with st.spinner(f"{model} is thinking..."):
                    response = generate_llama2_response(model, prompt)
                    if response is not None:
                        placeholder = st.empty()
                        full_response = ''
                        for item in response:
                            full_response += item
                            placeholder.markdown(full_response)
                        placeholder.markdown(full_response)
                        message = {"role": model, "content": full_response}
                        st.session_state.messages.append(message)

elif mode == 'comparison':
    # Compare responses from different models
    for model in selected_models:
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message(model):
                with st.spinner(f"{model} is thinking..."):
                    response = generate_llama2_response(model, prompt)
                    if response is not None:
                        placeholder = st.empty()
                        full_response = ''
                        for item in response:
                            full_response += item
                            placeholder.markdown(full_response)
                        placeholder.markdown(full_response)
                        message = {"role": model, "content": full_response}
                        st.session_state.messages.append(message)

# Display system message as a box
with st.container():
    st.text("System Message")
    st.text("This is a system message that can be edited.")
    st.text_area("Edit this message:", height=50)