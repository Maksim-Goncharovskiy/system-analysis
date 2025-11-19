import json
import numpy as np


def read_json(file_path: str) -> str:
    with open(file_path, 'r') as json_file:
        data = json_file.read()
    return data


def build_precedence_matrix(ranking: list[int, list[int]], total_objects: int) -> np.ndarray:
    """
    Формирование матрицы предшествования на основе ранжировки
    """
    positions = [0] * total_objects
    current_position = 0
    
    for cluster in ranking:
        if not isinstance(cluster, list):
            cluster = [cluster]
        for obj in cluster:
            positions[obj - 1] = current_position
        current_position += 1
    
    matrix = np.zeros((total_objects, total_objects), dtype=int)
    for i in range(total_objects):
        for j in range(total_objects):
            if positions[i] >= positions[j]:
                matrix[i, j] = 1
                
    return matrix


def extract_all_objects(rankings: list[list[int, list[int]]]) -> set:
    """Извлекает все уникальные объекты из списка ранжировок."""
    all_objects = set()
    for ranking in rankings:
        for cluster in ranking:
            if not isinstance(cluster, list):
                cluster = [cluster]
            all_objects.update(cluster)
    return all_objects


def find_contradiction_kernel(matrix_ab: np.ndarray, matrix_ab_prime: np.ndarray) -> list[list[int]]:
    """
    Ядро противоречий между двумя матрицами
    """
    kernel = []
    n = matrix_ab.shape[0]
    
    for i in range(n):
        for j in range(i + 1, n):
            if matrix_ab[i, j] == 0 and matrix_ab_prime[i, j] == 0:
                kernel.append([i + 1, j + 1])
                
    return kernel


def main(json_string_a: str, json_string_b: str) -> str:
    ranking_a = json.loads(json_string_a)
    ranking_b = json.loads(json_string_b)
    
    all_objects = extract_all_objects([ranking_a, ranking_b])
    
    if not all_objects:
        return json.dumps([])
    
    total_objects = max(all_objects)
    
    matrix_a = build_precedence_matrix(ranking_a, total_objects)
    matrix_b = build_precedence_matrix(ranking_b, total_objects)
    
    matrix_ab = matrix_a * matrix_b
    matrix_ab_prime = matrix_a.T * matrix_b.T
    
    kernel = find_contradiction_kernel(matrix_ab, matrix_ab_prime)
    
    return json.dumps(kernel)



if __name__ == "__main__":
    json_string_a: str = read_json("task3/ranking-A.json")
    json_string_b: str = read_json("task3/ranking-B.json")

    ground_truth: str = read_json("task3/AB-contradiction-kernel.json")

    answer: str = main(json_string_a, json_string_b)

    assert answer == ground_truth, "Тест не выполнен! Значения не совпали :("