from collections import deque
import heapq
import copy
import time

def find_zero(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                return (i, j)

def get_neighbors(state):
    neighbors = []
    x, y = find_zero(state)
    moves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    
    for new_x, new_y in moves:
        if 0 <= new_x < len(state) and 0 <= new_y < len(state[0]):
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            neighbors.append(new_state)
    
    return neighbors

def generate_goal_state(size):
    return [[(i * size + j + 1) % (size * size) for j in range(size)] for i in range(size)]

def heuristic_misplaced_tiles(state, goal_state):
    return sum(1 for i in range(len(state)) for j in range(len(state[i])) if state[i][j] != goal_state[i][j] and state[i][j] != 0)

def heuristic_manhattan_distance(state, goal_state):
    size = len(state)
    distance = 0
    for i in range(size):
        for j in range(size):
            value = state[i][j]
            if value != 0:
                goal_x, goal_y = divmod(value - 1, size)
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

def bfs(initial_state):
    size = len(initial_state)
    goal_state = generate_goal_state(size)
    queue = deque([(initial_state, [], 0)])  # (current state, path, cost)
    visited = set()
    max_memory = 0
    
    while queue:
        max_memory = max(max_memory, len(queue))
        state, path, cost = queue.popleft()
        
        if state == goal_state:
            return path + [state], cost, max_memory
        
        state_tuple = tuple(map(tuple, state))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        
        for neighbor in get_neighbors(state):
            queue.append((neighbor, path + [state], cost + 1))
    
    return None, None, max_memory

def greedy_search(initial_state):
    size = len(initial_state)
    goal_state = generate_goal_state(size)
    priority_queue = [(heuristic_misplaced_tiles(initial_state, goal_state), initial_state, [], 0)]
    visited = set()
    max_memory = 0
    
    while priority_queue:
        max_memory = max(max_memory, len(priority_queue))
        _, state, path, cost = heapq.heappop(priority_queue)
        
        if state == goal_state:
            return path + [state], cost, max_memory
        
        state_tuple = tuple(map(tuple, state))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        
        for neighbor in get_neighbors(state):
            heapq.heappush(priority_queue, (heuristic_misplaced_tiles(neighbor, goal_state), neighbor, path + [state], cost + 1))
    
    return None, None, max_memory

def a_star(initial_state):
    size = len(initial_state)
    goal_state = generate_goal_state(size)
    priority_queue = [(heuristic_manhattan_distance(initial_state, goal_state), 0, initial_state, [], 0)]
    visited = set()
    max_memory = 0
    
    while priority_queue:
        max_memory = max(max_memory, len(priority_queue))
        _, g, state, path, cost = heapq.heappop(priority_queue)
        
        if state == goal_state:
            return path + [state], cost, max_memory
        
        state_tuple = tuple(map(tuple, state))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        
        for neighbor in get_neighbors(state):
            new_g = g + 1
            f = new_g + heuristic_manhattan_distance(neighbor, goal_state)
            heapq.heappush(priority_queue, (f, new_g, neighbor, path + [state], cost + 1))
    
    return None, None, max_memory

def main():
    size = int(input("Enter puzzle size (3 for 3x3, 4 for 4x4): "))
    initial_state = []
    print(f"Enter the {size}x{size} initial state row by row, using spaces between numbers:")
    for _ in range(size):
        initial_state.append(list(map(int, input().split())))
    
    algorithms = {"BFS": bfs, "Greedy Search (H1)": greedy_search, "A* (H2)": a_star}
    results = []
    
    for name, algorithm in algorithms.items():
        print(f"\nRunning {name}...")
        start_time = time.time()
        solution, cost, memory = algorithm(initial_state)
        end_time = time.time()
        
        if solution:
            results.append((name, cost, end_time - start_time, memory))
        else:
            results.append((name, "No solution", "-", "-"))
    
    print("\nSummary of Results:")
    print("Method | Cost | Execution Time (s) | Memory Usage")
    print("--------------------------------------------------")
    for name, cost, exec_time, memory in results:
        print(f"{name}: {cost} | {exec_time:.4f} sec | {memory} states")

if __name__ == "__main__":
    main()