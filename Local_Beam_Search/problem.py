import random
import matplotlib.pyplot as plt
from PIL import Image as PILImage

class Problem:
    def __init__(self):
        self.goal = None

    def get_state(self): pass

    def get_pos_actions(self): pass

    def action(self, actions): pass

    def cost(self): pass
    
class Eight_puzzle(Problem):
    def __init__(self, img, empty_pos):
        Problem.__init__(self)
        self.w = 3
        self.h = 3
        self.tiles = []
        
        img_w, img_h = img.size
        self.tile_w = img_w / self.w
        self.tile_h = img_h / self.h
        
        for i in range(0, self.w):
            row = []
            for j in range(0, self.h):
                if (i, j) == empty_pos:
                    row.append({
                        'img': None,
                        'true_pos': (i, j)
                    })
                else:
                    box = (j * self.tile_w, i * self.tile_h,\
                            (j + 1) * self.tile_w, (i + 1) * self.tile_h)
                    row.append({
                        'img': img.crop(box),
                        'true_pos': (i, j)
                    })
            self.tiles.append(row)

        self.goal = self.get_state()
    
    def get_state(self):
        Problem.get_state(self)
        rows = []
        cur_row = []
        for row in self.tiles:
            cur_row = []
            for tile in row:
                cur_row.append((*tile['true_pos'], tile['img'] is None))
            rows.append(tuple(cur_row))
        return tuple(rows)
    
    def get_pos_actions(self):
        Problem.get_pos_actions(self)
        actions = []
        pos = self.get_empty_tile_pos()
        
        x, y = pos
        
        if x < self.w - 1:
            actions.append('right')
        if x > 0:
            actions.append('left')
        if y < self.h - 1:
            actions.append('down')
        if y > 0:
            actions.append('up')
        
        return actions
    
    def action(self, actions):
        Problem.action(self, actions)
        for action in actions:
            if action not in self.get_pos_actions():
                continue
            
            x, y = self.get_empty_tile_pos()
            x2, y2 = x, y
            match action:
                case 'left':
                    x2 -= 1
                case 'right':
                    x2 += 1
                case 'up':
                    y2 -= 1
                case 'down':
                    y2 += 1
            
            self.__swap((x, y), (x2, y2))
            
    def cost(self, action):
        Problem.cost(self, action)
        return 1
    
    def get_empty_tile_pos(self):
        for i, row in enumerate(self.get_state()):
            for j, tile_state in enumerate(row):
                if tile_state[2]:
                    return j, i
    
    def __swap(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        t = self.tiles[y1][x1]
        self.tiles[y1][x1] = self.tiles[y2][x2]
        self.tiles[y2][x2] = t
        
    def shuffle(self, n):
        actions = [random.choice(self.get_pos_actions()) for x in range(0, n)]
        self.action(actions)
        
    def show(self):
        output = ''
        for row in self.get_state():
            output += str(row) + '\n'
        return output
    
    def show_imgs(self, figsize):
        fig = plt.figure(figsize=figsize)
        
        i = 1
        for row in self.tiles:
            for tile in row:
                fig.add_subplot(len(self.tiles), len(self.tiles[0]), i)
                tile_img = tile['img'] if tile['img']\
                    else PILImage.new('RGB', (300, 300))
                t = plt.imshow(tile_img)
                i += 1

        return fig