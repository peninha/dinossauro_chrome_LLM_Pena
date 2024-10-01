# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import datetime
import json
import os
import random
import threading
import time
from dotenv import load_dotenv
load_dotenv()
import pygame
from openai import OpenAI
import google.generativeai as genai
import requests
import anthropic

#modelo = "gpt-3.5-turbo-0125"
modelo = "gpt-4o-mini"

#modelo = "gemini-1.0-pro-latest"

#modelo = "llama3"  # ollama
#modelo = "phi3"  # ollama
url_ollama = "http://localhost:11434/api/generate"  # endereco do ollama

#modelo = "claude-3-haiku-20240307"
#modelo = "claude-3-sonnet-20240229"
# modelo = "claude-3-opus-20240229"

dados = {'inimigo': 'indefinido', 'distancia': "indefinida", 'altura': 'indefinida'}
acao = {"acao": "nenhuma"}
jogar = ""
velocidade_do_jogo = 5  # original = 30
inicia_bot = True

def atualiza(dados):
    global sys_prompt
    global jogar
    sys_prompt = """You always must return your answers in a JSON format: 'acao':response
    If enemy is 'bird' and height > 119, say 'abaixar',
    Else If distance plus height/2 is less than 510 and more than 200, say 'pular'.
    Else say 'abaixar'"""
    jogar = f"""enemy = {dados['inimigo']}
                distance = {dados['distancia']}
                height = {dados['altura']}"""
    messages = [
        {"role": "system", "content": sys_prompt},  # System prompt
        {"role": "user", "content": jogar}  # User prompt
        ]
    return messages

pygame.init()

# Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chrome Dino Runner")

Ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)

RUNNING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

FONT_COLOR=(0,0,0)

class Dinosaur:

    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        global acao
        agir = acao["acao"]

        # atualiza imagem
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        # executa comando
        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE] or agir == "pular") and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif (userInput[pygame.K_DOWN] or agir == "abaixar" ) and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        #acao["acao"] = "nenhuma"

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        self.name = "Small Cactus"


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
        self.name = "Large Cactus"


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0
        self.name = "Bird"

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, dados, acao, velocidade_do_jogo
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False

    file_path = "score.txt"

    # Check if the file exists, and create it with default text if it doesn't
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write('0')
    else:
        # If the file exists but is empty, write "0" to it
        with open(file_path, 'r+') as file:
            content = file.read().strip()
            if content == '':
                file.write('0')

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        current_time = datetime.datetime.now().hour

        #file_path = "score.txt"
        if not os.path.isfile(file_path):
            # If the file does not exist, create it with some initial content
            with open(file_path, "w") as f:
                # Write some initial content to the file
                f.write("Initial content if needed\n")
        with open(file_path, "r") as f:
            score_ints = [int(x) for x in f.read().split()]
            #print("score_ints", score_ints)
            if score_ints:
                highscore = max(score_ints)
            else:
                highscore = 0
            #print("SCORE", highscore, points)
            if points > highscore:
                highscore=points 
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    frames = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()

        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            SCREEN.fill((255, 255, 255))
        else:
            SCREEN.fill((0, 0, 0))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        jogar = 2
        for obstacle in obstacles:
            if frames == jogar:
                dados = {"inimigo": obstacle.name, "distancia": obstacle.rect[0], "altura": (SCREEN_HEIGHT - obstacle.rect[1]) - (SCREEN_HEIGHT - (310 + 94))}
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                death_count += 1
                menu(death_count)

        if frames == jogar:
            frames = 0
        else:
            frames += 1

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(velocidade_do_jogo)
        pygame.display.update()


def menu(death_count):
    global points
    global FONT_COLOR
    global run_agent, dados

    last_score = 0

    run = True
    while run:
        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            FONT_COLOR=(0,0,0)
            SCREEN.fill((255, 255, 255))
        else:
            FONT_COLOR=(255,255,255)
            SCREEN.fill((128, 128, 128))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, FONT_COLOR)
        elif death_count > 0:
            dados = {'inimigo': 'indefinido', 'distancia': "indefinida", 'altura': 'indefinida'}
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
            score = font.render("Your Score: " + str(last_score), True, FONT_COLOR)
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            if points > 0:
                f = open("score.txt", "a")
                f.write(str(points) + "\n")
                f.close()
                last_score = points
                points = 0
            with open("score.txt", "r") as f:
                score = (
                    f.read()
                )  # Read all file in case values are not on a single line
                score_ints = [int(x) for x in score.split()]  # Convert strings to ints
            highscore = max(score_ints)  # sum all elements of the list
            hs_score_text = font.render(
                "High Score : " + str(highscore), True, FONT_COLOR
            )
            hs_score_rect = hs_score_text.get_rect()
            hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(hs_score_text, hs_score_rect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                run_agent = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()


if modelo.startswith("gpt"):
    client = OpenAI()
elif modelo.startswith("gemini"):
    print("Listando modelos")
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    client = genai.GenerativeModel(modelo)
elif modelo.startswith("claude"):
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

def generate_answer(messages, model="gpt-3.5-turbo-1106"):
    temperatura = 0.0
    if model.startswith("gpt"):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperatura,
                seed=42,
                response_format={"type": "json_object"},
            )

            return response.choices[0].message.content
        except Exception as e:
            print("Erro GPT", e)
            return e
    elif model.startswith("gemini"):
        try:
            genai.GenerationConfig(response_mime_type="application/json", temperature=temperatura)
            response = client.generate_content(messages)
            return response.text.lower().replace("```", "").replace("json","")
        except Exception as e:
            print("Erro Gemini", e)
            return e
    elif model.startswith("claude"):
        try:
            msg = client.messages.create(

                model=model,
                max_tokens=1000,
                temperature=temperatura,
                #system="Você é um assistente divertido.",
                messages=[
                    {"role": "user", "content": messages}
                ]
            )
            return msg.content[0].dict()['text']
        except Exception as e:
            print("Erro Gemini", e)
            return e
    elif model.startswith("llama") or model.startswith("phi") or model.startswith("gemma"):
        try:
            payload = {
                "model": model,
                "prompt": messages,
                "stream": False,
                "format": "json",
                "temperature": temperatura
            }

            response = requests.post(url_ollama, json=payload)

            return response.json()["response"].lower().replace("â", "a").replace("ç", "c").replace("ã", "a").replace("\n", "")
        except Exception as e:
            print("Erro Ollama", e)
            return e

run_agent = True

def recebe_estados():
    global run_agent, dados, acao, jogar, sys_prompt
    clock = pygame.time.Clock()
    previousAction = ""
    while run_agent:
        messages = atualiza(dados)
        if not dados["inimigo"] == "indefinido":
            print(60 * "#")
            print("delaytime", clock.tick())
            #print("Dados", dados)
            print("distancia", dados['distancia'])
            resposta = generate_answer(messages, model=modelo)
            acao["acao"] = json.loads(resposta)["acao"]
            currentAction = acao['acao']
            if currentAction != previousAction:
                print(f"acao = {currentAction} : {dados['altura']}")
            previousAction = currentAction
            time.sleep(0.2)
        else:
            time.sleep(1)

# inicia o chatgpt
if inicia_bot:
    ai_player = threading.Thread(target=recebe_estados)
    ai_player.start()

t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()


