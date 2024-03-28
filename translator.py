
import json

from lib.openaiclient import client

def flush_characters(target_string=""):
    """
    removes unnecessary characters
    """
    return target_string.strip('Thanks.').strip("Thanks").strip("\"")


def translate_text(text=None, source_lan=None, lang_out=None):
    """
    translates the text into desired language.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
            "role": "system",
            "content": f"Input Text: Provide either {source_lan} text that needs to be translated into {lang_out}.\nOutput Expectation: The model is expected to produce the translated text in {lang_out}, maintaining the original meaning, context, and nuances of the input text. Ensure that the translation accurately reflects the semantics and intent of the original text without adding any additional information or altering the meaning.\nGuidelines:\nTranslate the input text into {lang_out} while preserving the grammatical structure and semantic coherence.\nMaintain consistency in tense, tone, and style throughout the translation.\nDon't translate maths symbols  and word PWU. \nEnsure that cultural references and idiomatic expressions are appropriately translated to maintain the intended meaning.\nAvoid adding any extraneous information or personal interpretations. Focus solely on translating the input text accurately into {lang_out}.\nEvaluation Criteria: The quality of the translation will be assessed based on the accuracy, fluency, and fidelity to the original meaning of the input text. The translated text should be comprehensible and coherent in {lang_out}, reflecting a faithful rendition of the source language.\nExample:\nInput: \"The quick brown fox jumps over the lazy dog.\nNote: The model should strictly adhere to the translation task and refrain from paraphrasing, summarizing, or embellishing the text. Focus solely on translating the input text accurately into {lang_out} while maintaining semantic fidelity.\nSpecial Note - Kindly Add  Word \"Thanks\" strictly in english after your response ."
            },
            {
            "role": "user",
            "content": text
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        ).model_dump_json()
    response = json.loads(response)
    content = ""
    for choice in response['choices']:
        content += flush_characters(choice['message']['content']) 
        
    return content

def translate_text_segments(transcript_segments=None, source_lan=None, lang_out=None):
    """
    translates the transcript_segments into desired language.
    """
    for timeslot, text in transcript_segments.items():
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                "role": "system",
                "content": f"Input Text: Provide either {source_lan} text that needs to be translated into {lang_out}.\nOutput Expectation: The model is expected to produce the translated text in {lang_out}, maintaining the original meaning, context, and nuances of the input text. Ensure that the translation accurately reflects the semantics and intent of the original text without adding any additional information or altering the meaning.\nGuidelines:\nTranslate the input text into {lang_out} while preserving the grammatical structure and semantic coherence.\nMaintain consistency in tense, tone, and style throughout the translation.\nDon't translate maths symbols  and word PWU. \nEnsure that cultural references and idiomatic expressions are appropriately translated to maintain the intended meaning.\nAvoid adding any extraneous information or personal interpretations. Focus solely on translating the input text accurately into {lang_out}.\nEvaluation Criteria: The quality of the translation will be assessed based on the accuracy, fluency, and fidelity to the original meaning of the input text. The translated text should be comprehensible and coherent in {lang_out}, reflecting a faithful rendition of the source language.\nExample:\nInput: \"The quick brown fox jumps over the lazy dog.\nNote: The model should strictly adhere to the translation task and refrain from paraphrasing, summarizing, or embellishing the text. Focus solely on translating the input text accurately into {lang_out} while maintaining semantic fidelity.\nSpecial Note - Kindly Add  Word \"Thanks\" strictly in english after your response ."
                },
                {
                "role": "user",
                "content": text
                }
            ],
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            ).model_dump_json()
        response = json.loads(response)
        content = ""
        for choice in response['choices']:
            content += flush_characters(choice['message']['content']) 
        transcript_segments[timeslot] = content
    return transcript_segments