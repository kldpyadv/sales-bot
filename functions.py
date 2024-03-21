import openai
import ast
import re
import pandas as pd
import json

def send_user_mail(mail,name):
    conversation = "Thank you! I'll send the details to your email shortly. If you have any further questions or need assistance, feel free to reach out!"
    return conversation

def initialize_conversation():
    '''
    Returns a list [{"role": "system", "content": system_message}]
    '''
    
    delimiter = "####"
    example_user_req = {'GPU intensity': 'high','Display quality': 'high','Portability': 'low','Multitasking': 'high','Processing speed': 'high','Budget': '150000'}
    
    system_message = f"""
b
    You are an intelligent laptop gadget expert and your goal is to find the best laptop for a user.
    You need to ask relevant questions and understand the user profile by analysing the user's responses.
    You final objective is to fill the values for the different keys ('GPU intensity','Display quality','Portability','Multitasking','Processing speed','Budget') in the python dictionary and be confident of the values.
    These key value pairs define the user's profile.
    The python dictionary looks like this {{'GPU intensity': 'values','Display quality': 'values','Portability': 'values','Multitasking': 'values','Processing speed': 'values','Budget': 'values'}}
    The values for all keys, except 'budget', should be 'low', 'medium', or 'high' based on the importance of the corresponding keys, as stated by user. 
    The value for 'budget' should be a numerical value extracted from the user's response. 
    The values currently in the dictionary are only representative values. 
    
    {delimiter}Here are some instructions around the values for the different keys. If you do not follow this, you'll be heavily penalised.
    - The values for all keys, except 'Budget', should strictly be either 'low', 'medium', or 'high' based on the importance of the corresponding keys, as stated by user.
    - The value for 'budget' should be a numerical value extracted from the user's response.
    - 'Budget' value needs to be greater than or equal to 25000 INR. If the user says less than that, please mention that there are no laptops in that range.
    - Do not randomly assign values to any of the keys. The values need to be inferred from the user's response.
    {delimiter}

    To fill the dictionary, you need to have the following chain of thoughts:
    {delimiter} Thought 1: Ask a question to understand the user's profile and requirements. \n
    If their primary use for the laptop is unclear. Ask another question to comprehend their needs. Never mentions words like dictionary to the user, keep question around real world user should feel like he is talking to the machine
    You are trying to fill the values of all the keys ('GPU intensity','Display quality','Portability','Multitasking','Processing speed','Budget') in the python dictionary by understanding the user requirements.
    Identify the keys for which you can fill the values confidently using the understanding. \n
    Remember the instructions around the values for the different keys. 
    Answer "Yes" or "No" to indicate if you understand the requirements and have updated the values for the relevant keys. \n
    If yes, proceed to the next step. Otherwise, rephrase the question to capture their profile. \n{delimiter}

    {delimiter}Thought 2: Now, you are trying to fill the values for the rest of the keys which you couldn't in the previous step. 
    Remember the instructions around the values for the different keys. Ask questions you might have for all the keys to strengthen your understanding of the user's profile.
    Answer "Yes" or "No" to indicate if you understood all the values for the keys and are confident about the same. 
    If yes, move to the next Thought. If no, ask question on the keys whose values you are unsure of. \n
    It is a good practice to ask question with a sound logic as opposed to directly citing the key you want to understand value for.{delimiter}

    {delimiter}Thought 3: Check if you have correctly updated the values for the different keys in the python dictionary. 
    If you are not confident about any of the values, ask clarifying questions. {delimiter}

    {delimiter}Thought 4: Once you have the user requirements and you have shown laptops to user ask the user if he wants to get the laptop details on there mail  {delimiter}

    Follow the above chain of thoughts and only output the final updated python dictionary. \n


    {delimiter} Here is a sample conversation 1 between the user and assistant:
    User: "Hi, I'm looking for a laptop that can handle game development tasks."
    Assistant: "Great, game development can be quite demanding. First off, which game engines or development tools do you typically use?"
    User: "I use Unity and Unreal Engine for most of my projects."
    Assistant: "Both of those engines require significant GPU power for rendering. How often do you work with complex scenes or high-resolution textures?"
    User: "Pretty often, I'm usually working on projects with complex graphics."
    Assistant: "That definitely necessitates a laptop with high GPU intensity. Regarding your display needs, are you looking for a laptop with a high refresh rate and color accuracy?"
    User: "Yes, a high-quality display is crucial for me to accurately visualize and edit my work."
    Assistant: "Understood. Multitasking is also essential in game development. Do you usually have multiple applications or software running simultaneously?"
    User: "Absolutely, I often switch between the game engine, code editor, and graphic design software."
    Assistant: "It sounds like you'll need a laptop with high processing speed to handle all those tasks without lag. Considering all this, how important is portability for you?"
    User: "I mostly work from my home office, so the laptop doesn't need to be ultra-portable."
    Assistant: "Lastly, could you share your budget for the laptop?"
    User: "My budget is around 150,000 INR."
    Assistant: "{example_user_req}"
    {delimiter}

    {delimiter} Here is a sample conversation 2 between the user and assistant:
    User: "I'm looking for a laptop capable of developing and running VR applications."
    Assistant: "VR development is quite demanding. Could you share which VR platforms you're developing for?"
    User: "I develop mainly for Oculus Rift and HTC Vive."
    Assistant: "Those platforms require high GPU intensity for smooth performance. Do you also engage in creating high-resolution textures or 3D models?"
    User: "Yes, most of my work involves detailed 3D modeling and realistic textures."
    Assistant: "Given these requirements, a high-quality display is also essential for fine-tuning visuals. What display specifications are you looking for?"
    User: "Ideally, something with high resolution and a good refresh rate."
    Assistant: "Understood. With VR development, multitasking and processing speed must be crucial as well. How often do you find yourself running multiple resource-intensive applications simultaneously?"
    User: "All the time. I usually have my development environment, graphic design software, and VR simulation running at once."
    Assistant: "That's quite the workload. How important is portability to you, considering the heavy requirements of VR development?"
    User: "I prefer performance over portability. The laptop will mostly be stationary."
    Assistant: "Lastly, could you let me know your budget for this laptop?"
    User: "I can stretch up to 200,000 INR."
    Assistant: "Given your specialized needs for high GPU intensity, a top-tier display, the ability to multitask with high processing speed, and your budget, I'm checking our current options... Unfortunately, based on the very specific and high-end requirements you've mentioned, it seems we don't have a laptop in our inventory that perfectly matches all your criteria."
    User: "That's disappointing. What do you suggest?"
    Assistant: "I understand it's not the ideal situation. However, we can connect you with one of our human experts who specializes in high-performance computing solutions. They might be able to provide a custom solution or advise on upcoming models that meet your requirements. Would you like me to arrange a consultation for you?"
    User: "Yes, that would be helpful."
    Assistant: "Great! Could you please provide your name and the best way to contact you? Our expert will reach out to discuss your needs in detail."
    User: "[Provides name and contact information]"
    Assistant: "Thank you! Our expert will contact you shortly to explore the best options for your VR development needs. If you have any more questions in the meantime, feel free to reach out!"
    Start with a short welcome message and encourage the user to share their requirements. Do not start with Assistant: "
    {delimiter}

    {delimiter}user should never know what functionality we are doing in the backend keep it discrete strictly no codes or functions name in the assistant response
    {delimiter}

    """
    conversation = [{"role": "system", "content": system_message}]
    return conversation

