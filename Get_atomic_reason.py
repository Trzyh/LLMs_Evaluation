'''
Function: Breaking generations into a series of atomic reasoning processes
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
            Prompt = {"role": "user", "content": "Please breakdown the following sentence into reasoning steps:" + response["content"]+"Each reasoning step must consist of premises and a conclusion. The output of reasoning steps is in the following format: {'Reasoning step 1':'premises and conclusion of reasoning step 1', 'Reasoning step 2':'premises and conclusion of reasoning step 2',...}Do not perform any other operations. Only return reasoning steps to me, do not return any other content"}
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








