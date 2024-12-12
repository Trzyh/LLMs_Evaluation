'''
Function: Evaluating the factuality of atomic propositions
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

pla = [
    r'xxx',
    r'xxx',
    r'xxx',
]

labels = []
prompts = []
atomicfacts = []

pla_data = [prompts, labels, atomicfacts]
for i in range(0, len(pla)):
    with open(pla[i], 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line.strip())
            pla_data[i].append(data)

all_atomic_facts = []
i=0
for i in range(0,len(prompts)):
    atomic_facts = []
    for j in range(0,len(prompts[i])):
        if j ==0:
            prompt_content = "This is a passage and a question:" + prompts[i][j] + "The real answer of the question is "+labels[i]["answer"][j]+\
                             ". This is the solution given by Agent 1 based on the question, and I have broken it down into atomic facts:" + \
                             atomicfacts[i]["response"][j] + \
                             "Please use the passage and the question to determine whether each atomic fact is true or false." + \
                             "The output is in the following format: {'Atomic fact 1':'True or False', 'Atomic fact 2':'True or false',...} " + \
                             "Only return factuality of atomic facts to me. Do not return any other content to me."
            Prompt =  Prompt = {"role": "user", "content":prompt_content}
            atomic_facts_fact = construct_assistant_message(generate_completion(Prompt, model="meta-llama/Meta-Llama-3.1-70B-Instruct"))
            atomic_facts.append(atomic_facts_fact)
        if j ==1:
            prompt_content = "This is a prompt previously given to Agent1:" + prompts[i][j] + "The real answer of the question in the prompt is "+labels[i]["answer"][j]+\
                             ". This is the lastest solution given by Agent 1 based on the question, and I have broken it down into atomic facts:" + \
                             atomicfacts[i]["response"][j] + \
                             "Please use these information to determine whether each atomic fact is true or false." + \
                             "The output is in the following format: {'Atomic fact 1':'True or False', 'Atomic fact 2':'True or false',...} " + \
                             "Only return factuality of atomic facts to me. Do not return any other content to me."
            Prompt =  Prompt = {"role": "user", "content":prompt_content}
            atomic_facts_fact = construct_assistant_message(generate_completion(Prompt, model="meta-llama/Meta-Llama-3.1-70B-Instruct"))
            atomic_facts.append(atomic_facts_fact)
        if j == 2:
            prompt_content = ("This is a prompt previously given to Agent1:" + prompts[i][j] + \
                              "The real answer of the first question in the prompt is " + labels[i]["answer"][j-1] + \
                              "The real answer of the second question in the prompt is " + labels[i]["answer"][j]+\
                             ". This is the solution given by Agent 1 based on the second question, and I have broken it down into atomic facts:" + \
                             atomicfacts[i]["response"][j] + \
                             "Please use these information to determine whether each atomic fact is true or false." + \
                             "The output is in the following format: {'Atomic fact 1':'True or False', 'Atomic fact 2':'True or false',...} " + \
                             "Only return factuality of atomic facts to me. Do not return any other content to me.")
            Prompt = Prompt = {"role": "user", "content": prompt_content}
            atomic_facts_fact = construct_assistant_message(generate_completion(Prompt, model="meta-llama/Meta-Llama-3.1-70B-Instruct"))
            atomic_facts.append(atomic_facts_fact)
        if j ==3:
            prompt_content = "This is a passage and a question:" + prompts[i][j] + "The real answer of the question is "+labels[i]["answer"][j]+\
                             ". This is the solution given by Agent 2 based on the question, and I have broken it down into atomic facts:" + \
                             atomicfacts[i]["response"][j] + \
                             "Please use the passage and the question to determine whether each atomic fact is true or false." + \
                             "The output is in the following format: {'Atomic fact 1':'True or False', 'Atomic fact 2':'True or false',...} " + \
                             "Only return factuality of atomic facts to me. Do not return any other content to me."
            Prompt =  Prompt = {"role": "user", "content":prompt_content}
            atomic_facts_fact = construct_assistant_message(generate_completion(Prompt, model="meta-llama/Meta-Llama-3.1-70B-Instruct"))
            atomic_facts.append(atomic_facts_fact)
        if j == 4:
            prompt_content = "This is a prompt previously given to Agent2:" + prompts[i][
                j] + "The real answer of the question in the prompt is " + labels[i]["answer"][j] + \
                             ". This is the lastest solution given by Agent 2 based on the question, and I have broken it down into atomic facts:" + \
                             atomicfacts[i]["response"][j] + \
                             "Please use these information to determine whether each atomic fact is true or false." + \
                             "The output is in the following format: {'Atomic fact 1':'True or False', 'Atomic fact 2':'True or false',...} " + \
                             "Only return factuality of atomic facts to me. Do not return any other content to me."
            Prompt = Prompt = {"role": "user", "content": prompt_content}
            atomic_facts_fact = construct_assistant_message(generate_completion(Prompt, model="meta-llama/Meta-Llama-3.1-70B-Instruct"))
            atomic_facts.append(atomic_facts_fact)
        if j == 5:
            prompt_content = ("This is a prompt previously given to Agent2:" + prompts[i][j] + \
                              "The real answer of the first question in the prompt is " + labels[i]["answer"][j - 1] + \
                              "The real answer of the second question in the prompt is " + labels[i]["answer"][j] + \
                              ". This is the solution given by Agent 2 based on the second question, and I have broken it down into atomic facts:" + \
                              atomicfacts[i]["response"][j] + \
                              "Please use these information to determine whether each atomic fact is true or false." + \
                              "The output is in the following format: {'Atomic fact 1':'True or False', 'Atomic fact 2':'True or false',...} " + \
                              "Only return factuality of atomic facts to me. Do not return any other content to me.")
            Prompt = Prompt = {"role": "user", "content": prompt_content}
            atomic_facts_fact = construct_assistant_message(generate_completion(Prompt, model="meta-llama/Meta-Llama-3.1-70B-Instruct"))
            atomic_facts.append(atomic_facts_fact)
    all_atomic_facts.append(atomic_facts)
    i+=1


with open(r'xxx', 'w') as json_file:
    for all_information in all_atomic_facts:
        json_string = json.dumps(all_information)
        json_file.write(json_string + "\n")










