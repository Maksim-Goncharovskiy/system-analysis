def main(graph_string: str) -> list[list[bool]]:
    """
    graph_string: 'v1,v2\nv1,v3\n'
    """
    edges = graph_string.split('\n')

    # how many vertexes we have ?
    vertexes = set()

    for edge in edges:
        v1, v2 = edge.split(',')
        vertexes.update(v1, v2)

    graph = []

    for i in range(len(vertexes)):
        graph.append([0]*len(vertexes))

    for edge in edges:
        v1, v2 = edge.split(',')
        v1, v2 = int(v1) - 1, int(v2) - 1

        graph[v1][v2], graph[v2][v1] = 1, 1


    return graph


def read_csv(path: str) -> str:
    graph_string = ""

    with open(path, 'r') as csv:
        graph_string = ''.join(csv.readlines())

    return graph_string


def test1():
    csv_path = 'data/task2.csv'

    correct_answer = [
        [0, 1, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]
    ]

    main_answer = main(read_csv(csv_path))

    assert correct_answer == main_answer, "Incorrect answer!"



if __name__ == "__main__":
    try:
        test1()
    except AssertionError:
        print("Incorrect answer")
    else:
        print("Correct!")
    
