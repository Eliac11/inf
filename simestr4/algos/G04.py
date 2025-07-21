from collections import deque


def chess_to_indices(pos):
    column, row = pos
    return ord(column) - ord('a'), int(row) - 1

def is_valid(x, y):
    return 0 <= x < 8 and 0 <= y < 8


def moves(red_pos, green_pos):

    knight_moves = [
        (-2, -1), (-1, -2), (1, -2), (2, -1),
        (2, 1), (1, 2), (-1, 2), (-2, 1)
    ]
    

    red_start = chess_to_indices(red_pos)
    green_start = chess_to_indices(green_pos)
    

    queue = deque([(red_start[0], red_start[1], green_start[0], green_start[1], 0)])
    visited = set([(red_start[0], red_start[1], green_start[0], green_start[1])])
    
    while queue:
        rx, ry, gx, gy, steps = queue.popleft()
        
        if rx == gx and ry == gy:
            return steps
        
        for drx, dry in knight_moves:
            for dgx, dgy in knight_moves:
                nrx, nry = rx + drx, ry + dry
                ngx, ngy = gx + dgx, gy + dgy
                
                if is_valid(nrx, nry) and is_valid(ngx, ngy):
                    state = (nrx, nry, ngx, ngy)
                    if state not in visited:
                        visited.add(state)
                        queue.append((nrx, nry, ngx, ngy, steps + 1))
    
    return -1


k1,k2 = input().split()

print(moves(k1, k2))
