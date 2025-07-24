import streamlit as st
from few_shots import FewShots
from generate_post import *
def main():
    st.title("Personal Linkedin Post Generator")
    st.subheader("\"Analyze Your Voice. Automate Your Impact\". \nCreate personalized LinkedIn posts that match your unique writing style—instantly")
    col1,col2,col3=st.columns(3)
    fs=FewShots()
    with col1:
        selected_tag=st.selectbox("Topic", options=fs.get_tags())
    with col2:
        selected_length=st.selectbox("Length", options=['Short', 'Medium', 'Long'])
    with col3:
        selected_lang=st.selectbox("Language", options=['English', 'Hinglish'])
    if st.button("Generate"):
        st.subheader("Generating Posts")
        post = post_generate(selected_length, selected_lang, selected_tag)
        st.write(post)

if __name__=="__main__":
    main()