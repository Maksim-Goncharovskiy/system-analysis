import numpy as np


def read_csv(path: str) -> str:
    graph_string = ""

    with open(path, 'r') as csv:
        graph_string = ''.join(csv.readlines())

    return graph_string



def make_orient_adj_matrix(graph_string: str) -> np.ndarray[bool]:
    """
    Создаёт матрицу смежности для ориентированного графа.
    graph_string: 'v1,v2\nv1,v3\n'
    """
    edges: list[tuple[str, str]] = [tuple(edge.split(',')) for edge in graph_string.split('\n')]

    vertexes = set()

    for edge in edges:
        v1, v2 = edge[0], edge[1]
        vertexes.update(v1, v2)
    
    vertexes = sorted(list(vertexes))

    vert2indx = {v: i for i, v in enumerate(vertexes)}
    adj_matrix = np.zeros((len(vertexes), len(vertexes)), dtype=bool)
    
    for edge in edges:
        v1, v2 = edge[0], edge[1]
        adj_matrix[vert2indx[v1], vert2indx[v2]] = True

    return adj_matrix



def compute_r1(adj_matr: np.ndarray[bool]) -> np.ndarray[int]:
    return  adj_matr.astype(int)



def compute_r2(r1: np.ndarray[int]) -> np.ndarray[int]:
    return r1.T



def compute_r3(adj_matr: np.ndarray[bool]) -> np.ndarray[int]:
    """r3 = r1 * r1 (булево умножение)
    r3(mi, mk) = r1(mi, mj) and r(mj, mk)
    """
    r3 = adj_matr.copy()

    for _ in range(adj_matr.shape[0] - 1):
        r3 = r3 | (r3 @ adj_matr)

    r3 = (r3 & ~adj_matr).astype(int)

    return r3



def compute_r4(r3: np.ndarray[int]) -> np.ndarray[int]:
    """r4 = r3^T"""
    return r3.T



def compute_r5(r2: np.ndarray[int]) -> np.ndarray[int]:
    """r5 = r2 * r2 (булево умножение)"""
    r2 = r2.copy().astype(bool)
    n = r2.shape[0]
    r5 = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(i + 1, n):
            if np.any(r2[i] & r2[j]):
                r5[i, j], r5[j, i] = 1, 1
    return r5



def main(graph_string: str, root: str) -> tuple[list[list[int]], list[list[int]], list[list[int]], list[list[int]], list[list[int]]]:
    adj_matrix = make_orient_adj_matrix(graph_string)
    r1 = compute_r1(adj_matrix)
    r2 = compute_r2(r1)
    r3 = compute_r3(adj_matrix)
    r4 = compute_r4(r3)
    r5 = compute_r5(r2)
    return (
        r1.tolist(),
        r2.tolist(),
        r3.tolist(),
        r4.tolist(),
        r5.tolist()
    )



if __name__ == "__main__":
    csv_path = 'data/task2.csv'

    Ar = main(read_csv(csv_path), '1')

    for i in range(len(Ar)):
        print(f"r{i+1}: {Ar[i]}\n\n")