custom_functions = [
    {
        "name": "send_user_mail",
        "description": "Function to send mail to user, called when we have email id and name of the user",
        "parameters": {
            "type": "object",
            "properties": {
                "mail": {
                    "type": "string",
                    "description": "Email Id of the user",
                },
                "uname": {
                    "type": "string",
                    "description": "Name of the user",
                },
            },
            "required": ["mail", "uname"],
        },
    },
]

def get_chat_model_completions(messages):
    response = openai.chat.completions.create(
        model ="gpt-3.5-turbo-0613",
        messages = messages,
        functions = custom_functions,
        function_call = 'auto',
        temperature = 0, # this is the degree of randomness of the model's output
        max_tokens = 300
    )
    
    response_message = response.choices[0].message
    if response_message.function_call:
        output_string = response_message.function_call;
        # Convert the string output to a Python dictionary
        # The arguments field is also a JSON string, so parse it as well
        # Now, you can access mail, uname, and name
        
        function_name = output_string.name
        function_to_call = globals().get(function_name)
        if function_name != 'python' :
            arguments_dict = json.loads(output_string.arguments)
            mail = arguments_dict['mail']
            uname = arguments_dict['uname']
            if ("example" not  in mail and function_to_call):
                sendMail = function_to_call(mail, uname)
                return sendMail
            else:
                response = openai.chat.completions.create(
                model ="gpt-3.5-turbo-0613",
                messages = messages,
                temperature = 0, # this is the degree of randomness of the model's output
                max_tokens = 300
            )
            return response.choices[0].message.content
        else:
            response = openai.chat.completions.create(
                model ="gpt-3.5-turbo-0613",
                messages = messages,
                temperature = 0, # this is the degree of randomness of the model's output
                max_tokens = 300
            )
            return response.choices[0].message.content
        
    else:
        return response.choices[0].message.content



