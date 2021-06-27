from sys import argv
from typing import List
import os
from time import sleep

def parse(code_lines: List[str]):
    alphabet_start = 0
    alphabet_end = 0
    try: 
        alphabet_start = code_lines.index("BEGIN ALPHA")
        alphabet_end = code_lines.index("END ALPHA")
        if alphabet_end - alphabet_start <= 1:
            print("Alphabet has no symbols")
            return
    except:
        print("Couldn't find BEGIN ALPHA or END ALPHA")
        return

    alphabet = []
    for i in range(alphabet_start + 1, alphabet_end):
        alphabet.append(code_lines[i].strip())
    
    rules_start = 0
    rules_end = 0
    try: 
        rules_start = code_lines.index("BEGIN RULES")
        rules_end = code_lines.index("END RULES")
        if rules_end - rules_start <= 1:
            print("No rules specified")
            return
    except:
        print("Couldn't find BEGIN RULES or END RULES")
        return

    rules = []
    for i in range(rules_start + 1, rules_end):
        rule = code_lines[i].strip()
        if rule.find("->") == -1:
            print("Invalid rule: " + rule)
            return
        
        rule_parts = rule.split("->")
        if len(rule_parts) != 2:
            print("Invalid rule: " + rule)
            return

        symbol = rule_parts[0].strip()
        if not symbol in alphabet:
            print("Symbol used in rule is not part of alphabet: " + symbol)

        if symbol in list(map(lambda r: r["symbol"], rules)):
            print("Symbol with more than one rule specified: " + symbol)
            return
        
        production = rule_parts[1].strip()
        rules.append({
            "symbol": symbol,
            "production": production,
        })

    initial_state_start = 0
    initial_state_end = 0
    try: 
        initial_state_start = code_lines.index("BEGIN INITIALSTATE")
        initial_state_end = code_lines.index("END INITIALSTATE")
        if initial_state_end - initial_state_start <= 1:
            print("No initial state specified")
            return
    except:
        print("Couldn't find BEGIN INITIALSTATE or END INITIALSTATE")
        return

    initial_state = ""
    for i in range(initial_state_start + 1, initial_state_end):
        initial_state += code_lines[i].strip()


    return alphabet, rules, initial_state

def interpret(rules, initial_state: str):
    m = 2 # 2-tag system

    current_state = initial_state
    while True:
        print(current_state)
        if current_state == "":
            print("Reached void state")
            return

        if current_state[0] == "H":
            print("Reached halt")
            return
        
        matched = False
        for rule in rules:
            symbol = rule["symbol"]
            production = rule["production"]
            if current_state[0:len(symbol)] == symbol:
                current_state = current_state[m:] + production
                matched = True
                break
    
        if not matched:
            print("Couldn't match any rules: " + current_state)
            return


if __name__ == "__main__":
    file_path = argv[1]

    if not os.path.exists(file_path):
        print("File not found")
    else:
        with open(file_path, "r") as f:
            contents = list(map(lambda c: c.strip(), f.readlines()))
            parsed = parse(contents)

            if parsed is None:
                print("Parse failed")
            else:
                alphabet, rules, initial_state = parsed
                interpret(rules, initial_state)
            
        