import sys
sys.setrecursionlimit(10000)


def tarjan(n, muchii):
    """Returneaza (puncte_de_articulatie, componente_biconexe)
    pentru un graf neorientat cu varfurile 1..n."""
    adj = {v: [] for v in range(1, n + 1)}
    for u, v in muchii:
        adj[u].append(v)
        adj[v].append(u)

    disc, low = {}, {}
    timp = [0]
    stiva = []            # stiva de muchii
    blocuri = []
    articulatii = set()

    def dfs(u, parinte):
        timp[0] += 1
        disc[u] = low[u] = timp[0]
        copii = 0
        for v in adj[u]:
            if v == parinte:
                continue
            if v not in disc:                 # muchie de arbore
                copii += 1
                stiva.append((u, v))
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] >= disc[u]:         # u separa subarborele lui v
                    if parinte is not None or copii > 1:
                        articulatii.add(u)
                    bloc = set()
                    while True:
                        e = stiva.pop()
                        bloc.update(e)
                        if e == (u, v):
                            break
                    blocuri.append(sorted(bloc))
            elif disc[v] < disc[u]:           # muchie inapoi
                stiva.append((u, v))
                low[u] = min(low[u], disc[v])

    for s in range(1, n + 1):
        if s not in disc:
            dfs(s, None)
    return sorted(articulatii), blocuri


if __name__ == "__main__":
    # Test 1: doua triunghiuri legate printr-un varf comun + un pod
    g1 = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (6, 4)]
    art, blocuri = tarjan(6, g1)
    print("Graf 1")
    print("Puncte de articulatie:", art)      # [3, 4]
    print("Componente biconexe:", blocuri)    # [1,2,3], [3,4], [4,5,6]

    # Test 2: graful din Exercitiul 2 (nu are puncte de articulatie)
    k5a = [(a, b) for a in range(1, 6) for b in range(a + 1, 6)]
    k5b = [(a, b) for a in range(6, 11) for b in range(a + 1, 11)]
    g2 = k5a + k5b + [(3, 6), (5, 6), (5, 8)]
    art, blocuri = tarjan(10, g2)
    print("\nGraf 2 (Exercitiul 2)")
    print("Puncte de articulatie:", art)      # []
    print("Componente biconexe:", blocuri)    # un singur bloc cu toate cele 10 varfuri