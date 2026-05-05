import streamlit as st
import openai
from anthropic import Anthropic

# PAGE CONFIG
st.set_page_config(page_title="Pixii AEO Diagnostic", page_icon="🔍", layout="wide")

st.title("🚀 Pixii.ai: AEO Diagnostic Tool")
st.markdown("### *Is your brand invisible to AI shoppers?*")

# SIDEBAR - For API Keys
with st.sidebar:
    st.header("🔑 API Configuration")
    openai_key = st.text_input("OpenAI API Key", type="password")
    anthropic_key = st.text_input("Anthropic API Key", type="password")
    st.info("We check GPT-4o and Claude 3.5 to see if they recommend your brand.")

# INPUTS
col1, col2 = st.columns(2)
with col1:
    brand = st.text_input("Your Brand Name", placeholder="e.g., Apple")
with col2:
    query = st.text_input("Customer Search Query", placeholder="e.g., best laptop for creators")

if st.button("Run Diagnostic Scan"):
    if not openai_key or not anthropic_key or not brand or not query:
        st.error("Please fill in all fields and API keys!")
    else:
        with st.spinner("Scanning AI Answer Engines..."):
            prompt = f"Act as a shopping expert. A customer is asking: '{query}'. Provide a list of the top 3 recommended brands and a brief reason why for each."
            
            # OpenAI Call
            client_oa = openai.OpenAI(api_key=openai_key)
            res_oa = client_oa.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}]).choices[0].message.content

            # Anthropic Call
            client_ant = Anthropic(api_key=anthropic_key)
            res_ant = client_ant.messages.create(model="claude-3-5-sonnet-20240620", max_tokens=1000, messages=[{"role": "user", "content": prompt}]).content[0].text

            # Logic
            oa_found = brand.lower() in res_oa.lower()
            ant_found = brand.lower() in res_ant.lower()

            # UI Display
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("GPT-4o Results")
                st.metric("Visibility", "Found" if oa_found else "Missing", delta="100%" if oa_found else "-100%")
                st.write(res_oa)
            with c2:
                st.subheader("Claude 3.5 Results")
                st.metric("Visibility", "Found" if ant_found else "Missing", delta="100%" if ant_found else "-100%")
                st.write(res_ant)
