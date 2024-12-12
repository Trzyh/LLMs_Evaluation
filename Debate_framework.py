'''
Function: Debate
Author: Yiheng Zhao
'''


import json
import random
from openai import OpenAI
import os

openai = OpenAI(
    api_key="xxx",
    base_url="xxx",
)

def read_jsonl(path: str):
    with open(path) as fh:
        return [json.loads(line) for line in fh.readlines() if line]

def generate_completion(question, model):
    completion = openai.chat.completions.create(
        model=model,
        messages=question
    )

    return completion

def construct_assistant_message(completion):
    content = completion.choices[0].message.content
    return {"role": "assistant", "content": content}

def construct_agent1_round2_message(response_from_agent1, response_from_agent2, merged_last_elements, question):

    given_passage = "This is the passage you were given before:{}".format(merged_last_elements)

    given_question = "This is the question you were given before:{}".format(question)
    prefix_agent1 = "You are Agent1. This is the solution to the question you were given before from yourself: "
    prefix_agent1 = prefix_agent1 + "```{}```".format(response_from_agent1["content"])

    prefix_agent2 = "This is the solution to the question you were given before from Agent2: "
    prefix_agent2 = prefix_agent2 + "``{}```".format(response_from_agent2["content"]) + "Agent2 is another agent."


    prefix_string = given_passage + given_question + prefix_agent1 + prefix_agent2 + """\n\n Using these solutions as additional information, can you answer the question you were given before as accurately as possible based on the passage you were given before again? Your answer must be A) or B) or C). Explain your answer, putting the answer in the form () at the end of your response."""

    return {"role": "user", "content": prefix_string}

def construct_agent2_round2_message(response_from_agent1, response_from_agent2, merged_last_elements, question):

    given_passage = "This is the passage you were given before:{}".format(merged_last_elements)
    given_question = "This is the question you were given before:{}".format(question)

    prefix_agent2 = "You are Agent2."+" This is the solution to the question you were given before from yourself:  "
    prefix_agent2 = prefix_agent2 + "``{}```".format(response_from_agent2["content"])

    prefix_agent1 = "This is the solution to the question you were given before from Agent1: "
    prefix_agent1 = prefix_agent1 + "```{}```".format(response_from_agent1["content"]) + "Agent1 is another agent."

    prefix_string = given_passage + given_question + prefix_agent2 + prefix_agent1 + """\n\n Using these solutions as additional information, can you answer the question you were given before as accurately as possible based on the passage you were given before again? Your answer must be A) or B) or C). Explain your answer, putting the answer in the form () at the end of your response."""

    return {"role": "user", "content": prefix_string}

def construct_agent1_round3_message(response_from_agent1_round2, response_from_agent2_round2, merged_last_elements, question, changed_question):

    given_passage = "This is the passage you were given before:{}".format(merged_last_elements)
    given_question = "This is the question you were given before:{}".format(question)

    prefix_agent1_round2 = "You are Agent1. This is the latest solution to the question you were given before from yourself: "
    prefix_agent1_round2 = prefix_agent1_round2 + "```{}```".format(response_from_agent1_round2["content"][:-1])

    prefix_agent2_round2 = "This is the latest solution to the question you were given before from Agent2: "
    prefix_agent2_round2 = prefix_agent2_round2 + "```{}```".format(response_from_agent2_round2["content"][:-1]) + "Agent2 is another agent."

    prefix_string = given_passage + given_question + prefix_agent1_round2 + prefix_agent2_round2 + """\n\n Using these solutions as additional information, can you answer the following question as possible based on the passage you were given before again? {} Your answer must be A) or B) or C). Explain your answer, putting the answer in the form () at the end of your response.""".format(changed_question)

    return {"role": "user", "content": prefix_string}

def construct_agent2_round3_message(response_from_agent1_round2, response_from_agent2_round2, merged_last_elements, question, changed_question):

    given_passage = "This is the passage you were given before:{}".format(merged_last_elements)
    given_question = "This is the question you were given before:{}".format(question)

    prefix_agent1_round2 = "This is the latest solution to the question you were given before from Agent1: "
    prefix_agent1_round2 = prefix_agent1_round2 + "```{}```".format(response_from_agent1_round2["content"][:-1]) + "Agent1 is another agent."

    prefix_agent2_round2 = "You are Agent2. This is the latest solution to the question you were given before from yourself:"
    prefix_agent2_round2 = prefix_agent2_round2 + "```{}```".format(response_from_agent2_round2["content"][:-1])

    prefix_string = given_passage + given_question + prefix_agent2_round2 + prefix_agent1_round2+  """\n\n Using these solutions as additional information, can you answer the following question as possible based on the passage you were given before again? {} Your answer must be A) or B) or C). Explain your answer, putting the answer in the form () at the end of your response.""".format(changed_question)

    return {"role": "user", "content": prefix_string}

