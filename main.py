import pygame
from pytmx.util_pygame import load_pygame
from pygame import mixer
pygame.init()
### source 1 (IMPORTING TMX FILES)###
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect(topleft=pos)
### source 1 (IMPORTING TMX FILES)###

### Settings related ###
Width = 1350
Height = 820
screen = pygame.display.set_mode((Width,Height))
sFont = pygame.font.Font('freesansbold.ttf',20)
bFont = pygame.font.Font('freesansbold.ttf',50)
ENDINGFONT = pygame.font.Font('freesansbold.ttf',200)
timer = pygame.time.Clock()
fps = 60
pygame.display.set_caption("Block Conqueror")
icon = pygame.image.load('Main/Images/sword.png')
pygame.display.set_icon(icon)
tmx_data = load_pygame('/Users/jack/Desktop/Cis 1051 Final proj/TMX/small.tmx')
sprite = pygame.sprite.Group()
### Background Music ###
basic = mixer.music.load('/Users/jack/Desktop/Cis 1051 Final proj/Main/euphoria.mp3')
mixer.music.play(-1)
### Background Music ###


### source 1 (IMPORTING TMX FILES)###
for layer in tmx_data.visible_layers:
	if hasattr(layer,'data'):
		for x,y,surf in layer.tiles():
			pos = (x * 64, y * 64)
			Tile(pos = pos, surf = surf, groups = sprite)
### source 1 (IMPORTING TMX FILES)###
            

playerChar = ['knight','knight','knight']
AI = ['goblin','goblin','goblin',]
PlayerLocations = [(2,2),(1,3),(2,4)]
AILocations = [(4,2),(7,7),(11,4)]
turn_step = 0
selection = 100
moves = []

knight = pygame.image.load('/Users/jack/Desktop/Cis 1051 Final proj/Main/warrior/warriorDE1.png')
goblin = pygame.image.load('/Users/jack/Desktop/Cis 1051 Final proj/Main/Red/flip.png')
playerImages = [knight]
AIImages = [goblin]
piece_list = ['knight','goblin']

###### drawing line and text ######
def Screen(): 
    for i in range(12):
         pygame.draw.line(screen, 'black', (0,64*i),(1280,64*i),1)
    for i in range(20):
         pygame.draw.line(screen, 'black', (64*i,0),(64*i,768),1)
    pygame.draw.rect(screen,'red',[0,720,700,100])
    pygame.draw.rect(screen,'gold',[0,720,700,100],5)
    screen.blit(bFont.render("Level 1: The Great Plains", True, 'black'),(40,750))
    status_text = ['SELECT A PIECE!','MOVE TO LOCATION!',
                   "AI'S TURN","AI'S TURN"]
    screen.blit(bFont.render(status_text[turn_step],True,'white'),(150,70))
    if len(playerChar) == 0:
        screen.blit(ENDINGFONT.render('DEFEATED !!',True,'red'),(0,300))
    if len(AI) == 0:
        screen.blit(ENDINGFONT.render('VICTORY !!',True,'red'),(100,300))

def draw_pieces():
    for i in range(len(playerChar)):
        index = piece_list.index(playerChar[i])
        if playerChar[i] == 'knight':
            screen.blit(knight, (PlayerLocations[i][0] * 64, PlayerLocations[i][1] * 64))
        else:
            screen.blit(playerImages[index], (PlayerLocations[i][0] * 64, PlayerLocations[i][1] * 64))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [PlayerLocations[i][0] * 64 + 1, PlayerLocations[i][1] * 64 + 1,64, 64], 2)
    for i in range(len(AI)):
        index = piece_list.index(AI[i])
        if AI[i] == 'goblin':
            screen.blit(goblin, (AILocations[i][0] * 64, AILocations[i][1] * 64))
        else:
            screen.blit(AIImages[index], (AILocations[i][0] * 64, AILocations[i][1] * 64))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [AILocations[i][0] * 64 + 1, AILocations[i][1] * 64 + 1,64, 64], 2)


def check_options(pieces, locations, turn):
     moves_list = []
     all_moves_list = []
     for i in range((len(pieces))):
         location = locations[i]
         piece = pieces[i]
         if piece == 'knight':
             moves_list = check_knight(location, turn)
         elif piece == 'goblin':
             moves_list = check_goblin(location, turn)
         all_moves_list.append(moves_list)
     return all_moves_list
             


def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = AILocations
        friends = PlayerLocations
    else:
        friends = AILocations
        enemies_list = PlayerLocations
    targets = [(0,1),(0,2),(0,3),(0,-1),(0,-2),(0,-3),(1,0),(2,0),(3,0),(-3,0),(-2,0),(-1,0),(1,2), (1,-2), (2,1), (2,-1), (-1, 2), (-1, -2), (-2, 1), (-2, -1),(1,1),(-1,-1),(1,-1),(-1,1)]
    for i in range(len(targets)):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends and 0 <= target[0] <= 19 and 0 <= target[1] <= 11:
            moves_list.append(target)
    return moves_list

def check_goblin(position,color):
    moves_list = []
    if color == 'white':
        enemies_list = AILocations
        friends = PlayerLocations
    else:
        friends = AILocations
        enemies_list = PlayerLocations
    targets = [(0,1),(0,2),(0,3),(0,-1),(0,-2),(0,-3),(1,0),(2,0),(3,0),(-3,0),(-2,0),(-1,0),(1,2), (1,-2), (2,1), (2,-1), (-1, 2), (-1, -2), (-2, 1), (-2, -1),(1,1),(-1,-1),(1,-1),(-1,1)]
    for i in range(len(targets)):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends and 0 <= target[0] <= 19 and 0 <= target[1] <= 11:
            moves_list.append(target)
    return moves_list


def check_moves():
    if turn_step < 2:
        options_list = player_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

#drawing valid moves
def draw_valid(moves):
    if turn_step<2:
        color = "blue"
    else:
        color = "red"
    for i in range(len(moves)):
        pygame.draw.circle(screen,color,(moves[i][0]*64+32,moves[i][1]*64+32),5)
        pygame.draw.rect(screen,color,[moves[i][0]*64+1,moves[i][1]*64+1,64,64],2)
 
#Game Loop
black_options = check_options(AI,AILocations,'black')
player_options = check_options(playerChar,PlayerLocations,'white')
run = True
while run:
    timer.tick(fps)
    screen.fill("black")
    sprite.draw(screen)
    Screen()
    draw_pieces()
    if selection != 100:
        moves = check_moves()
        draw_valid(moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #and not game_over:
            x_coord = event.pos[0] // 64
            y_coord = event.pos[1] // 64
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in PlayerLocations:
                    selection = PlayerLocations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in moves and selection != 100:
                    PlayerLocations[selection] = click_coords
                    if click_coords in AILocations:
                        AIPiece = AILocations.index(click_coords)
                        AI.pop(AIPiece)
                        AILocations.pop(AIPiece)
                    black_options = check_options(AI, AILocations, 'black')
                    player_options = check_options(playerChar, PlayerLocations, 'white')
                    turn_step = 2
                    selection = 100
                    moves = []
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in AILocations:
                    selection = AILocations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in moves and selection != 100:
                    AILocations[selection] = click_coords
                    if click_coords in PlayerLocations:
                        PlayerPiece = PlayerLocations.index(click_coords)
                        playerChar.pop(PlayerPiece)
                        PlayerLocations.pop(PlayerPiece)
                    black_options = check_options(AI, AILocations, 'black')
                    player_options = check_options(playerChar, PlayerLocations, 'white')
                    turn_step = 0
                    selection = 100
                    moves = []
    pygame.display.flip()
pygame.quit()