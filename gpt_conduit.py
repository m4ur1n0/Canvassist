from openai import OpenAI
import json
import os
import config
import sys
"""
"Provide a set of numbered steps outlining an effective strategy for completing a homework assignment. The homework assignment is 
described by the text enclosed in single quotes: '{description}'. Write the advice in JSON format, where each step number maps to 
the description for that step of the effective work strategy. Additionally, create a JSON file containing a dictionary of helpful 
websites for completing the assignment. Each entry in the dictionary should have a title as its key and a URL as its value. Finally, 
include another JSON file containing a single integer representing the estimated time, in minutes, to complete this assignment. If 
you encounter any difficulties, such as trouble estimating the time required. Ensure that each JSON file follows a consistent structure. 
If you are unable to find relevant websites, return an empty JSON dictionary for that file instead."
"""


api_key = config.openai_api_key
client = OpenAI(api_key=api_key)

prompt_format = ""
def generate_steps_prompt(description):
    # EXPECTS A FULL CLASS DESCRIPTION AS PARAMETER
    # this function returns a prompt to feed the AI
    if "'" in description:
        temp = description.split("'")
        description = "".join(temp)

    """
    You must create one JSON file containing a dictionary. Respond to me only with this JSON file and absolutely nothing else. 
    You need to create a step-by-step plan outlining a specific strategy to efficiently complete an assignment. The assignment's 
    description will follow, enclosed in single quotes: 'Nicolas Malebranche, Search after Truth: iii.ii.6 (i, 220-2); vi.ii.3 
    (i, 225-33)\nQ: What are occasional causes--are they real causes?\n\u00a0'. The JSON file needs to map the number of each step 
    in the success strategy to the string which describes the step itself. Make your advice as specific to the assignment description 
    as possible. If you cannot come up with anything specific to the assignment description, it is okay to give a broader strategy. 
    It is absolutely crucial that you respond with a JSON dictionary. It is also absolutely crucial that this is the only thing you 
    respond with at all. I am an API using your services, and I need to be able to json.load() this response without making any modifications.
    """
    return f"You must create one JSON file containing a dictionary. Respond to me only with this JSON file and absolutely nothing else. You need to create a step-by-step plan outlining a specific strategy to efficiently complete an assignment. The assignment's description will follow, enclosed in single quotes: ' {description} '. The JSON file needs to map the number of each step in the success strategy to the string which describes the step itself. Make your advice as specific to the assignment description as possible. If you cannot come up with anything specific to the assignment description, it is okay to give a broader strategy. It is absolutely crucial that you respond with a JSON dictionary. It is also absolutely crucial that this is the only thing you respond with at all. I am an API using your services, and I need to be able to json.load() this response without making any modifications."
    # return f"Provide a set of numbered steps outlining an effective strategy for completing a homework assignment. The homework assignment is described by the text enclosed in single quotes: '{description}'. Write the advice in JSON format, where each step number maps to the description for that step of the effective work strategy. Additionally, create a JSON file containing a dictionary of helpful websites for completing the assignment. Each entry in the dictionary should have a title as its key and a URL as its value. Finally, include another JSON file containing a single integer representing the estimated time, in minutes, to complete this assignment. If you encounter any difficulties, such as trouble estimating the time required. Ensure that each JSON file follows a consistent structure. If you are unable to find relevant websites, return an empty JSON dictionary for that file instead. It is absolutely crucial that you do return all 3 JSON dictionaries, they all must be formatted exactly as specified, and you must return absolutely nothing else."
def generate_urls_prompt(description):
    # EXPECTS A FULL CLASS DESCRIPTION AS PARAMETER
    if "'" in description:
        temp = description.split("'")
        description = "".join(temp)

    """
    You must create one JSON file containing a dictionary. Respond to me only with this JSON file and absolutely nothing else. 
    You need to create a list of website urls that may prove helpful when completing a specific assignment. The assignment's 
    description will follow, enclosed in single quotes: '   '. The JSON file needs to map the name of the website to the actual 
    url of the website. Make your advice as specific to the assignment description as possible. If, AND ONLY IF, you cannot come 
    up with anything specific to the assignment description, it is okay to give websites that will be useful more broadly. It is 
    absolutely crucial that you respond with a JSON dictionary. It is also absolutely crucial that this is the only thing you 
    respond with at all. I am an API using your services, and I need to be able to json.load() this response without making any modifications.
    """

    return f"You must create one JSON file containing a dictionary. Respond to me only with this JSON file and absolutely nothing else. You need to create a list of website urls that may prove helpful when completing a specific assignment. The assignment's description will follow, enclosed in single quotes: ' {description} '. The JSON file needs to map the name of the website to the actual url of the website. Make your advice as specific to the assignment description as possible. If, AND ONLY IF, you cannot come up with anything specific to the assignment description, it is okay to give websites that will be useful more broadly. It is absolutely crucial that you respond with a JSON dictionary. It is also absolutely crucial that this is the only thing you respond with at all. I am an API using your services, and I need to be able to json.load() this response without making any modifications."
