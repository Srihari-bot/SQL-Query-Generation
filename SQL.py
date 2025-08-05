# import streamlit as st
# import pandas as pd
# import sqlite3
# import requests

# # IBM Watsonx.ai text generation API details
# api_key = "_bsaaf2TIgUm4NEeU4TCAipr_K2Pou6afOC3OsXA4_70"
# url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
# project_id = "fdaabd6a-ff60-40c4-bf37-5549a34deac4"
# model_id = "meta-llama/llama-3-405b-instruct"

# @st.cache_data
# def get_access_token(api_key):
#     auth_url = "https://iam.cloud.ibm.com/identity/token"
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Accept": "application/json"
#     }
#     data = {
#         "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
#         "apikey": api_key
#     }

#     response = requests.post(auth_url, headers=headers, data=data)

#     if response.status_code != 200:
#         st.error(f"Failed to get access token: {response.text}")
#         raise Exception(f"Failed to get access token: {response.text}")

#     token_info = response.json()
#     return token_info['access_token']

# def generate_sql_query_watson(content, access_token):
#     body = {
#         "input": content,
#         "parameters": {
#             "decoding_method": "greedy",
#             "max_new_tokens": 300,
#             "min_new_tokens": 30,
#             "stop_sequences": [";"],
#             "repetition_penalty": 1.05,
#             "temperature": 0.5
#         },
#         "model_id": model_id,
#         "project_id": project_id
#     }




#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {access_token}"
#     }

#     response = requests.post(url, headers=headers, json=body)

#     if response.status_code != 200:
#         st.error(f"Non-200 response: {response.status_code} - {response.text}")
#         raise Exception(f"Non-200 response: {response.status_code} - {response.text}")

#     data = response.json()
#     if 'results' in data and len(data['results']) > 0:
#         return data['results'][0]['generated_text'].strip()
#     else:
#         st.error("No results returned from Watson API.")
#         return None

# # def extract_sql_query(response_text):
# #     sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']
# #     for keyword in sql_keywords:
# #         if keyword in response_text.upper():
# #             start_index = response_text.upper().index(keyword)
# #             sql_query = response_text[start_index:].strip()
# #             # Replace backticks with double quotes for SQLite compatibility
# #             sql_query = sql_query.replace('`', '"')
# #             # Enclose column names with spaces in double quotes
# #             columns = sql_query.split()
# #             columns = [f'"{col}"' if " " in col and not col.startswith('"') else col for col in columns]
# #             sql_query = " ".join(columns)
# #             return sql_query
# #     return None

# # def extract_sql_query(response_text):
# #     sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']
# #     for keyword in sql_keywords:
# #         if keyword in response_text.upper():
# #             start_index = response_text.upper().index(keyword)
# #             sql_query = response_text[start_index:].strip()
# #             # Replace backticks with double quotes for SQLite compatibility
# #             sql_query = sql_query.replace('`', '"')
# #             # Enclose column names with spaces in double quotes
# #             columns = sql_query.split()
# #             columns = [f'"{col}"' if " " in col and not col.startswith('"') else col for col in columns]
# #             sql_query = " ".join(columns)
# #             # Ensure the query ends with a semicolon, as needed
# #             if not sql_query.endswith(';'):
# #                 sql_query += ';'
# #             return sql_query
# #     return None

# def extract_sql_query(response_text):
#     sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']
#     for keyword in sql_keywords:
#         if keyword in response_text.upper():
#             # Find where the SQL query starts
#             start_index = response_text.upper().index(keyword)
#             # Extract the query part from the response
#             sql_query = response_text[start_index:].strip()
            
#             # Replace backticks with double quotes for SQLite compatibility
#             sql_query = sql_query.replace('`', '"')
            
#             # Enclose column names with spaces in double quotes
#             columns = sql_query.split()
#             columns = [f'"{col}"' if " " in col and not col.startswith('"') else col for col in columns]
#             sql_query = " ".join(columns)
            
#             # Clean up and ensure no extra text is included
#             sql_query = sql_query.split(";", 1)[0] + ";"  # Take only the first SQL statement
#             return sql_query
#     return None




# def main():
#     st.set_page_config(page_title="CSV to SQL Query Generator", page_icon="📊", layout="wide")
#     st.title('CSV to SQL Query Generator')

#     uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
#     if uploaded_file is not None:
#         df = pd.read_csv(uploaded_file)
#         st.write(f"Uploaded file has {df.shape[0]} rows and {df.shape[1]} columns.")
        
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.subheader("Data Preview")
#             st.dataframe(df.head())
        
#         with col2:
#             st.subheader("Column Info")
#             for col in df.columns:
#                 st.write(f"- {col}: {df[col].dtype}")

#         table_name = st.text_input("Enter the table name:", "cars_dataset")
#         user_question = st.text_area("Ask a question about the CSV data:")

#         if st.button("Generate and Execute SQL Query"):
#             with st.spinner("Generating and executing query..."):
#                 access_token = get_access_token(api_key)

#                 conn = sqlite3.connect(':memory:')
#                 df.to_sql(table_name, conn, index=False)

#                 content = f"""
# Based on the following CSV data structure and the user's question, generate a SQL SELECT query to retrieve relevant information.

# Table name: {table_name}
# Columns: {', '.join(df.columns)}

# Sample data:
# {df.head().to_string()}

# User's question:
# {user_question}

