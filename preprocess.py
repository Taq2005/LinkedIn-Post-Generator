import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm
def extract_metadata(post):
    template = '''
    You are give a LinkedIn post. You need to extract the number of lines, language of the post and tags.
    1. Return a valid JSON.  No preamble
    2. JSON object should have exactly three keys: line_count, language, tags.
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish(English+Hindi)
    Here is an actual post on which you need to perform these tasks
    {post}
    '''
    pt=PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input = {'post': post})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except:
        raise OutputParserException()
    return res


def get_unified_tags(post_with_meta):
    unique_tags = set()
    for post in post_with_meta:
        unique_tags.update(post['tags'])
    unique_tag_list = ', '.join(unique_tags)
    template = '''
    I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list
    Example 1: "Jobseekers","Job Hunting","JobHunt" and similar can all be merged into a single tag "Job Search"
    Example 2: "Motivation", "Inspiration" can be merged into "Motivation"
    Example 3: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should follow title case convention example: "Motivation", "Job Search".
    3. Output should be a JSON object, no preamble
    4. Output should have a mapping to original tag and unified tag.
    Example: {{"Jobseeker": "Job Search","Job Hunting:: "Job Search", "Motivation": "Motivation"}} 

    Here is the list of tags:
    {tags}

    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'tags': str(unique_tag_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big")
    return res


def process_posts(raw_file_path, processed_path="data/processed.json"):
    enriched_data=[]
    with open(raw_file_path, encoding="utf-8") as file:
        raw_data = json.load(file)
        for post in raw_data:
            extract_meta=extract_metadata(post['text'])
            post_with_meta=post | extract_meta
            enriched_data.append(post_with_meta)
    unified_tags=get_unified_tags(enriched_data)
    for epost in enriched_data:
        current_tags=epost['tags']
        new_tags={unified_tags[tag] for tag in current_tags}
        epost['tags']=list(new_tags)
    with open(processed_path, "w", encoding="utf-8") as outfile:
        json.dump(enriched_data, outfile, indent=4)


if __name__== "__main__":
    process_posts("data/data.json", "data/processed.json")