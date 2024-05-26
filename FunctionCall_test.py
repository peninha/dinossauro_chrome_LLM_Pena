import json
from openai import OpenAI

model = "gpt-4o"
temperatura = 0.0
dados = {
    'inimigo': 'small cactus', 
    'distancia': "465", 
    'altura': '95'}

sys_prompt = """relay the parameters"""
jogar = f"""enemy = {dados['inimigo']}
            distance = {dados['distancia']}
            height = {dados['altura']}"""
messages = [
    {"role": "system", "content": sys_prompt},  # System prompt
    {"role": "user", "content": jogar}  # User prompt
    ]

tools = [
    {
        "type": "function",
        "function": {
            "name": "chooseAction",
            "description": "decides which action to take",
            "parameters": {
                "type": "object",
                "properties": {
                    "enemy": {
                        "type": "string",
                        "description": "the enemy name"
                    },
                    "distance": {
                        "type": "integer",
                        "description": "the enemy distance"
                    },
                    "height": {
                        "type": "integer",
                        "description": "the enemy height"
                    }
                },
                "required": ["enemy", "distance", "height"]
            }
        }
    }
]

tool_choice = {"type": "function", "function": {"name": "chooseAction"}}

client = OpenAI()

def pularCalc(distancia, altura):
    if isinstance(distancia, int) and isinstance(altura, int):
        return distancia + altura / 2
    return False

def chooseAction(enemy, distance, height):
    if enemy == 'indefinido':
        return False
    if enemy == 'bird' and height > 119:
        return 'abaixar'
    elif pularCalc(distance, height) <= 460:
        return 'pular'
    return 'abaixar'

def generate_answer(messages, model="gpt-3.5-turbo-1106"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperatura,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response.choices[0].message
    except Exception as e:
        print("Erro GPT", e)
        return e
    
    
response = generate_answer(messages, model)
print(response)
tool_calls = response.tool_calls
tool_call_id = tool_calls[0].id
tool_function_name = tool_calls[0].function.name
enemy = eval(tool_calls[0].function.arguments)['enemy']
distance = eval(tool_calls[0].function.arguments)['distance']
height = eval(tool_calls[0].function.arguments)['height']