dn_tt_ep = read_jsonl(r"xxx")


agents = 2
rounds = 3
random.seed(0)
for data in dn_tt_ep[20:21]:

    document_name = data['Document_name']
    directory_path = r'xxx'
    file_path = os.path.join(directory_path, f"{document_name}.json")

    all_information_list = []
    z = 0
    for ep in data['event_pairs']:

        event1 = ' '.join(data['text'][int(i) - 1][-1] for i in ep[0][1])
        event2 = ' '.join(data['text'][int(i) - 1][-1] for i in ep[1][1])

        token_id_event1_firstword = ep[0][1][0]
        token_id_event1_lastword = ep[0][1][-1]
        token_id_event2_firstword = ep[1][1][0]
        token_id_event2_lastword = ep[1][1][-1]

        merged_last_elements = ""
        for i in range(len(data["text"])):
            first_element = data["text"][i][0]
            current_element = data["text"][i][-1]


            if i < len(data["text"]) - 1:
                if (token_id_event1_firstword != token_id_event1_lastword) and (token_id_event2_firstword != token_id_event2_lastword):
                    if (first_element == token_id_event1_firstword) or (first_element == token_id_event2_firstword):
                        merged_last_elements += '<' + current_element
                    elif (first_element == token_id_event1_lastword) or (first_element == token_id_event2_lastword):
                        merged_last_elements += current_element + '>'
                    else:
                        merged_last_elements += current_element
                elif (token_id_event1_firstword == token_id_event1_lastword) and (token_id_event2_firstword == token_id_event2_lastword):
                    if (first_element == token_id_event1_firstword) or (first_element == token_id_event2_firstword):
                        merged_last_elements += '<' + current_element + '>'
                    else:
                        merged_last_elements += current_element
                elif (token_id_event1_firstword != token_id_event1_lastword) and (token_id_event2_firstword == token_id_event2_lastword):
                    if first_element == token_id_event1_firstword:
                        merged_last_elements += '<' + current_element
                    elif first_element == token_id_event1_lastword:
                        merged_last_elements += current_element + '>'
                    elif first_element == token_id_event2_firstword:
                        merged_last_elements += '<' + current_element + '>'
                    else:
                        merged_last_elements += current_element
                elif (token_id_event1_firstword == token_id_event1_lastword) and (token_id_event2_firstword != token_id_event2_lastword):
                    if first_element == token_id_event2_firstword:
                        merged_last_elements += '<' + current_element
                    elif first_element == token_id_event2_lastword:
                        merged_last_elements += current_element + '>'
                    elif first_element == token_id_event1_firstword:
                        merged_last_elements += '<' + current_element + '>'
                    else:
                        merged_last_elements += current_element

                next_element = data["text"][i + 1][-1]
                if next_element.isalnum():
                    merged_last_elements += " "
            if i == len(data["text"]) - 1:
                merged_last_elements += current_element

        original_question = "Is <{}> the cause or the effect of <{}>? : A) <{}> is neither the cause nor the effect of <{}>, B) <{}> is the cause of <{}>, C) <{}> is the effect of <{}>".format(event1,event2,event1,event2,event1,event2,event1,event2)
        changed_question = "Is <{}> the cause or the effect of <{}>? : A) <{}> is neither the cause nor the effect of <{}>, B) <{}> is the cause of <{}>, C) <{}> is the effect of <{}>".format(
            event2, event1, event2, event1, event2, event1, event2, event1)
        agent_contexts = []
        for agent in range(0, agents):
            if agent == 0:
                agent_context = [{"role": "user",
                                  "content": """Passage:{} You are Agent1. Can you answer the following question as accurately as possible based on the given passage? {} Your answer must be A) or B) or C). Explain your answer, putting the answer in the form () at the end of your response.""".format(
                                      merged_last_elements,original_question)}]
                agent_contexts.append(agent_context)
            if agent == 1:
                agent_context = [{"role": "user",
                                  "content": """Passage:{} You are Agent2. Can you answer the following question as accurately as possible based on the given passage? {} Your answer must be A) or B) or C). Explain your answer, putting the answer in the form () at the end of your response.""".format(
                                      merged_last_elements, original_question)}]
                agent_contexts.append(agent_context)


        for round in range(0, rounds):
            if round == 0:
                agent1_completion_round1 = generate_completion(question=agent_contexts[0], model="meta-llama/Meta-Llama-3-8B-Instruct")
                agent1_message = construct_assistant_message(agent1_completion_round1)

                agent_contexts[0].append(agent1_message)

                agent2_completion_round1 = generate_completion(question=agent_contexts[1], model="mistralai/Mistral-7B-Instruct-v0.3")
                agent2_message = construct_assistant_message(agent2_completion_round1)
                agent_contexts[1].append(agent2_message)

            if round == 1:
                prompt_agent1_round2 = construct_agent1_round2_message(agent_contexts[0][-1], agent_contexts[1][-1],
                                                                       merged_last_elements, original_question)
                agent_contexts[0].append(prompt_agent1_round2)
                agent1_completion_round2 = generate_completion(question=agent_contexts[0], model="meta-llama/Meta-Llama-3-8B-Instruct")
                agent1_message = construct_assistant_message(agent1_completion_round2)
                agent_contexts[0].append(agent1_message)


                prompt_agent2_round2 = construct_agent2_round2_message(agent_contexts[0][-3], agent_contexts[1][-1],
                                                                       merged_last_elements, original_question)
                agent_contexts[1].append(prompt_agent2_round2)
                agent2_completion_round2 = generate_completion(question=agent_contexts[1], model="mistralai/Mistral-7B-Instruct-v0.3")
                agent2_message = construct_assistant_message(agent2_completion_round2)
                agent_contexts[1].append(agent2_message)


            if round == 2:
                prompt_agent1_round3 = construct_agent1_round3_message(agent_contexts[0][1], agent_contexts[0][-1],
                                                                       agent_contexts[1][1], agent_contexts[1][-1],
                                                                       merged_last_elements, original_question, changed_question)
                agent_contexts[0].append(prompt_agent1_round3)
                agent1_completion_round3 = generate_completion(question=agent_contexts[0], model="meta-llama/Meta-Llama-3-8B-Instruct")
                agent1_message = construct_assistant_message(agent1_completion_round3)
                agent_contexts[0].append(agent1_message)

                prompt_agent2_round3 = construct_agent2_round3_message(agent_contexts[0][1], agent_contexts[0][-3],
                                                                       agent_contexts[1][1], agent_contexts[1][-1],
                                                                       merged_last_elements, original_question, changed_question)
                agent_contexts[1].append(prompt_agent2_round3)
                agent2_completion_round3 = generate_completion(question=agent_contexts[1], model="mistralai/Mistral-7B-Instruct-v0.3")
                agent2_message = construct_assistant_message(agent2_completion_round3)
                agent_contexts[1].append(agent2_message)



        event1_token = [i for i in ep[0][1]]
        event2_token = [i for i in ep[1][1]]

        event1_sentence_number = ' '.join(data['text'][int(i) - 1][1] for i in ep[0][1])
        event2_sentence_number = ' '.join(data['text'][int(i) - 1][1] for i in ep[1][1])

        Agent1_round1 = agent_contexts[0][1]
        Agent1_round2 = agent_contexts[0][3]
        Agent1_round3 = agent_contexts[0][5]


        Agent2_round1 = agent_contexts[1][1]
        Agent2_round2 = agent_contexts[1][3]
        Agent2_round3 = agent_contexts[1][5]

        all_information = {
            'event1_information': [event1, event1_token, event1_sentence_number],
            'event2_information': [event2, event2_token, event2_sentence_number],
            'response': [Agent1_round1, Agent1_round2, Agent1_round3, Agent2_round1, Agent2_round2, Agent2_round3]
        }

        all_information_list.append(all_information)

        z+=1

    with open(file_path, 'w') as json_file:
        for all_information in all_information_list:
            json_string = json.dumps(all_information)
            json_file.write(json_string + "\n")

    print(f"Data has been written to {file_path}")














