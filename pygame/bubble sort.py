from collections import deque
import random

def is_solved(state, k):
    for bottle in state:
        if len(bottle) > 0 and (len(bottle) != k or len(set(bottle)) != 1):
            return False
    return True

def get_possible_moves(state, k):
    moves = []
    for i, src in enumerate(state):
        if not src:
            continue
        color = src[-1]
        # Find the maximum sequence of the same color from the top
        seq_length = 0
        while seq_length < len(src) and src[-(seq_length+1)] == color:
            seq_length += 1
        # Can pour from src to dest
        for j, dest in enumerate(state):
            if i == j:
                continue
            if not dest or (dest[-1] == color and len(dest) + seq_length <= k):
                # Transfer the sequence
                new_state = [list(bottle) for bottle in state]
                transfer = new_state[i][-seq_length:]
                del new_state[i][-seq_length:]
                new_state[j].extend(transfer)
                # Convert to tuples and canonicalize
                new_state = tuple(tuple(bottle) for bottle in new_state)
                moves.append(new_state)
    return moves

def solve(initial_state, k):
    visited = set()
    queue = deque([(initial_state, 0)])
    visited.add(initial_state)
    
    while queue:
        state, steps = queue.popleft()
        if is_solved(state, k):
            return True
        for next_state in get_possible_moves(state, k):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, steps + 1))
    return False

def generate_random_configuration(no_of_colors, extra_bottles, bottle_size):
    # Generate colors (e.g., 'A', 'B', 'C', ...)
    colors = [chr(ord('A') + i) for i in range(no_of_colors)]
    
    # Create a list of all balls (each color appears `bottle_size` times)
    balls = [color for color in colors for _ in range(bottle_size)]
    
    # Shuffle the balls randomly
    random.shuffle(balls)
    
    # Distribute balls into bottles
    bottles = [[] for _ in range(no_of_colors)]
    
    # Assign balls to bottles
    for ball in balls:
        # Find a bottle that isn't full
        bottle = random.choice([b for b in bottles if len(b) < bottle_size])
        bottle.append(ball)
    for _ in range(extra_bottles): bottles.append([]) 
    
    # Convert to tuples (immutable for hashing)
    state = tuple(tuple(bottle) for bottle in bottles)
    
    return state

def apply_move(state, src, dest, k):
    # Check if the move is valid
    if src < 0 or src >= len(state) or dest < 0 or dest >= len(state):
        print("Invalid bottle index.")
        return state
    if not state[src]:
        print("Source bottle is empty.")
        return state
    if len(state[dest]) >= k:
        print("Destination bottle is full.")
        return state
    if state[dest] and state[src][-1] != state[dest][-1]:
        print("Colors do not match.")
        return state
    
    # Perform the move
    new_state = [list(bottle) for bottle in state]
    color = new_state[src][-1]
    # Transfer the maximum sequence of the same color
    seq_length = 0
    while seq_length < len(new_state[src]) and new_state[src][-(seq_length+1)] == color:
        seq_length += 1
    # Ensure the destination has enough space
    if len(new_state[dest]) + seq_length > k:
        print("Not enough space in the destination bottle.")
        return state
    # Transfer the sequence
    transfer = new_state[src][-seq_length:]
    del new_state[src][-seq_length:]
    new_state[dest].extend(transfer)
    # Convert back to tuples
    return tuple(tuple(bottle) for bottle in new_state)

def draw(state):
    # ANSI color codes for some common colors
    colors = {
        'A': '\033[91m███\033[0m',  # Red
        'B': '\033[92m███\033[0m',  # Green
        'C': '\033[94m███\033[0m',  # Blue
        'D': '\033[93m███\033[0m',  # Yellow
        'E': '\033[96m███\033[0m',  # Cyan
        'F': '\033[95m███\033[0m',  # Magenta
        'G': '\033[90m███\033[0m',  # Gray (for 'A')
        'H': '\033[97m███\033[0m',  # White (for 'D')
    }
    
    # Find the maximum height of the bottles
    max_height = max(len(bottle) for bottle in state)
    
    # Draw from top to bottom
    for i in range(max_height - 1, -1, -1):
        row = []
        for bottle in state:
            if i < len(bottle):
                color = bottle[i]
                row.append(colors.get(color, '█'))  # Use default block if color not found
            else:
                row.append('\033[97m███\033[0m')  # Empty space for bottles shorter than max height
        print('   '.join(row))
    
    # Print bottle indices
    print('     '.join(f'{i}' for i in range(len(state))))

# Generate a solvable random configuration
capacity = 4  # Capacity per bottle
no_of_colors = 3
extra_bottles = 1
state = generate_random_configuration(no_of_colors, extra_bottles, capacity)
while not solve(state, capacity):
    state = generate_random_configuration(no_of_colors, extra_bottles, capacity)

states_history = [state]

def undo_move(state):
    if len(states_history) == 1:
        print("No moves to undo.")
        return state
    if len(states_history) != 1: states_history.pop()
    state = states_history[-1]
    return state

def reset_state():
    global states_history
    states_history = states_history[:1]
    return states_history[0]

# Game loop
while not is_solved(state, capacity):
    # Display the current state
    print("\nCurrent State:")
    draw(state)
    
    # Get player input
    move = None
    try:
        move = input(
            '''Enter your move (source destination)
(z to undo)
(0 to reset)
(q to quit)
: ''')
    except KeyboardInterrupt:
        print('Bye')
        exit()
    if move == 'z':
        state = undo_move(state)
    elif move == 'r':
        state = reset_state()
    elif move == 'q':
        print('Bye')
        exit()
    try:
        src = int(move[0])
        dest = int(move[1])
        new_state = apply_move(state, src, dest, capacity)
        if new_state != state:
            states_history.append(state)
            state = new_state
    except ValueError:
        print("Invalid input. Please enter two numbers without separation eg:23") 

# Win message
print("\nCongratulations! You solved the puzzle!")
