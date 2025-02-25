from shortGPT.gpt import gpt_utils
import json
def extractJsonFromString(text):
    start = text.find('{') 
    end = text.rfind('}') + 1
    if start == -1 or end == 0:
        raise Exception("Error: No JSON object found in response")
    json_str = text[start:end]
    return json.loads(json_str)


def getImageQueryPairs(captions, n=15, maxTime=2):
    chat, _ = gpt_utils.load_local_yaml_prompt('prompt_templates/editing_generate_images.yaml')
    prompt = chat.replace('<<CAPTIONS TIMED>>', f"{captions}").replace("<<NUMBER>>", f"{n}")
    
    try:
        # Get response and parse JSON
        res = gpt_utils.llm_completion(chat_prompt=prompt)
        data = extractJsonFromString(res)
        # Convert to pairs with time ranges
        pairs = []
        end_audio = captions[-1][0][1]
        
        for i, item in enumerate(data["image_queries"]):
            time = item["timestamp"]
            query = item["query"]
            
            # Skip invalid timestamps
            if time <= 0 or time >= end_audio:
                continue
                
            # Calculate end time for this image
            if i < len(data["image_queries"]) - 1:
                next_time = data["image_queries"][i + 1]["timestamp"]
                end = min(time + maxTime, next_time)
            else:
                end = min(time + maxTime, end_audio)
                
            pairs.append(((time, end), query + " image"))
            
        return pairs
        
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from LLM")
        return []
    except KeyError:
        print("Error: Malformed JSON structure")
        return []
    except Exception as e:
        print(f"Error processing image queries: {str(e)}")
        return []

def getVideoSearchQueriesTimed(captions_timed):
    """
    Generate timed video search queries based on caption timings.
    Returns list of [time_range, search_queries] pairs.
    """
    err = ""

    for _ in range(4):
        try:
            # Get total video duration from last caption
            end_time = captions_timed[-1][0][1]
            
            # Load and prepare prompt
            chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/editing_generate_videos.yaml')
            prompt = chat.replace("<<TIMED_CAPTIONS>>", f"{captions_timed}")
            
            # Get response and parse JSON
            res = gpt_utils.llm_completion(chat_prompt=prompt, system=system)
            data = extractJsonFromString(res)
            
            # Convert to expected format
            formatted_queries = []
            for segment in data["video_segments"]:
                time_range = segment["time_range"]
                queries = segment["queries"]
                
                # Validate time range
                if not (0 <= time_range[0] < time_range[1] <= end_time):
                    continue
                    
                # Ensure exactly 3 queries
                while len(queries) < 3:
                    queries.append(queries[-1])
                queries = queries[:3]
                
                formatted_queries.append([time_range, queries])
                
            # Verify coverage
            if not formatted_queries:
                raise ValueError("Generated segments don't cover full video duration")
                
            return formatted_queries
        except Exception as e:
            err = str(e)
            print(f"Error generating video search queries {err}")
    raise Exception(f"Failed to generate video search queries {err}")