#(c) 2025 Spyro24

import time
import pygame as p
import tank
import tile_handler
import font
import clickgrid

players    = 1
bots       = 7
end        = False
bound      = (24,16)
window     = p.display.set_mode((1200, 720))
users      = []
sprites    = tile_handler.load_tiles("./sprites.png", {"size":"6x6"}, mode="single")
tile_size  = 32
void       = window.get_rect().centerx
blit_pos   = void - (tile_size * (bound[0] / 2)), 0
ground     = p.Surface((tile_size * bound[0], tile_size * bound[1]))
zero_pos   = window.blit(ground, (blit_pos[0], blit_pos[1])).topleft
font_draw  = font.font(window, "./standard")
field_sel  = clickgrid.ClickGrid(bound, window.blit(ground, (blit_pos[0], blit_pos[1])))
mouse_hold = False
scaleds    = [p.transform.scale(sprites[3], (tile_size * 2, tile_size *2)),
              p.transform.scale(sprites[4], (tile_size * 2, tile_size *2)),
              p.transform.scale(sprites[5], (tile_size * 2, tile_size *2))]
void       = window.get_rect().midbottom
buttons    = []#[window.blit(scaleds[0], (void[0] + (10 * tile_size), void[1] - (6 * tile_size))), window.blit(scaleds[0], (void[0] + (8 * tile_size), void[1] - (6 * tile_size)))]

#init blits
buttons.append(window.blit(scaleds[0], (void[0] + (10 * tile_size), void[1] - (6 * tile_size))))
buttons.append(window.blit(scaleds[1], (void[0] + ( 8 * tile_size), void[1] - (6 * tile_size))))
#shity class
class globvar:
    def __init__(self):
        self.mouse_hold = False
globva = globvar()

#create the playground
for x in range(bound[0]):
    for y in range(bound[1]):
        ground.blit(p.transform.scale(sprites[1], (tile_size, tile_size)),(x * tile_size, y*tile_size))

#init the AI Players
for n in range(bots):
    users.append(tank.tank(bound))
    users[-1].add_env(window, zero_pos, sprites[0], tile_size, users)
    users[-1].init()

#init the Players
for n in range(players):
    users.append(tank.tank(bound, AI=False, ID=n+1))
    users[-1].add_env(window, zero_pos, sprites[6], tile_size, users)
    users[-1].init()
    users[-1].player_name = tank.key_input(window, font_draw, tile_size, "Enter player name for " + str(users[-1].player_name))

#functions
def update_screen():
    window.blit(ground, (blit_pos[0], blit_pos[1]))
    for user in users:
        user.draw_to_screen()
    p.display.flip()

def human_player(player):
    void = window.get_rect().midbottom
    draw_zero = void[0] - (tile_size * (bound[0] / 2)), void[1] - (6 *tile_size)
    player_stats = player.get_stats()
    win_update = True
    font_size = tile_size / 1.5
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
   
        m_pos   = p.mouse.get_pos()
        m_click = p.mouse.get_pressed()
    
        if m_click[0]:
            if not globva.mouse_hold:
                globva.mouse_hold = True
                if field_sel.activate_rect.collidepoint(m_pos):
                    x_move     = 0
                    y_move     = 0
                    click_pos  = field_sel.get_click(m_pos)
                    player_pos = player.get_pos()
                    if not click_pos == player_pos:
                        if click_pos[0] < player_pos[0]:
                            x_move = -1
                        elif click_pos[0] > player_pos[0]:
                            x_move = 1
                        if click_pos[1] < player_pos[1]:
                            y_move = -1
                        elif click_pos[1] > player_pos[1]:
                            y_move = 1
                        player.action_move((x_move, y_move))
                    break
                elif buttons[0].collidepoint(m_pos):
                    return 0
                elif buttons[1].collidepoint(m_pos):
                    window.blit(scaleds[2], (void[0] + ( 8 * tile_size), void[1] - (6 * tile_size)))
                    p.display.flip()
                    while True:
                        p.event.get()
                        m_pos   = p.mouse.get_pos()
                        m_click = p.mouse.get_pressed()
                        if m_click[0]:
                            if not globva.mouse_hold:
                                globva.mouse_hold = True
                                if field_sel.activate_rect.collidepoint(m_pos):
                                    click_pos  = field_sel.get_click(m_pos)
                                    shooted = player.action_shoot(click_pos)
                                elif buttons[1].collidepoint(m_pos):
                                    update = True
                                    break
                                if shooted == True:
                                    break
                        else:
                            globva.mouse_hold = False
                    break
        else:
            globva.mouse_hold = False
        
        if win_update:
            window.fill((0, 0, 0))
            window.blit(scaleds[0], (void[0] + (10 * tile_size), void[1] - (6 * tile_size)))
            window.blit(scaleds[1], (void[0] + ( 8 * tile_size), void[1] - (6 * tile_size)))
            font_draw.draw("Lives:" + str(player_stats[0]), font_size, draw_zero)
            font_draw.draw("Tokens:" + str(player_stats[1]), font_size, (draw_zero[0], draw_zero[1] + tile_size))
            font_draw.draw("Player:" + str(player_stats[2]), font_size, (draw_zero[0], draw_zero[1] + (tile_size * 2)))
            update_screen()
            player.highlight(sprites[7])
            p.display.flip()
            win_update = False

#start game
update = True
while not end:
    for user in users:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                end = True
            
        window.fill((0, 0, 0))
        user.add_token()
        aip = user.ai_player
        if not user.player_is_alive():
            continue 
        if aip:
            while True:
                round_fin = user.ai_round()
                update_screen()
                if round_fin:
                    time.sleep(0.05)
                    break
        else:
            while True:
                if user.tokens < 1:
                    break
                action = human_player(user)
                if action == 0: 
                    break
    
    alives = 0
    for user in users:
        if user.player_is_alive():
            alives += 1
    if alives == 1:
        for user in users:
            if user.player_is_alive():
                print(user.get_stats())
                exit(0)

