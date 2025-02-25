import json
from shortGPT.gpt import gpt_utils

def generateScript(script_description, language):
    out = {'script': ''}
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/chat_video_script.yaml')
    chat = chat.replace("<<DESCRIPTION>>", script_description).replace("<<LANGUAGE>>", language)
    
    retries = 0
    max_retries = 3  # Set a reasonable limit on retries
    while not ('script' in out and out['script']) and retries < max_retries:
        try:
            result = gpt_utils.llm_completion(chat_prompt=chat, system=system, temp=1)
            print("Raw result:", result)  # Log the result for debugging

            # Clean and normalize the result before parsing
            result = result.strip()  # Remove leading/trailing whitespace/newlines
            
            # **NEW FIX: Remove Markdown artifacts like ```json ... ```
            if result.startswith("```json") and result.endswith("```"):
                result = result[7:-3].strip()  # Remove ```json (first 7 chars) and ``` (last 3 chars)

            # Check if the response has the "json " prefix and remove it
            if result.lower().startswith("json "):
                result = result[5:].strip()  # Remove "json " prefix and extra spaces

            # Validate JSON format
            if result.startswith('{') and result.endswith('}'):
                try:
                    out = json.loads(result)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}. Raw result: {result}")
                    retries += 1
            else:
                print(f"Unexpected format: {result}")
                retries += 1
        except Exception as e:
            retries += 1
            print(f"Error during script generation (attempt {retries}/{max_retries}): {e}")
            if retries >= max_retries:
                print("Max retries reached. Returning empty script.")
                break
    return out.get('script', 'Error generating script')

def correctScript(script, correction):
    out = {'script': ''}
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/chat_video_edit_script.yaml')
    chat = chat.replace("<<ORIGINAL_SCRIPT>>", script).replace("<<CORRECTIONS>>", correction)

    retries = 0
    max_retries = 3  # To prevent infinite loops

    while not ('script' in out and out['script']) and retries < max_retries:
        try:
            result = gpt_utils.llm_completion(chat_prompt=chat, system=system, temp=1)
            print("Raw result:", result)  # Debugging output

            # **New Fix: Remove Markdown artifacts like ```json ... ```
            if result.startswith("```json") and result.endswith("```"):
                result = result[7:-3].strip()

            # **Remove unexpected "json " prefix if present**
            if result.lower().startswith("json "):
                result = result[5:].strip()

            # Validate and parse JSON
            if result.startswith('{') and result.endswith('}'):
                out = json.loads(result)
            else:
                print(f"Unexpected format: {result}")
                retries += 1
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}. Raw result: {result}")
            retries += 1
        except Exception as e:
            retries += 1
            print(f"Error in correctScript (attempt {retries}/{max_retries}): {e}")

    return out.get('script', 'Error correcting script')