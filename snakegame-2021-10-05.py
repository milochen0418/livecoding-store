# Live Coding for Snake Game on VT
# The Live Coding is save here
# https://www.facebook.com/groups/developer.taiwan/posts/411380293726221/  

import random
async def init_vt_program(program_func, keyboardUrl):
    snakeVT = VirtualTerminal()
    keyboardImpl = InkeyImpl(snakeVT.getKeyboardQueue())
    VtJupyterAdapter(snakeVT, manual_refresh = True).startVtProgram(program_func)
    await keyboardImpl.runRecvKeyService("RecvFromWeb", keyboardUrl)

def get_new_head(game_logic):
    direction = game_logic['direction'] # Four directions-> L:left, R:right, U:up, D:down 
    cols = game_logic['cols']
    rows = game_logic['rows']
    snake = game_logic['snake']
    head = snake[0]
    new_head = None
    if direction == 'L':
        new_head = [head[0], (head[1] -1) % cols]
    elif direction == 'R':
        new_head = [head[0], (head[1] + 1) % cols]
    elif direction == 'D':
        new_head = [ (head[0] + 1) % rows, head[1]]
    elif direction == 'U':
        new_head = [ (head[0] - 1) % rows, head[1]] 
    return new_head
def is_hitting(A, B):
    if A[0] == B[0] and A[1] == B[1]:
        return True
    else:
        return False
def make_new_food(game_logic):
    rows = game_logic['rows']
    cols = game_logic['cols']
    snake = game_logic['snake']
    candidate = [random.randint(0, rows - 1), random.randint(0, cols - 1)] # food candidate
    while True:
        is_candidate_ok = True
        for i in range(len(snake)):
            body = snake[i]
            if is_hitting(body, candidate):
                is_candidate_ok = False
                break
        if is_candidate_ok == True:
            break
    game_logic['food'] = candidate      
def game_logic_change(v:VirtualTerminal, game_logic):
    snake = game_logic['snake']
    cols = game_logic['cols']
    rows = game_logic['rows']
    food = game_logic['food']
    head = snake[0]    
    new_head = get_new_head(game_logic) # Get new head by currnet direction of snake
    snake.insert(0, new_head)
    if is_hitting(new_head, food):
        make_new_food(game_logic)
        game_logic['score'] += 1
    else:
        del snake[-1]
    # Check game over of snake head is hitting body
    for i in range(1, len(snake)):
        if is_hitting(snake[0], snake[i]):
            game_logic['gameover'] = True
def game_logic_draw(v:VirtualTerminal, game_logic):
    snake = game_logic['snake']
    food = game_logic['food']
    
    # draw snake head
    head = snake[0]
    v.locate(head[0], head[1])
    v.print('█')

    # draw snake body
    for i in range(1, len(snake)):
        body = snake[i]
        v.locate(body[0], body[1])
        v.print('▓')
    # draw food 
    v.locate(food[0], food[1])
    v.print('●')
    # draw score
    v.locate(0,0)
    v.print('Score分數:' + str(game_logic['score']))
    if game_logic['gameover'] == True:
        v.locate(10, 15)
        v.print('==== GAME OVER ====')
    v.flush()
def snake_game_program(v:VirtualTerminal):
    key_left: int = 37
    key_up: int = 38
    key_right: int = 39
    key_down: int = 40 
    key_c: int = 67
    key_x: int = 88
    rows, cols = v.size()
    food = [3, 20] 
    snake = [ [3, 6], [3, 5], [3, 4], [3, 3]] # snake[0] is snake's head
    
    # define game logic for this snake game 
    game_logic = dict() 
    game_logic['rows'] = rows # number of rows in this game
    game_logic['cols'] = cols # number of cols in this game
    game_logic['food'] = food # food location 
    game_logic['score'] = 0 #initial score is zero. 
    game_logic['snake'] = snake # snake body is seuqnece of locations and let first element to be head of snake
    game_logic['direction'] = 'R' # Four directions-> L:left, R:right, U:up, D:down 
    game_logic['gameover'] = False # show status is game over or not
    
    v.clear()
    game_logic_draw(v, game_logic) # draw according to the game_logic
    while True:
        v.delay(0.1)
        v.clear()
        game_logic_change(v, game_logic)
        game_logic_draw(v, game_logic)
        if game_logic['gameover'] == True:
            break
        # Processing keyboard event (Like INKEY$ in Qbasic )
        key = v.inkey()
        if key == key_up and game_logic['direction'] != 'D':
            game_logic['direction'] = 'U'
        elif key == key_down and game_logic['direction'] != 'U':
            game_logic['direction'] = 'D'
        elif key == key_right and game_logic['direction'] != 'L':
            game_logic['direction'] = 'R'
        elif key == key_left and game_logic['direction'] != 'R':
            game_logic['direction'] = 'L'
await init_vt_program(snake_game_program, "https://keyboard.covidicq.net")
