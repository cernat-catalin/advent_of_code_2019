def dfs(node, tree, path_len, path_lens):
    children = tree.get(node, [])
    path_lens[node] = path_len
    return path_len + sum([dfs(child, tree, path_len + 1, path_lens) for child in children])


def get_parents(node, parent):
    parents = []
    while node in parent:
        parents.append(parent[node])
        node = parent[node]
    return parents


def find_lca(node1, node2, parent):
    parents_1 = get_parents(node1, parent)
    parents_2 = set(get_parents(node2, parent))
    return next((node for node in parents_1 if node in parents_2), None)


with open('day6/input') as f:
    orbit_pairs = [tuple(line.rstrip().split(')')) for line in f.readlines()]
    tree = {}
    parent = {}
    for k, v in orbit_pairs:
        tree.setdefault(k, []).append(v)
        parent[v] = k

    path_lens = {}
    print(dfs('COM', tree, 0, path_lens)) # part one

    lca = find_lca('YOU', 'SAN', parent)
    print(path_lens['YOU'] + path_lens['SAN'] - 2 * path_lens[lca] - 2) # part two