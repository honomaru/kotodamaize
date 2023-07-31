import os
import openai
import re

MODEL_NAME = "gpt-4"
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

BASE_PROMPT_DICT={
    "radio": "Arrange the following text in the style of a radio conversation, with the MC and guest taking turns speaking. Begin each line with 'A: ' if the speaker is an MC, and 'B: ' if the speaker is a guest. The first speaker must be the MC. \n",
    "lesson": "Arrange the following text in the style of college lesson, with a teacher and a student taking turns speaking. Begin each line with 'A: ' if the speaker is a teacher, and 'B: ' if the speaker is a student. The first speaker must be the Teacher.\n",
    "comedy": "Arrange the following text in the style of a comedy act, with a comedians A and B taking turns speaking. Begin each line with 'A: ' or 'B: ' to identify the speaker. All outputs should be vocalizable strings. For example, (laughs) should be Hahaha!\n",
    "narrative": "Arrange the following text in the style of narrative. Prefix the output with 'A: '. Don't use the 'A: ' notation in the rest of the output."
}

SPEAKER_NAME_DICT = {
    "radio":["MC: ","Guest: "],
    "narrative":[""],
    "lesson":["Teacher: ","Student: "],
    "comedy":["Comedian A: ","Comedian B: "]
}

def text2text(text, mode):
    """
    #Transform text to text & Save to specified file_path and return error if exists        
    #Returns:
    #    file_path (str): file path of transformed text (output of llm)
    """
    base_prompt = BASE_PROMPT_DICT[mode]
    prompt = base_prompt + text
    transformed_text = transform_text(prompt)
    # save text to file
    #path = f'./output/{task_id}/{mode}_text.txt'
    #with open(path,"w") as f:
    #    f.write(transformed_text)
    return transformed_text

def transform_text(prompt):
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    res = response.choices[0]["message"]["content"].strip() 
    return res

def display_text(text, mode="radio", keywords=["A: ","B: "]):
    # get speaker names corresponds to mode
    # ex)["MC: ", "Guest: "]
    speaker_names = SPEAKER_NAME_DICT[mode] 
    # register pattern
    pattern = '|'.join(map(re.escape, keywords))
    # insert \n every time pattern appears
    result = re.sub(pattern, lambda match: speaker_names[0] if match.group(0) == keywords[0] else speaker_names[1], text)
    return result
    

def main():
    SPEAKER_NAME_DICT = {
    "radio":["MC: ","Guest: "]
    }
    text = """
    Title: The Wonders of Quantum Entanglement: Spooky Action at a Distance

Introduction:

Welcome to my scientific blog, where we delve into the fascinating world of quantum physics! Today's topic revolves around one of the most intriguing phenomena in the quantum realm - "Quantum Entanglement." Prepare to have your mind blown by the counterintuitive and mysterious nature of this phenomenon.

What is Quantum Entanglement?

Quantum entanglement is a bizarre and captivating phenomenon that occurs when two or more particles become linked in such a way that the state of one particle is dependent on the state of another, regardless of the distance between them. These particles could be photons, electrons, or even more complex entities like atoms or molecules.

The EPR Paradox:

Quantum entanglement was first brought to the limelight through a thought experiment proposed by Einstein, Podolsky, and Rosen (EPR) in 1935. They intended to show that quantum mechanics was an incomplete theory, and there must be "hidden variables" governing the behavior of particles. However, later experiments proved them wrong, giving rise to the quantum mechanical interpretation.

Non-Local Connections:

One of the most perplexing aspects of quantum entanglement is its non-locality. When two particles become entangled, their fates become intertwined. This means that if you measure one particle's property, such as its spin or polarization, the other particle's corresponding property will instantaneously be determined, regardless of the vast distance separating them. This instantaneous influence has been famously referred to by Einstein as "spooky action at a distance."

Applications of Quantum Entanglement:

Beyond its mind-boggling conceptual implications, quantum entanglement plays a vital role in modern technology. Quantum computing and quantum cryptography heavily rely on exploiting the correlations between entangled particles to perform tasks that classical computers cannot achieve efficiently.

Bell's Inequality and Tests of Entanglement:

Physicist John Bell proposed an inequality that could test whether observed correlations between entangled particles could be explained by classical or local hidden variables. Numerous experiments have been conducted, consistently violating Bell's inequality, confirming the presence of genuine quantum entanglement.

Quantum Entanglement and the Nature of Reality:

Quantum entanglement raises profound questions about the fundamental nature of reality, challenging our classical intuitions. The idea that the state of one particle can be connected to another, irrespective of distance, shakes the very foundation of our understanding of the universe.

Conclusion:

Quantum entanglement remains one of the most extraordinary and mysterious phenomena in the realm of science. Its implications extend beyond the theoretical realm and have practical applications in cutting-edge technologies. As we continue to unravel the secrets of the quantum world, we are confronted with a universe that defies conventional wisdom and beckons us to explore further into the wonders of nature.

Thank you for joining me on this entangled journey through the captivating world of quantum physics. Until next time, keep questioning, keep exploring, and keep embracing the wonders of science!
    """
    mode = "radio"
    transformed_text = display_text(text2text(text, mode))
    with open("transformed_text.txt","w") as f:
        f.write(transformed_text)

if __name__ == "__main__":
    main()
