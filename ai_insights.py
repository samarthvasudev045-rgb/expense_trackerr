import streamlit as st
from groq import Groq

def generate_insights(df):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    prompt = f"""
    Analyze the following expense data:

    {df.to_string()}

    Provide:
    - Spending patterns
    - Cost-cutting suggestions
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
