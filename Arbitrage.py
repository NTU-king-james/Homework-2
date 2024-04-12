def find_arbitrage_from_tokenB(liquidity, fee_percent=0.3):
    # Calculate the fee multiplier
    fee_multiplier = 1 - fee_percent / 100
    # print(f"fee_multiplier: {fee_multiplier}") 
    # Create a graph from the liquidity data
    graph = {}
    for (token1, token2), (num1, num2) in liquidity.items():
        if token1 not in graph:
            graph[token1] = []
        if token2 not in graph:
            graph[token2] = []
        # Create edges with weights as exchange rates adjusted for the fee
        graph[token1].append((token2, num1, num2))
        graph[token2].append((token1, num2, num1))

    def dfs(current_token, visited, balance, path):
        if current_token in visited:
            if current_token == 'tokenB' and balance > 20.0 and len(path) > 1:
                # Found a profitable cycle
                path_str = '->'.join(path + ['tokenB'])
                print(f"path: {path_str}, tokenB balance={balance:.6f}")
                return True
            return False
        visited.add(current_token)
        for next_token, x, y in graph[current_token]:
            deltaX = balance 
            new_balance = (deltaX*997*y)/(x*1000+deltaX*997)
            if dfs(next_token, visited, new_balance , path + [current_token]):
                return True
        visited.remove(current_token)
        return False

    # Start DFS from 'tokenB' to find an arbitrage cycle
    if 'tokenB' in graph:
        dfs('tokenB', set(), 5.0, [])

    
# Liquidity dictionary as provided
liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

find_arbitrage_from_tokenB(liquidity)


