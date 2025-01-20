import sys
import re
import openai
import json


def gpt_prompt(tactic, before_state="No before state provided", after_state="No after state provided"):
    openai.api_key = ""


    NL_prompt = f'''
    You need to write an in-line comment which is a natural language version of a Lean tactic.

    This is the goal state before the tactic was applied: {before_state}
    The tactic {tactic} was applied and the goal state changed to: {after_state}
    ''' + '''IMPORTANT: Respond with ONLY a raw JSON object in the following format, without any code block formatting or additional text:
    {
    "Inline Comment": "Comment"
    }
    '''


    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Lean4 expert translating Lean proofs to natural language."},
                {"role": "user", "content": NL_prompt},
            ],
            temperature=0.5,
        )
        reply = response['choices'][0]['message']['content']
        if reply.startswith('```'):
            start = reply.find('{')
            end = reply.rfind('}') + 1
            if start != -1 and end != 0:
                reply = reply[start:end]
        reply_json = json.loads(reply)
        return reply_json.get("Inline Comment")
    except Exception as e:
        return f"An error occurred: {e}"



if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_data = sys.argv[1]

        before_goal_match = re.search(r"Before:\n(.*?⊢.*)", input_data, re.DOTALL)
        before_goal = before_goal_match.group(1).strip() if before_goal_match else "No before goal found"

        after_goal_match = re.search(r"After:\n(.*?⊢.*)", input_data, re.DOTALL)
        after_goal = after_goal_match.group(1).strip() if after_goal_match else "No after goal found"

        tactic_match = re.search(r"Tactic:\s*(.*)", input_data)
        tactic = tactic_match.group(1).strip() if tactic_match else "No tactic provided"

        # print(f"Goal Before Tactic:\n⊢ {before_goal}\n")
        # print(f"User-Provided Tactic:\n{tactic}\n")
        # print(f"Goal After Tactic:\n⊢ {after_goal}\n")
        natural_language = gpt_prompt(str(tactic), str(before_goal), str(after_goal))
        print(f"NL Translation: \n{natural_language}")


    else:
        print("No input received from Lean!")
