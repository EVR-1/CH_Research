import argparse
import subprocess
import itertools


def normalize_weights(edges1, edges2):
    """Нормализует веса рёбер в диапазон [0, 1]."""
    weights1 = [weight for _, _, weight in edges1]
    weights2 = [weight for _, _, weight in edges2]
    min_weight1 = min(weights1)
    max_weight1 = max(weights1)
    min_weight2 = min(weights2)
    max_weight2 = max(weights2)
    #if max_weight1 == min_weight1:
    #    return [(u, v, 1) for u, v, _ in edges]  # Если все веса одинаковы, нормализуем до 1
    return [(u, v, (weight1 - min_weight1) / (max_weight1 - min_weight1)) for u, v, weight1 in edges1], [(u, v, (weight2 - min_weight2) / (max_weight2 - min_weight2)) for u, v, weight2 in edges2]

def apply_multiplicative_convolution(w1, w2):
    """Возвращает произведение весов для мультипликативной свертки."""
    if w1 * w2 > 1073741822:
        return 1073741822
    else:
        return w1 * w2

def apply_lambda_convolution(w1, w2, lambd=0.5):
    """Возвращает результат свертки с параметром λ."""
    return lambd * w1 + (1 - lambd) * w2

def process_graph_files(file1, file2, output_multiplicative, output_lambda, lambd=0.5):
    header_line = None
    minimax1_edges = []
    minimax2_edges = []
    multiplicative_edges = []
    lambda_edges = []

    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        for line1, line2 in zip(f1, f2):
            # Если строка начинается с 'p', сохраняем ее как заголовок для всех файлов
            if line1.startswith('p'):
                header_line = line1.strip()
                continue
            # Пропуск комментариев
            if line1.startswith('c') or line2.startswith('c'):
                continue

            # Разделяем строки на вершины и веса
            u1, v1, w1 = map(float, line1.split()[1:])
            u2, v2, w2 = map(float, line2.split()[1:])

            # Проверяем, что рёбра идентичны
            assert (u1, v1) == (u2, v2), "Рёбра в файлах не совпадают"

            # Применяем свертки
            multiplicative_weight = apply_multiplicative_convolution(w1, w2)

            # Сохраняем рёбра для последующей нормализации минимакс-свертки
            minimax1_edges.append((int(u1), int(v1), w1))
            minimax2_edges.append((int(u2), int(v2), w2))
            multiplicative_edges.append((int(u1), int(v1), multiplicative_weight))

    # Нормализация минимакс-свертки
    minimax1_edges, minimax2_edges = normalize_weights(minimax1_edges,minimax2_edges)
    for i in range(len(minimax1_edges)):
        lambda_weight = apply_lambda_convolution(minimax1_edges[i][2], minimax2_edges[i][2], lambd)
        lambda_edges.append((int(u1), int(v1), lambda_weight))    

    # Записываем результаты в файлы с добавлением заголовка
    with open(output_multiplicative, 'w') as out_multiplicative, \
         open(output_lambda, 'w') as out_lambda:
             
        out_multiplicative.write("c This file is generated by a script\n")
        out_lambda.write("c This file is generated by a script\n")
        
        if header_line:
            out_multiplicative.write(header_line + "\n")
            out_lambda.write(header_line + "\n")

        for u, v, weight in multiplicative_edges:
            out_multiplicative.write(f"a {u} {v} {weight}\n")
        for u, v, weight in lambda_edges:
            out_lambda.write(f"a {u} {v} {weight}\n")

    # Выполняем ConvertGraph для каждого выходного файла и затем GenerateODPairs
    bin_multiplicative = convert_graph(output_multiplicative)
    bin_lambda = convert_graph(output_lambda)

    generate_od_pairs(bin_multiplicative)
    generate_od_pairs(bin_lambda)

def convert_graph(filename):
    """Выполняет команду ConvertGraph для указанного файла .gr и возвращает имя бинарного файла .bin."""
    t_name = filename.replace(".dist.gr","")
    print(t_name)
    out_name = t_name + "_graph"
    command = [
        "./ConvertGraph", "-s", "dimacs", "-d", "binary",
        "-a", "capacity", "coordinate", "free_flow_speed", "lat_lng", "length",
        "-i", t_name, "-o", out_name
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Успешно выполнено ConvertGraph для {filename}")
    except subprocess.CalledProcessError:
        print(f"Ошибка при выполнении ConvertGraph для {filename}")
    return out_name + ".gr.bin"

def generate_od_pairs(filename):
    """Выполняет команду GenerateODPairs для указанного бинарного графа .bin."""
    t_name = filename.replace(".gr.bin","")
    out_name = t_name + "_graph_pairs"
    command = [
        "./GenerateODPairs", "-n", "100", "-r", "1", "-d", "10", "-geom",
        "-g", filename, "-o", out_name
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Успешно выполнено GenerateODPairs для {filename}")
    except subprocess.CalledProcessError:
        print(f"Ошибка при выполнении GenerateODPairs для {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Свертка двух графов с разными методами.")
    parser.add_argument("file1", type=str, help="Путь к первому .gr файлу.")
    parser.add_argument("file2", type=str, help="Путь ко второму .gr файлу.")
    parser.add_argument("--output_multiplicative", type=str, default="output_multiplicative.gr", help="Имя выходного файла для мультипликативной свертки.")
    parser.add_argument("--output_lambda", type=str, default="output_lambda.gr", help="Имя выходного файла для свертки с параметром лямбда.")
    parser.add_argument("--lambda_value", type=float, default=0.5, help="Значение параметра лямбда для свертки с параметром лямбда.")

    args = parser.parse_args()

    process_graph_files(
        args.file1, 
        args.file2, 
        args.output_multiplicative, 
        args.output_lambda, 
        args.lambda_value
    )
