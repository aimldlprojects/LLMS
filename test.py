import streamlit as st

# Custom CSS to style the sections
st.markdown(
    """
    <style>
    .section1 {
        background-color: #0019c3;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .section2 {
        background-color: #3d95f8;
        padding: 20px;
        border-radius: 10px;
    }
    .title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# First section with Title 1 and background color
st.markdown('<div class="section1">', unsafe_allow_html=True)
st.markdown('<div class="title">Title 1</div>', unsafe_allow_html=True)
st.write("Above Box Text")
st.markdown('</div>', unsafe_allow_html=True)

# Second section with Title 2 and different background color
st.markdown('<div class="section2">', unsafe_allow_html=True)
st.markdown('<div class="title">Title 2</div>', unsafe_allow_html=True)
st.write("Below Box Text")
st.markdown('</div>', unsafe_allow_html=True)
