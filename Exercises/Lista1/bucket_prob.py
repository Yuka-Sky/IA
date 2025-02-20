from collections import deque

capacities = (4, 3)  
start_state = (0, 0)  

def get_neighbors(state, capacities):
    """Returns possible next states from the current state."""
    a, b = state
    a_max, b_max = capacities
    possible_moves = set([
        (a_max, b),   # Fill bucket A
        (a, b_max),   # Fill bucket B
        (0, b),       # Empty bucket A
        (a, 0),       # Empty bucket B
        (max(0, a - (b_max - b)), min(b_max, b + a)),  # Pour A → B
        (min(a_max, a + b), max(0, b - (a_max - a)))   # Pour B → A
    ])
    return possible_moves

def bfs(capacities, start, goal_amount):
    """Breadth-First Search to find the shortest solution."""
    queue = deque([(start, [])])
    visited = set()

    while queue:
        current_state, path = queue.popleft()
        if current_state in visited:
            continue
        visited.add(current_state)
        if current_state[0] == goal_amount:
            return path + [current_state]
        for neighbor in get_neighbors(current_state, capacities):
            if neighbor not in visited:
                queue.append((neighbor, path + [current_state]))

    return None


def dfs_limited(capacities, start, goal_amount, max_depth):
    """Depth-First Search with a depth limit."""
    stack = [(start, [], 0)]
    visited = set()

    while stack:
        current_state, path, depth = stack.pop()
        if current_state in visited:
            continue
        visited.add(current_state)
        if current_state[0] == goal_amount:
            return path + [current_state]
        if depth < max_depth:
            for neighbor in get_neighbors(current_state, capacities):
                if neighbor not in visited:
                    stack.append((neighbor, path + [current_state], depth + 1))

    return None

def iddfs(capacities, start, goal_amount, max_depth):
    """Iterative Deepening DFS that increases depth limit gradually."""
    for depth in range(max_depth + 1):
        solution = dfs_limited(capacities, start, goal_amount, depth)
        if solution:
            return solution
    return None


def main():
    while True:
        try:
            goal_amount = int(input(f"Enter the goal amount (0 to {capacities[0]} liters in bucket A): "))
            if 0 <= goal_amount <= capacities[0]:
                break
            else:
                print(f"Invalid input! Enter a number between 0 and {capacities[0]}.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")

    while True:
        print("\nChoose an algorithm to solve the Two Buckets Problem:")
        print("1. Breadth-First Search (BFS)")
        print("2. Depth-First Search (DFS - Limited Depth)")
        print("3. Iterative Deepening Depth-First Search (IDDFS)")
        print("4. Exit")
        
        choice = input("Enter your choice (1/2/3/4): ").strip()
        
        if choice == "1":
            solution = bfs(capacities, start_state, goal_amount)
            algorithm = "BFS"
        elif choice == "2":
            max_depth = int(input("Enter max depth for DFS: "))
            solution = dfs_limited(capacities, start_state, goal_amount, max_depth)
            algorithm = "DFS (Limited Depth)"
        elif choice == "3":
            max_depth = int(input("Enter max depth for IDDFS: "))
            solution = iddfs(capacities, start_state, goal_amount, max_depth)
            algorithm = "IDDFS"
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please enter 1, 2, 3, or 4.")
            continue

        # Display the solution
        if solution:
            print(f"\n{algorithm} Solution for goal {goal_amount}L in bucket A:")
            for step in solution:
                print(step)
        else:
            print(f"\nNo solution found using {algorithm}.")

if __name__ == "__main__":
    main()
