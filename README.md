<p align="center">
  <img src="https://github.com/dhhruv/Chrome-Dino-Runner/blob/master/assets/DinoWallpaper.png" width="97" height="97">
  <h2 align="center" style="margin-top: -4px !important;">Campeonato de Dino com ChatGPT 😂😂</h2>
</p>

### Introdução:

-	O Dinosaur Game, também conhecido como **T-Rex Game, Steve the Jumping Dinosaur ou Dino Runner** e inicialmente codinome Project Bolan, é um jogo de navegador integrado no **Google Chrome Web Browser**. O jogo foi criado por **Sebastien Gabriel em 2014** e pode ser acessado pressionando a barra de espaço no modo offline no Google Chrome.

### Sobre:

-	A seguir, representamos uma versão recriada para LLM jogar do famoso Dinosaur Game no modo off-line do navegador Chrome, implementado usando **Python e PyGame**. A adaptção foi feita por Dhruv Panchal e pode ser baixada no https://github.com/dhhruv/Chrome-Dino-Runner. O arquivo do projeto contém **Arquivos de imagem** e um script python **(chromedino_V1_GPT4.py)**.
-	Uma GUI simples e fácil de usar é fornecida para uma melhor jogabilidade. O design da jogabilidade é tão simples que o usuário não achará difícil de usar e entender. Diferentes imagens são usadas no desenvolvimento deste projeto de jogo simples, o ambiente de jogo é igual ao jogo Chrome Dino Run original. Para demonstração do projeto, dê uma olhada no GIF abaixo.

<p align="center">
  <img src="https://github.com/dhhruv/Chrome-Dino-Runner/blob/master/assets/Other/Chrome%20Dino.gif">
</p>

### Instalação:

-	Antes de mais nada, **clone o repositorio** com:
```
git clone https://github.com/inteligenciamilgrau/dinossauro_chrome_chatgpt.git
``` 
**OU**
Faça o Download do ZIP e descompacte seu conteudo.

-	Depois instale as dependencias pelo Command Prompt OU Terminal usando:
```
pip install requirements.txt
```

### Jogar:

-	Depois da instalação, configure sua API da OpenAI na pasta ".env", e rode o [`chromedino_V1_GPT4.py`] com
```
python chromedino.py
```

### Importante:

-   A velocidade foi diminuida para dar tempo para a LLM pensar!
-   A variável "jogar" tem o prompt, use ele para melhorar a performance!
-   Você pode observar 3 variaveis:
-   O tipo de inimigo que é Cactus ou Bird
-   A distancia que ele está de você
-   A altura que ele tem

### PS:

-   Agradeço demais Dhruv Panchal que fez essa versão para Python porque todas outras versões que encontrei, nenhuma tinha o pássaro. Ou quando tinha, o Dino não abaixava. Sem falar nas nuvens e no cenário que no geral ou não tinha, ou era bugado!

### References:
-	http://www.pygame.org/docs
-	https://en.wikipedia.org/wiki/Dinosaur_Game
-	Various articles and videos.
