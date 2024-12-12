'''
Function: Breaking generations into a series of atomic propositions
Author: Yiheng Zhao
'''

import json
from openai import OpenAI

openai = OpenAI(
    api_key="xxx",
    base_url="xxx",
)

def generate_completion(question, model):
    completion = openai.chat.completions.create(
        messages=[question],
        model=model,
    )

    return completion

def construct_assistant_message(completion):
    content = completion.choices[0].message.content
    return {"role": "assistant", "content": content}

file_name = r'xxx'

All_information_list = []
with open(file_name, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    z=0
    for line in lines:
        line = json.loads(line.strip())
        event1_information = line.get("event1_information")
        event2_information = line.get("event2_information")
        responses = line.get("response")
        all_information = {}
        Atomic_facts = []
        for response in responses:
            Prompt = {"role": "user", "content": "Please breakdown the following sentence into atomic facts:" + response["content"]+"The output of atomic facts is in the following format: {'Atomic fact 1':'Content of Atomic fact1', 'Atomic fact 2':'Content of Atomic fact2',...} Do not perform any other operations. Only return atomic facts to me, do not return any other content"}
            atomic_facts = construct_assistant_message(generate_completion(Prompt,model="mistralai/Mixtral-8x22B-Instruct-v0.1"))
            Atomic_facts.append(atomic_facts["content"])
        all_information = {
            'event1_information': event1_information,
            'event2_information': event2_information,
            'response': Atomic_facts
        }
        All_information_list.append(all_information)
        z+=1


with open(r"xxx", 'w') as json_file:
    for all_information in All_information_list:
        json_string = json.dumps(all_information)
        json_file.write(json_string + "\n")