def moderation_check(user_input):
    response = openai.moderations.create(input=user_input)
    moderation_output = response.results[0]
    if moderation_output.flagged == True:
        return "Flagged"
    else:
        return "Not Flagged"


    
def intent_confirmation_layer(response_assistant):
    delimiter = "####"
    prompt = f"""
    You are a senior evaluator who has an eye for detail.
    You are provided an input. You need to evaluate if the input has the following keys: 'GPU intensity','Display quality','Portability','Multitasking',' Processing speed','Budget'
    Next you need to evaluate if the keys have the the values filled correctly.
    The values for all keys, except 'budget', should be 'low', 'medium', or 'high' based on the importance as stated by user. The value for the key 'budget' needs to contain a number with currency. If budget value is undefined and you have value for all other keys, ask user for budget, when you have value for all keys then only output yes.
    Values of all the keys is must for the output to be yes else output no and ask relevent questions to get the missing value of keys strictly follow this, cross check if all keys have values to be sure
    Output a string 'Yes' if the input contains the dictionary with the values correctly filled for all keys.
    Otherwise out the string 'No'.

    Here is the input: {response_assistant}
    Only output a one-word string - Yes/No.
    """


    confirmation = openai.completions.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt = prompt,
                    temperature=0)
    return confirmation.choices[0].text




def dictionary_present(response):
    delimiter = "####"
    user_req = {'GPU intensity': 'high','Display quality': 'high','Portability': 'medium','Multitasking': 'high','Processing speed': 'high','Budget': '200000 INR'}
    prompt = f"""You are a python expert. You are provided an input.
            You have to check if there is a python dictionary present in the string.
            It will have the following format {user_req}.
            Your task is to just extract and return only the python dictionary from the input.
            The output should match the format as {user_req}.
            The output should contain the exact keys and values as present in the input.

            Here are some sample input output pairs for better understanding:
            {delimiter}
            input: - GPU intensity: low - Display quality: high - Portability: low - Multitasking: high - Processing speed: medium - Budget: 50,000 INR
            output: {{'GPU intensity': 'low', 'Display quality': 'high', 'Portability': 'low', 'Multitasking': 'high', 'Processing speed': 'medium', 'Budget': '50000'}}

            input: {{'GPU intensity':     'low', 'Display quality':     'high', 'Portability':    'low', 'Multitasking': 'high', 'Processing speed': 'medium', 'Budget': '90,000'}}
            output: {{'GPU intensity': 'low', 'Display quality': 'high', 'Portability': 'low', 'Multitasking': 'high', 'Processing speed': 'medium', 'Budget': '90000'}}

            input: Here is your user profile 'GPU intensity': 'high','Display quality': 'high','Portability': 'medium','Multitasking': 'low','Processing speed': 'high','Budget': '200000 INR'
            output: {{'GPU intensity': 'high','Display quality': 'high','Portability': 'medium','Multitasking': 'high','Processing speed': 'low','Budget': '200000'}}
            {delimiter}

            Here is the input {response}

            """
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens = 2000
        # temperature=0.3,
        # top_p=0.4
    )
    return response.choices[0].text



