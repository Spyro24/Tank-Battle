#(c) 2025 Spyro24
import random
import pygame as p
import time

class tank:
    def __init__(self, bound, AI=True, ID=1):
        self.ai_player   = AI
        self.pos_x       = 0
        self.pos_y       = 0
        self.max_pos_x   = bound[0]
        self.max_pos_y   = bound[1]
        self.tokens      = 0
        self.lives       = 3
        self.shoot_range = 2
        self.ai_balance  = [0, 100]
        self.player_name = "Bot"
        self.sound_table = None
        if not AI:
            self.player_name = "Player " + str(ID)
    
    def add_env(self, window, zero_pos, sprite, tile_size, player_list):
        self.window    = window
        self.null      = zero_pos
        self.tile_size = tile_size
        self.sprite    = p.transform.scale(sprite, (tile_size, tile_size))
        self.players   = player_list
    
    def init(self):
        self.pos_x = random.randint(0, self.max_pos_x - 1)
        self.pos_y = random.randint(0, self.max_pos_y - 1)
        if self.ai_player:
            for n in range(5):
                self.ai_balance.insert(-1, random.randint(self.ai_balance[-2], self.ai_balance[-1]))
            print(self.ai_balance)
        
    def ai_round(self):
        if self.player_is_alive():
            if self.tokens > 0:
                void = random.randint(0, 100)
                if self.ai_balance[0] <= void < self.ai_balance[1]: #move
                    self.move()
                elif self.ai_balance[1] <= void < self.ai_balance[2]: #shoot
                    self.shoot()
                elif self.ai_balance[5] <= void <= self.ai_balance[6]: #wait
                    return True
                return False
            else: return True #end round because the AI has no tokens
    
    def move(self):
        moved = False
        if self.ai_player:
            while not moved:
                choice = random.randint(0,4)
                if choice < 3:
                    move_x = random.randint(-1, 1)
                    move_y = random.randint(-1, 1)
                else:
                    choice = random.randint(0, len(self.players) - 1)
                    if self.players[choice] is not self and self.players[choice].player_is_alive():
                        goto = self.players[choice].get_pos()
                        x_move = 0
                        y_move = 0
                        if goto[0] < self.pos_x:
                            x_move = -1
                        elif goto[0] > self.pos_x:
                            x_move = 1
                        if goto[1] < self.pos_y:
                            y_move = -1
                        elif goto[1] > self.pos_y:
                            y_move = 1
                        if self.action_move((x_move, y_move)):
                            self.tokens -= 1
                            moved = True
                    break
                if 0 <= (move_x + self.pos_x) < self.max_pos_x:
                    if 0 <= (move_y + self.pos_y) < self.max_pos_y:
                        can_move = True
                        for user in self.players:
                            if user.get_pos() == (self.pos_x + move_x, self.pos_y + move_y):
                                can_move = False
                        if can_move:
                            self.pos_x += move_x
                            self.pos_y += move_y
                            self.tokens -= 1
                            moved = True
    
    def action_move(self, dir_): #Player action
        if 0 <= (dir_[0] + self.pos_x) < self.max_pos_x:
            if 0 <= (dir_[1]+ self.pos_y) < self.max_pos_y:
                can_move = True
                for user in self.players:
                    if user.get_pos() == (self.pos_x + dir_[0], self.pos_y + dir_[1]):
                        can_move = False
                if can_move:
                    self.pos_x += dir_[0]
                    self.pos_y += dir_[1]
                    self.tokens -= 1
                    return True
        return False
        
    def shoot(self):
        t_pos_x = self.pos_x
        t_pos_y = self.pos_y
        for player in self.players:
            if not (player is self):
                m_pos_x, m_pos_y = player.get_pos()
                check   = []
                if t_pos_x > m_pos_x:
                    check.append(t_pos_x); check.append(m_pos_x)
                else:
                    check.append(m_pos_x); check.append(t_pos_x)
                if t_pos_y > m_pos_y:
                    check.append(t_pos_y); check.append(m_pos_y)
                else:
                    check.append(m_pos_y); check.append(t_pos_y)
                if check[0] - check[1] <= self.shoot_range:
                    if check[2] - check[3] <= self.shoot_range:
                        draw_pos_enem = player.get_pos()
                        p.draw.line(self.window, (255,0,127), (self.pos_x * self.tile_size + (self.tile_size / 2) + self.null[0], self.pos_y * self.tile_size + (self.tile_size / 2) + self.null[1]), (draw_pos_enem[0] * self.tile_size + (self.tile_size / 2) + self.null[0], draw_pos_enem[1] * self.tile_size + (self.tile_size / 2) + self.null[1]), int(self.tile_size / 8))
                        p.display.flip()
                        self.sound_table[1].play()
                        time.sleep(0.05)
                        player.lives -= 1
                        if player.lives == 0:
                            self.sound_table[0].play()
                        self.tokens -= 1
                        return True
    
    def action_shoot(self, pos):
        t_pos_x = self.pos_x
        t_pos_y = self.pos_y
        m_pos_x = pos[0]
        m_pos_y = pos[1]
        check   = []
        if t_pos_x > m_pos_x:
            check.append(t_pos_x); check.append(m_pos_x)
        else:
            check.append(m_pos_x); check.append(t_pos_x)
        if t_pos_y > m_pos_y:
            check.append(t_pos_y); check.append(m_pos_y)
        else:
            check.append(m_pos_y); check.append(t_pos_y)
        if check[0] - check[1] <= self.shoot_range:
            if check[2] - check[3] <= self.shoot_range:
                for player in self.players:
                    if not (player is self):
                        if player.get_pos() == pos:
                            self.tokens -= 1
                            draw_pos_enem = player.get_pos()
                            p.draw.line(self.window, (255,0,0), (self.pos_x * self.tile_size + (self.tile_size / 2) + self.null[0], self.pos_y * self.tile_size + (self.tile_size / 2) + self.null[1]), (draw_pos_enem[0] * self.tile_size + (self.tile_size / 2) + self.null[0], draw_pos_enem[1] * self.tile_size + (self.tile_size / 2) + self.null[1]), int(self.tile_size / 8))
                            p.display.flip()
                            self.sound_table[1].play()
                            time.sleep(0.05)
                            player.lives -= 1
                            if player.lives == 0:
                                self.sound_table[0].play()
                            return True
        return False
    
    def player_is_alive(self):
        if self.lives > 0:
            return True
        else:
            return False
        
    def add_token(self):
        self.tokens += 1
    
    def get_pos(self):
        if self.player_is_alive():
            return (self.pos_x, self.pos_y)
        else:
            return (-1, -1)
    
    def draw_to_screen(self):
        if self.player_is_alive():
            self.window.blit(self.sprite, (self.pos_x * self.tile_size + self.null[0], self.pos_y * self.tile_size + self.null[1]))
            
    def highlight(self, sprite):
        self.window.blit(p.transform.scale(sprite, (self.tile_size, self.tile_size)), (self.pos_x * self.tile_size + self.null[0], self.pos_y * self.tile_size + self.null[1]))
        
    def get_stats(self):
        return (self.lives, self.tokens, self.player_name)
    
