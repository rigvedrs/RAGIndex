from openai import OpenAI
# import os

def combine_prompts(full_chunk, answer):
    instruction_prompt = f''' 
    Prompt:
    # Role:
    you are an expert in content writting . Your job is to find the exact context used in the full chunk text to generate given answer
    # Instruction:
    - Generate the exact context used from {full_chunk} to generate given answer {answer}
    - It should be in 5,6 senetnces.
    - Use same words and formating used in full_chunk.
'''
    return instruction_prompt

# Get OpenAI API key with proper error handling
# openai_api_key = os.environ.get('OPENAI_API_KEY')
# if not openai_api_key:
#     print("Warning: OPENAI_API_KEY environment variable not set. Context generation will not work.")

def get_context(full_chunk, answer):
    # if not openai_api_key:
    #     return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
    
    try:
        client = OpenAI()
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct-0914",
            prompt=combine_prompts(full_chunk, answer),
            temperature=0.2,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["#", ";"]
        )

        if hasattr(response, 'choices') and response.choices:
            first_choice_text = response.choices[0].text
        else:
            first_choice_text = "No choices found in the response."
        # print(first_choice_text)
        return first_choice_text
    except Exception as e:
        return f"Error generating context: {str(e)}"