def generate_time_estimate_prompt(description):
    # EXPECTS A FULL CLASS DESCRIPTION AS PARAMETER
    """You must create one JSON file containing a dictionary. Respond to me only with this JSON file and absolutely nothing else. 
    You need to create an estimate, in minutes, of how long it might take to complete a specific assignment. The assignment's 
    description will follow, enclosed in single quotes: ' {description} '. The JSON file needs to map the key 'time' to the SINGLE 
    INTEGER minute estimate you generated. Make your estimate as specific to the assignment description as possible. If, AND ONLY IF, 
    you cannot come up with anything specific to the assignment description, it is okay to make a general guess, but in these cases 
    it would be better to overestimate the time rather than underestimate. It is absolutely crucial that you respond with a JSON dictionary. 
    It is also absolutely crucial that this is the only thing you respond with at all. I am an API using your services, and I need to be able 
    to json.load() this response without making any modifications"""
    
    return f"You must create one JSON file containing a dictionary. Respond to me only with this JSON file and absolutely nothing else. You need to create an estimate, in minutes, of how long it might take to complete a specific assignment. The assignment's description will follow, enclosed in single quotes: ' {description} '. The JSON file needs to map the key 'time' to the SINGLE INTEGER minute estimate you generated. Make your estimate as specific to the assignment description as possible. If, AND ONLY IF, you cannot come up with anything specific to the assignment description, it is okay to make a general guess, but in these cases it would be better to overestimate the time rather than underestimate. It is absolutely crucial that you respond with a JSON dictionary. It is also absolutely crucial that this is the only thing you respond with at all. I am an API using your services, and I need to be able to json.load() this response without making any modifications"

# def generate_prompt2(description): #just to use while we don't have integration w/ Canvas data
#    # description = text_dic['description']

#     return f"Give me a numbered steps to take to complete the following assignment wrapped by single quotes: '{description}' Please write the advice like normal, but put it in json format containing the step number and the description for that step. Also write another JSON file containing URLs and titles of websites which could be helpful for completing the assignment. Also, write another JSON file which contains a single estimated time to complete the assignment. Only return the three JSON files."

def generate_text(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    ) 
    # print(chat_completion.choices)  
    return chat_completion.choices[0].message.content

#def retrieve_json(generated_text):
    #generated_response = generated_text
    #response_dict = json.loads(generated_response)
    #return response_dict

def process_chatgpt_output(chatgpt_output):
    # Split the chatgpt_output into individual JSON strings
    json_strings = chatgpt_output.split("\n\n")
    # file_paths as a list because [0] should be steps [1] should be urls, and [2] should be minutes
    
    assignment_outp_content = {}
    # Process each JSON string separately
    for i, json_string in enumerate(json_strings):
        # print(i)
        # print(f"\n\n{json_string}\n\n")
        try:
            # Parse the JSON string into a dictionary
            json_data = json.loads(json_string)
            if json_data == {}:
                pass
            else:
                assignment_outp_content = json_data
            

        except json.JSONDecodeError as e:
            print(f"Error loading JSON file {i}: {e}", file=sys.stderr)
        except KeyError as e:
            print(f"GPT returned too many responses : {e}", file=sys.stderr)
    
    # # STORE ALL 3 IN ONE DICTIONARY UNDER ASSIGNMENT NAME FILE NAME
    # assignment_outp_file_name = f"gpt_output_{assignment_id}.json"
    # file_path = "gpt_out/" + assignment_outp_file_name

    # # Save the JSON data to a file
    # with open(file_path, "w") as json_file:
    #     json.dump(obj=assignment_outp_content, fp=json_file, indent=4)

    # print(f"JSON file {i} saved successfully: {file_path}")
    
    # return file_path
    return assignment_outp_content


def get_json_from_assignment_id(assignment_id):
    # takes in one assignment ID, then asks chatgpt about it, and saves 3 separate documents
    with open("json_out/assignment_ids_to_info.json", "r") as file:
        try:
            info = json.load(file)
            assignment_info = info[assignment_id]
        except KeyError:
            print(f"Assignment ID ' {assignment_id} ' not in database", path=sys.stderr)
            return
        
        description = assignment_info['description']

        steps_prompt = generate_steps_prompt(description)
        urls_prompt = generate_urls_prompt(description)
        time_prompt = generate_time_estimate_prompt(description)

        steps_output = generate_text(steps_prompt)
        urls_output = generate_text(urls_prompt)
        time_output = generate_text(time_prompt)

        output_dict = {}
        dict1 = process_chatgpt_output(chatgpt_output=steps_output)
        dict2 = process_chatgpt_output(chatgpt_output=urls_output)
        dict3 = process_chatgpt_output(chatgpt_output=time_output)

        output_dict.update(dict1)
        output_dict.update(dict2)
        output_dict.update(dict3)

        with open('json_out/assignment_ids_to_info.json', 'r') as file:
            existing_data = json.load(file)

        # Add the new key-value pair
        existing_data[assignment_id]['steps'] = dict1
        existing_data[assignment_id]['urls'] = dict2
        existing_data[assignment_id]['time_estimate'] = dict3

        print(f"DONE WITH {assignment_id}")

        # Write the updated data back to the JSON file
        with open('json_out/assignment_ids_to_info.json', 'w') as file:
            json.dump(existing_data, file, indent=4)

def fulfill_thread_list(assg_list):
    for ass_id in assg_list:
        get_json_from_assignment_id(ass_id)

get_json_from_assignment_id("18760000001401668")