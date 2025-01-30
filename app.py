import json
import streamlit as st
from openai import OpenAI
from prompts import SYNTHETIC_DATA_PROMPT
import pandas as pd


DATA_TYPES = [
    "General Query",
    "Prompt Injection",
    "Offensive Language",
    "Off-Topic Query",
    "Toxic Content in Query",
    "Multiple Questions in Query",
    "Non-Standard Characters",
    "Sexist Conten in Query",
]

N_ROWS_PER_TYPE = 5

st.title("Synthetic Datasets")
st.text("Demo of the Galileo synthetic data generation feature.")

api_key = st.text_input("This demo makes calls to OpenAI. Enter the API key below (search for \"OpenAI API Key\" in 1Pass):", type="password")
# client = OpenAI(api_key=st.secrets["OpenAI_key"])
client = OpenAI(api_key=api_key)

form = st.form('configs')

def generate_data(model, description, examples, edge_cases):
    
    prompt_filled = SYNTHETIC_DATA_PROMPT.format(
        app_details=description,
        examples=" - " + "\n - ".join(examples),
        edge_cases=",".join(edge_cases),
        n=N_ROWS_PER_TYPE
    )

    completion = client.chat.completions.create(
        model=model,
        temperature=1,
        # model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt_filled,
            }
        ]
    )

    return completion

def process_openai_response(completion):
    content = completion.choices[0].message.content
    content = content.replace("```", "").replace("json", "").strip("\n")
    parsed_output = json.loads(content)
    
    dataframe = []

    for query_type in parsed_output['queries']:
        name = query_type['edge_case']
        queries = query_type['queries']

        for q in queries:
            dataframe.append([q, name])
    
    return pd.DataFrame(dataframe, columns=['query', 'type'])



with form:
    
    description = st.text_area('What does your app do?', placeholder="E.g., Customer support chatbot for a mobile carrier service")

    examples = st.text_area(
        'Provide 3-5 sample user queries that you expect users to ask in your app',
        placeholder="Enter one query per line"
    )

    selected_test_cases = st.multiselect(
        label="Data Types: select what kind of data to generate",
        options=DATA_TYPES,
        default=["General Query", "Prompt Injection", "Offensive Language"],
        placeholder="Specify what data to generate",
    )
    
    additional_test_cases = st.text_area(
        'To test additional edge cases, specify custom data types below:',
        placeholder="Enter one data type per line. e.g.:\nMalformed Date Request\nForeign Language",
    )


    model = st.selectbox("Model to generate data with", options=['gpt-4o-mini', 'gpt-4o'])

    submit = st.form_submit_button('Generate Data')
    


if submit:
    if not examples:
        st.error("You must enter at least one example query above!")
    else:
        if additional_test_cases:
            cases = additional_test_cases.split("\n")
            selected_test_cases +=  cases
        
        with st.spinner('Generating data. This will take a minute'):
            generation = generate_data(model, description, examples.split("\n"), selected_test_cases)

        result_df = process_openai_response(generation)
        st.dataframe(result_df)

        st.download_button(
            "Download CSV",
            result_df.to_csv(index=False).encode('utf-8'),
            "file.csv",
            "text/csv",
            key='download-csv'
        )