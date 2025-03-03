from collections import deque

# Define the possible moves
def possible_moves(state):
    M, C, B = state
    moves = []
    
    # Boat on the left bank (B=0)
    if B == 0:
        # Two missionaries cross
        if M >= 2:
            moves.append((M-2, C, 1))
        # Two cannibals cross
        if C >= 2:
            moves.append((M, C-2, 1))
        # One missionary and one cannibal cross
        if M >= 1 and C >= 1:
            moves.append((M-1, C-1, 1))
        # One missionary crosses
        if M >= 1:
            moves.append((M-1, C, 1))
        # One cannibal crosses
        if C >= 1:
            moves.append((M, C-1, 1))
    else:
        # Boat on the right bank (B=1)
        # Two missionaries cross back
        if M < 3:
            moves.append((M+2, C, 0))
        # Two cannibals cross back
        if C < 3:
            moves.append((M, C+2, 0))
        # One missionary and one cannibal cross back
        if M < 3 and C < 3:
            moves.append((M+1, C+1, 0))
        # One missionary crosses back
        if M < 3:
            moves.append((M+1, C, 0))
        # One cannibal crosses back
        if C < 3:
            moves.append((M, C+1, 0))
    
    return moves

# Check if a state is valid
def is_valid_state(state):
    M, C, B = state
    # Missionaries must never be outnumbered by cannibals on either bank
    if M < C and M > 0:
        return False
    if M > 3 or C > 3 or M < 0 or C < 0:
        return False
    return True

# Check if a state is the goal state
def is_goal_state(state):
    return state == (0, 0, 1)

# BFS Implementation (Breadth-First Search)
def bfs(initial_state):
    queue = deque([(initial_state, [])])  # (state, path)
    visited = set()

    while queue:
        state, path = queue.popleft()
        if state in visited:
            continue
        visited.add(state)

        if is_goal_state(state):
            return path + [state]

        for move in possible_moves(state):
            if is_valid_state(move) and move not in visited:
                queue.append((move, path + [state]))

    return None

# DFS Implementation (Depth-First Search with limited depth)
def dfs(initial_state, limit):
    stack = [(initial_state, [], 0)]  # (state, path, depth)
    visited = set()

    while stack:
        state, path, depth = stack.pop()
        if state in visited:
            continue
        visited.add(state)

        if is_goal_state(state):
            return path + [state]

        if depth < limit:
            for move in possible_moves(state):
                if is_valid_state(move) and move not in visited:
                    stack.append((move, path + [state], depth + 1))

    return None

# Iterative Deepening Implementation (combines DFS with increasing depth)
def iterative_deepening(initial_state):
    depth = 0
    while True:
        result = dfs(initial_state, depth)
        if result is not None:
            return result
        depth += 1

# Convert state to a human-readable string
def state_to_str(state):
    M, C, B = state
    bank = "Left" if B == 0 else "Right"
    return f"Missionaries: {M}, Cannibals: {C}, Boat: {bank}"

# Display the solution path in a simple format
def display_solution(path):
    if path:
        print("Solution found:")
        for step in path:
            print(state_to_str(step))
    else:
        print("No solution found.")

# Main function to run all three strategies
def run_all_strategies():
    print("Choose the algorithm to use:")
    print("1. BFS (Breadth-First Search)")
    print("2. DFS (Depth-First Search)")
    print("3. Iterative Deepening")
    
    choice = input("Enter the number corresponding to the algorithm: ")

    # Prompt for the number of missionaries and cannibals
    missionaries = int(input("Enter the number of missionaries: "))
    cannibals = int(input("Enter the number of cannibals: "))

    initial_state = (missionaries, cannibals, 0)

    if choice == '1':
        print("\nRunning BFS...")
        bfs_result = bfs(initial_state)
        display_solution(bfs_result)
    
    elif choice == '2':
        print("\nRunning DFS with a depth limit of 10...")
        dfs_result = dfs(initial_state, 10)
        display_solution(dfs_result)
    
    elif choice == '3':
        print("\nRunning Iterative Deepening...")
        iterative_result = iterative_deepening(initial_state)
        display_solution(iterative_result)
    
    else:
        print("Invalid choice. Please enter a valid number.")

# Run the strategies with user input
run_all_strategies()