def extract_dictionary_from_string(string):
    regex_pattern = r"\{[^{}]+\}"

    dictionary_matches = re.findall(regex_pattern, string)
    dictionary = {}

    # Extract the first dictionary match and convert it to lowercase
    if dictionary_matches:
        dictionary_string = dictionary_matches[0]
        dictionary_string = dictionary_string.lower()

        # Convert the dictionary string to a dictionary object using ast.literal_eval()
        dictionary = ast.literal_eval(dictionary_string)
    return dictionary




def compare_laptops_with_user(user_req_string):
    laptop_df= pd.read_csv('updated_laptop.csv')
    user_requirements = extract_dictionary_from_string(user_req_string)
    budget_str = str(user_requirements.get('budget', '0')).replace(',', '').split()[0]
    try:
        budget = int(budget_str)
    except ValueError:
        print(f"Invalid budget value: {budget_str}")
        budget = 0 
    #This line retrieves the value associated with the key 'budget' from the user_requirements dictionary.
    #If the key is not found, the default value '0' is used.
    #The value is then processed to remove commas, split it into a list of strings, and take the first element of the list.
    #Finally, the resulting value is converted to an integer and assigned to the variable budget.


    filtered_laptops = laptop_df.copy()
    filtered_laptops['Price'] = filtered_laptops['Price'].str.replace(',','').astype(int)
    filtered_laptops = filtered_laptops[filtered_laptops['Price'] <= budget].copy()
    #These lines create a copy of the laptop_df DataFrame and assign it to filtered_laptops.
    #They then modify the 'Price' column in filtered_laptops by removing commas and converting the values to integers.
    #Finally, they filter filtered_laptops to include only rows where the 'Price' is less than or equal to the budget.

    mappings = {
        'low': 0,
        'medium': 1,
        'high': 2
    }
    # Create 'Score' column in the DataFrame and initialize to 0
    filtered_laptops['Score'] = 0
    for index, row in filtered_laptops.iterrows():
        user_product_match_str = row['laptop_feature']
        laptop_values = extract_dictionary_from_string(user_product_match_str)
        score = 0

        for key, user_value in user_requirements.items():
            if key.lower() == 'budget':
                continue  # Skip budget comparison
            laptop_value = laptop_values.get(key, None)
            laptop_mapping = mappings.get(laptop_value.lower(), -1)
            user_mapping = mappings.get(user_value.lower(), -1)
            if laptop_mapping >= user_mapping:
                ### If the laptop value is greater than or equal to the user value the score is incremented by 1
                score += 1

        filtered_laptops.loc[index, 'Score'] = score

    # Sort the laptops by score in descending order and return the top 5 products
    top_laptops = filtered_laptops.drop('laptop_feature', axis=1)
    top_laptops = top_laptops.sort_values('Score', ascending=False).head(3)
    return top_laptops.to_json(orient='records')




def recommendation_validation(laptop_recommendation):
    data = json.loads(laptop_recommendation)
    data1 = []
    for i in range(len(data)):
        if data[i]['Score'] > 2:
            data1.append(data[i])

    return data1


def initialize_conv_reco(products):
    system_message = f"""
    You are an intelligent laptop gadget expert and you are tasked with the objective to \
    solve the user queries about any product from the catalogue: {products} and prompt user if they want the product details on there mail id. You start with brief summary of each laptop as the below format then asking user for there email and name\
    You should keep the user profile in mind while answering the questions.
    Keep the conversation real like you are an expert sales person with knowledge of laptop. Don't use hashtags or words like solution.\
    
    Start with a brief summary of each laptop in the following format, in decreasing order of price of laptops, keep the summary short around 40-50 tokens only for each laptop and then ask if user want the details on mail or not:
    1. <Laptop Name> : <Major specifications of the laptop>, <Price in Rs>
    2. <Laptop Name> : <Major specifications of the laptop>, <Price in Rs>
    Would you like to go over the details of these laptops here, or should I email the information to you?
    """
    conversation = [{"role": "system", "content": system_message }]
    return conversation