# Please provide only a SQL SELECT query that could answer the user's question based on this data. Do not include any explanation or additional text.
# """

#                 response = generate_sql_query_watson(content, access_token)

#                 if response:
#                     extracted_query = extract_sql_query(response)
#                     if extracted_query:
#                         st.subheader("Generated SQL Query")
#                         st.code(extracted_query, language='sql')

#                         try:
#                             # Remove any trailing semicolon and whitespace
#                             cleaned_query = extracted_query.rstrip(';').strip()
#                             result = pd.read_sql_query(cleaned_query, conn)
#                             st.subheader("Query Result")
#                             st.dataframe(result)
                            
#                             # Add download button for query results
#                             csv = result.to_csv(index=False)
#                             st.download_button(
#                                 label="Download results as CSV",
#                                 data=csv,
#                                 file_name="query_results.csv",
#                                 mime="text/csv",
#                             )
#                         except sqlite3.OperationalError as e:
#                             st.error(f"An error occurred while executing the query: {e}")
#                     else:
#                         st.error("Could not extract a valid SQL query from the response.")
#                 else:
#                     st.error("Failed to generate SQL query using Watson.")

#                 conn.close()

# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import sqlite3
import requests

# IBM Watsonx.ai text generation API details

api_key = "zpseg_CvW4iY1piNQkKhxemS2NoRPTkP2VOAOOXkENns"
url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
project_id = "6de5c4d1-65ac-43c8-8476-ed6082eee2ed"
model_id = "google/flan-ul2"
auth_url = "https://iam.cloud.ibm.com/identity/token"


@st.cache_data
def get_access_token(api_key):
    auth_url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code != 200:
        st.error(f"Failed to get access token: {response.text}")
        raise Exception(f"Failed to get access token: {response.text}")
    token_info = response.json()
    return token_info['access_token']

def generate_sql_query_watson(content, access_token):
    body = {
        "input": content,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 300,
            "min_new_tokens": 30,
            "stop_sequences": [";"],
            "repetition_penalty": 1.05,
            "temperature": 0.5
        },
        "model_id": model_id,
        "project_id": project_id
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        st.error(f"Non-200 response: {response.status_code} - {response.text}")
        raise Exception(f"Non-200 response: {response.status_code} - {response.text}")
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]['generated_text'].strip()
    else:
        st.error("No results returned from Watson API.")
        return None

def extract_sql_query(response_text):
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']
    for keyword in sql_keywords:
        if keyword in response_text.upper():
            start_index = response_text.upper().index(keyword)
            sql_query = response_text[start_index:].strip()
            
            # Replace backticks with double quotes for SQLite compatibility
            sql_query = sql_query.replace('`', '"')
            
            # Enclose column names with spaces in double quotes
            columns = sql_query.split()
            columns = [f'"{col}"' if " " in col and not col.startswith('"') else col for col in columns]
            sql_query = " ".join(columns)
            
            # Clean up and ensure no extra text is included
            sql_query = sql_query.split(";", 1)[0] + ";"  # Take only the first SQL statement
            
            # Replace "text" with "text_" to avoid syntax errors
            sql_query = sql_query.replace(" text ", " text_ ")
            
            return sql_query
    return None

def main():
    st.set_page_config(page_title="CSV to SQL Query Generator", page_icon="📊", layout="wide")
    st.title('CSV to SQL Query Generator')
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(f"Uploaded file has {df.shape[0]} rows and {df.shape[1]} columns.")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Data Preview")
            st.dataframe(df.head())
        with col2:
            st.subheader("Column Info")
            for col in df.columns:
                st.write(f"- {col}: {df[col].dtype}")

        table_name = st.text_input("Enter the table name:", "my_table")
        user_question = st.text_area("Ask a question about the CSV data:")
        
        if st.button("Generate and Execute SQL Query"):
            with st.spinner("Generating and executing query..."):
                access_token = get_access_token(api_key)
                
                # Create in-memory SQLite database and table
                conn = sqlite3.connect(':memory:')
                df.to_sql(table_name, conn, index=False)
                
                content = f"""
                Based on the following CSV data structure and the user's question, generate a SQL SELECT query to retrieve relevant information.
                Table name: {table_name}
                Columns: {', '.join(df.columns)}
                Sample data:
                {df.head().to_string()}
                User's question: {user_question}
                Please provide only a SQL SELECT query that could answer the user's question based on this data. Do not include any explanation or additional text.
                """
                
                response = generate_sql_query_watson(content, access_token)
                if response:
                    extracted_query = extract_sql_query(response)
                    if extracted_query:
                        st.subheader("Generated SQL Query")
                        st.code(extracted_query, language='sql')
                        try:
                            # Remove any trailing semicolon and whitespace
                            cleaned_query = extracted_query.rstrip(';').strip()
                            result = pd.read_sql_query(cleaned_query, conn)
                            st.subheader("Query Result")
                            st.dataframe(result)
                            
                            # Add download button for query results
                            csv = result.to_csv(index=False)
                            st.download_button(
                                label="Download results as CSV",
                                data=csv,
                                file_name="query_results.csv",
                                mime="text/csv"
                            )
                        except sqlite3.OperationalError as e:
                            st.error(f"An error occurred while executing the query: {e}")
                    else:
                        st.error("Could not extract a valid SQL query from the response.")
                else:
                    st.error("Failed to generate SQL query using Watson.")
                conn.close()

if __name__ == "__main__":
    main()