def key_input(window, font, tilesize, hint):
    key_table = { 97:"A",  98:"B",  99:"C", 100:"D", 101:"E", 102:"F", 103:"G", 104:"H", 105:"I", 106:"J",
                 107:"K", 108:"L", 109:"M", 110:"N", 111:"O", 112:"P", 113:"Q", 114:"R", 115:"S", 116:"T",
                 117:"U", 118:"V", 119:"W", 120:"X", 121:"Y", 122:"Z",  48:"0",  49:"1",  50:"2",  51:"3",
                  52:"4",  53:"5",  54:"6",  55:"7",  56:"8",  57:"9"}
    return_string = ""
    k_hold  = False
    update = True
    window = window
    mid_point = window.get_rect().center
    r_size_x = mid_point[0] * 1.5
    r_size_y = mid_point[1] * 1.5
    r_zero_x = mid_point[0] / 4
    r_zero_y = mid_point[1] / 4
    while True:
        p.event.get()
        k_count = 0
        keys    = p.key.get_pressed()
        if keys[13]:
            break
        elif keys[8]:
            k_count += 1
            if not k_hold:
                k_hold = True
                try:
                    return_string = return_string.removesuffix(return_string[-1])
                    update = True
                except:
                    pass
        for n in range(len(keys)):
            if keys[n]:
                k_count += 1
                if not k_hold:
                    k_hold = True
                    try:
                        if len(return_string) <= 0:
                            return_string += key_table[n]
                        else:
                            return_string += key_table[n].lower()
                        update = True
                    except KeyError:
                        pass
                    print(n)
        if update:
            p.draw.rect(window, (127,127,255), (r_zero_x, r_zero_y, r_size_x, r_size_y))
            font.draw(hint, tilesize, (tilesize + r_zero_x, tilesize + r_zero_y))
            font.draw(return_string, tilesize, (tilesize + r_zero_x, tilesize * 4 + r_zero_y))
            p.display.flip()
            update = False
        if k_count == 0:
            k_hold = False
    return return_string

#tw = p.display.set_mode((500,500))
#print(key_input(tw, None, None, None))
        