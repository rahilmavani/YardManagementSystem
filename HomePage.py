import streamlit as st

st.set_page_config(
    page_title="Container Managemet System"

)


st.markdown("""
<style>
   .css-h5rgaw.ea3mdgi1 {
        visibility: hidden;
   }        
    
           
</style>






""", unsafe_allow_html=True)


st.image("BitShift.png", width = 300)
st.title("Container Management System")

st.sidebar.success("Navigate Pages from Above")
st.markdown("""---""")

st.subheader("Problem Statement:")

st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font"> The goal of this project is to develop an AI-powered system which will guide and place the incoming containers in an optimised way such that there will be less shuffling and the best way to place containers. Container placement must be done within a short time span. The system should be able to provide relevant and accurate location with containers.</p>', unsafe_allow_html=True)

st.markdown("""---""")
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

st.subheader("Features")
st.markdown("- <p class='big-font'>Predict the timing of the individual containers</p>", unsafe_allow_html=True)
st.markdown("- <p class='big-font'>Generate the optimised location of an individual container</p>", unsafe_allow_html=True)
st.markdown("- <p class='big-font'>Scale to handle large volumes of containers</p>", unsafe_allow_html=True)
st.markdown("- <p class='big-font'>Data privacy and security</p>", unsafe_allow_html=True)
st.markdown("- <p class='big-font'>Ethical use of AI</p>", unsafe_allow_html=True)
st.markdown("""---""")

st.subheader("About Us")
st.markdown('<p class="big-font"> We are sophomore students of Pandit Deendayal Energy University. We are dedicated to create robust technologies, we are excited to be part of this hackathon, ready to showcase our innovative spirit and problem-solving skills. With a passion for technology and sustainability, we aim to make a meaningful impact in this sector.</p>', unsafe_allow_html=True)
st.subheader("Our Team: ")
st.markdown("- <p class='big-font'>Rahil Mavani</p>", unsafe_allow_html=True)
st.markdown("- <p class='big-font'>Meet Dholakia</p>", unsafe_allow_html=True)
st.markdown("- <p class='big-font'>Pal Zadafiya</p>", unsafe_allow_html=True)
st.markdown("- <p class='big-font'>Aryan Kadivar</p>", unsafe_allow_html=True)


