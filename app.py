import os
import streamlit as st
import pandas as pd

from openai import OpenAI

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
MODEL = "meta-llama/llama-3-8b-instruct"

# Set up OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


st.title("📊 GenAI Data Analyst")
st.write("Upload your CSV and ask questions about it using GenAI!")


uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])
df = None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        if st.checkbox("Show Uploaded Dataset"):
            st.dataframe(df)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

user_input = st.text_input("❓ Ask a question about your uploaded dataset:")


if user_input and df is not None and OPENROUTER_API_KEY:
   
    prompt = f"""
You are a helpful data analyst. Use the following sample of uploaded CSV data to answer the user's question.

Here is the sample data:
{df.head(10).to_string(index=False)}

Question: {user_input}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": "https://your-app-name.streamlit.app",  # Optional
                "X-Title": "GenAI Data Analyst"
            }
        )
        answer = response.choices[0].message.content
        st.success("✅ Answer:")
        st.write(answer)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

elif user_input and df is None:
    st.warning("⚠️ Please upload a CSV file before asking questions.")

elif not OPENROUTER_API_KEY:
    st.warning("⚠️ OpenRouter API Key not found. Please check your `.env` or Streamlit secrets.")

