from llm_helper import llm
from few_shots import FewShots
fs=FewShots()
def length_to_lines(length):
    if length == "Short":
        return "1 to 9 lines"
    elif length == "Medium":
        return "10 to 30 lines"
    else :
        return "More than 30 lines"

def get_prompt(length,language,topic):
    length_lines = length_to_lines(length)
    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.
    
    1) Topic: {topic}
    2) Length: {length_lines}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of English and Hinglish
    The script for the generated post should always be English
    
    '''
    examples = fs.get_filtered_posts(length,language,topic)
    if len(examples)>0:
        i=1
        prompt+= "4) Use the writing style as per the following examples."
        for post in (examples):
            post_text=post["text"]
            prompt+= f"\n\nExample {i}: \n\n {post_text}"
            i+=1
            if i==2:
                break
    return prompt


def post_generate(length,language,topic):
    prompt = get_prompt(length,language,topic)
    response = llm.invoke(prompt)
    return response.content

if __name__=="__main__":
    post = get_prompt("Short", "English", "Motivation")
    print(post)