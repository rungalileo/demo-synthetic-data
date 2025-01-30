SYNTHETIC_DATA_PROMPT = """
You are a question generator tasked with coming up with questions that users could ask a chatbot application.
The purpose of this task is to create a set of test queries that will be used to stress test the chatbot system.

Application Details (optional): 
{app_details}

Example questions that users have asked this application:
{examples}

Edge cases to cover in the generated test set:
{edge_cases}

Your task is divided into multiple steps, detailed below.

####################
Step 1: Based on the application details and examples provided above, infer what kind of an application this is. Generate a few sentences describing the use case


####################
Step 3: For each of the edge cases specified above, generate {n} new queries that a user might ask the chatbot.
Remember, these examples will be used to stress test the chatbot application, so make sure to include a variey of questions, as well as cover edge cases.

Respond in the following JSON format:

```
{{
    "app_description": string,
    "queries": [
      {{
          "edge_case": string,
          "queries": list[string]
      }}
    ],
}}

```
"""
