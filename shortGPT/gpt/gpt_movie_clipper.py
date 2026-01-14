import json
import re
from shortGPT.gpt.gpt_utils import llm_completion, load_local_yaml_prompt


def format_transcript_for_llm(whisper_analysis):
    formatted_lines = []
    for segment in whisper_analysis.get('segments', []):
        start = segment.get('start', 0)
        end = segment.get('end', 0)
        text = segment.get('text', '').strip()
        if text:
            formatted_lines.append(f"[{start:.2f} - {end:.2f}] \"{text}\"")
    return "\n".join(formatted_lines)


def extract_json_from_response(response):
    json_match = re.search(r'\[[\s\S]*\]', response)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass
    
    return []


def detect_interesting_moments(whisper_analysis, min_duration=15, max_duration=45, num_clips=3):
    chat_prompt, system_prompt = load_local_yaml_prompt('prompt_templates/movie_clipper_detect_moments.yaml')
    
    transcript = format_transcript_for_llm(whisper_analysis)
    
    if not transcript.strip():
        return []
    
    chat_prompt = chat_prompt.replace('<<TRANSCRIPT>>', transcript)
    chat_prompt = chat_prompt.replace('<<MIN_DURATION>>', str(min_duration))
    chat_prompt = chat_prompt.replace('<<MAX_DURATION>>', str(max_duration))
    chat_prompt = chat_prompt.replace('<<NUM_CLIPS>>', str(num_clips))
    
    response = llm_completion(
        chat_prompt=chat_prompt,
        system=system_prompt,
        temp=0.3,
        max_tokens=2000,
        remove_nl=False
    )
    
    moments = extract_json_from_response(response)
    
    validated_moments = []
    for moment in moments:
        if all(key in moment for key in ['start_time', 'end_time']):
            validated_moments.append({
                'start_time': float(moment['start_time']),
                'end_time': float(moment['end_time']),
                'reason': moment.get('reason', ''),
                'clip_title': moment.get('clip_title', 'Untitled Clip')
            })
    
    return validated_moments


def get_clip_suggestions_summary(moments):
    summary_lines = []
    for i, moment in enumerate(moments, 1):
        duration = moment['end_time'] - moment['start_time']
        summary_lines.append(
            f"Clip {i}: \"{moment['clip_title']}\" "
            f"({moment['start_time']:.1f}s - {moment['end_time']:.1f}s, {duration:.1f}s duration)\n"
            f"  Reason: {moment['reason']}"
        )
    return "\n\n".join(summary_lines)
