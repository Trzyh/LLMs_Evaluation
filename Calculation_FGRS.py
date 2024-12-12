'''
Function: Calculating FGRS
Author: Yiheng Zhao
'''


import json
import re

def extract_true_false(input_string):
    matches = re.findall(r'\bFalse\b|\bTrue\b', input_string)
    return matches


file_name = r'xxx'


with open(file_name, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    FGFS_agent1_round1 = []
    FGFS_agent1_round2 = []
    FGFS_agent1_round3 = []
    FGFS_agent2_round1 = []
    FGFS_agent2_round2 = []
    FGFS_agent2_round3 = []
    for line in lines:
        line = json.loads(line.strip())
        # agent1_round1
        results_agent1_round1 = extract_true_false(line[0]['content'])
        true_count = results_agent1_round1.count('True')
        if len(results_agent1_round1) > 0:
            ratio_agent1_round1 = true_count / len(results_agent1_round1)
        else:
            ratio_agent1_round1 = 0
        FGFS_agent1_round1.append(ratio_agent1_round1)
        # agent1_round2
        results_agent1_round2 = extract_true_false(line[1]['content'])
        true_count = results_agent1_round2.count('True')
        if len(results_agent1_round2) > 0:
            ratio_agent1_round2 = true_count / len(results_agent1_round2)
        else:
            ratio_agent1_round2 = 0
        FGFS_agent1_round2.append(ratio_agent1_round2)
        # agent1_round3
        results_agent1_round3 = extract_true_false(line[2]['content'])
        true_count = results_agent1_round3.count('True')
        if len(results_agent1_round3) > 0:
            ratio_agent1_round3 = true_count / len(results_agent1_round3)
        else:
            ratio_agent1_round3 = 0
        FGFS_agent1_round3.append(ratio_agent1_round3)
        # agent2_round1
        results_agent2_round1 = extract_true_false(line[3]['content'])
        true_count = results_agent2_round1.count('True')
        if len(results_agent2_round1) > 0:
            ratio_agent2_round1 = true_count / len(results_agent2_round1)
        else:
            ratio_agent2_round1 = 0
        FGFS_agent2_round1.append(ratio_agent2_round1)
        # agent2_round2
        results_agent2_round2 = extract_true_false(line[4]['content'])
        true_count = results_agent2_round2.count('True')
        if len(results_agent2_round2) > 0:
            ratio_agent2_round2 = true_count / len(results_agent2_round2)
        else:
            ratio_agent2_round2 = 0
        FGFS_agent2_round2.append(ratio_agent2_round2)
        # agent2_round3
        results_agent2_round3 = extract_true_false(line[5]['content'])
        true_count = results_agent2_round3.count('True')
        if len(results_agent2_round3) > 0:
            ratio_agent2_round3 = true_count / len(results_agent2_round3)
        else:
            ratio_agent2_round3 = 0
        FGFS_agent2_round3.append(ratio_agent2_round3)


    average_value1 = sum(FGFS_agent1_round1) / len(FGFS_agent1_round1)
    average_value2 = sum(FGFS_agent1_round2) / len(FGFS_agent1_round2)
    average_value3 = sum(FGFS_agent1_round3) / len(FGFS_agent1_round3)
    average_value4 = sum(FGFS_agent2_round1) / len(FGFS_agent2_round1)
    average_value5 = sum(FGFS_agent2_round2) / len(FGFS_agent2_round2)
    average_value6 = sum(FGFS_agent2_round3) / len(FGFS_agent2_round3)

print(average_value1, average_value2, average_value3, average_value4, average_value5, average_value6)











