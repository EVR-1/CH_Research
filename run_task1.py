import subprocess
import argparse
import os

import gr_reduce2bin
import p2p_applier

def main():
    # Создание парсера аргументов
    parser = argparse.ArgumentParser(description="Скрипт для вызова двух других скриптов с входными файлами.")
    parser.add_argument("file1", help="Путь к первому входному файлу.")
    parser.add_argument("file2", help="Путь ко второму входному файлу.")
    args = parser.parse_args()

    # Проверка существования входных файлов
    if not os.path.exists(args.file1) or not os.path.exists(args.file2):
        print("Ошибка: Один или оба входных файла не найдены.")
        return
    
    mult_base_name = "output_multiplicative"
    lambda_base_name = "output_lambda"
    
    # Вызываем первый скрипт с двумя файлами
    print("gr_reduce2bin...")
    gr_reduce2bin.main([args.file1, args.file2, "--output_multiplicative" ,f"{mult_base_name}.dist.gr", "--output_lambda",f"{lambda_base_name}.dist.gr"])
    
    # Вызываем второй скрипт для каждого входного файла
    print("p2p_applier")
    
    p2p_applier.main([f"{mult_base_name}_graph.gr.bin", "30" , f"{mult_base_name}_result", f"{mult_base_name}_ch", f"{mult_base_name}_graph_graph_pairs.csv" ])
    for i in range(0,5):
                p2p_applier.main([f"{lambda_base_name}{i}_graph.gr.bin", "30" , f"{lambda_base_name}{i}_result", f"{lambda_base_name}{i}_ch", f"{lambda_base_name}{i}_graph_graph_pairs.csv" ])

if __name__ == "__main__":
    main()
