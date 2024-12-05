import subprocess
import argparse
import os

import gr_reduce
import ch_solver_applier

def main():
    # Создание парсера аргументов
    parser = argparse.ArgumentParser(description="Скрипт для вызова двух других скриптов с входными файлами.")
    parser.add_argument("file1", help="Путь к первому входному файлу.")
    parser.add_argument("file2", help="Путь ко второму входному файлу.")
    parser.add_argument("instances")
    args = parser.parse_args()

    # Проверка существования входных файлов
    if not os.path.exists(args.file1) or not os.path.exists(args.file2):
        print("Ошибка: Один или оба входных файла не найдены.")
        return
    
    base_dir = "temp/"
    
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    base_name = args.file1.replace(".gr","")
    probe_base_name = f"output_probe"
    mult_base_name = f"{base_name}_output_multiplicative"
    lambda_base_name = f"{base_name}_output_lambda"
    
    # Вызываем первый скрипт с двумя файлами
    print("gr_reduce2...")
    gr_reduce.main([args.file1, args.file2, "--output_multiplicative" ,f"{mult_base_name}.gr", "--output_lambda",f"{lambda_base_name}.gr", "--output_probe",f"{probe_base_name}.gr"])
    
    # Вызываем второй скрипт для каждого входного файла
    print("ch...")
    
    ch_solver_applier.main([f"{mult_base_name}.gr", f"{probe_base_name}.gr", args.instances , "0.9", f"{mult_base_name}_res.txt", base_dir ])
    ch_solver_applier.main([f"{mult_base_name}.gr", f"{probe_base_name}.gr", args.instances , "0.95", f"{mult_base_name}_res.txt", base_dir  ])
    ch_solver_applier.main([f"{mult_base_name}.gr", f"{probe_base_name}.gr", args.instances , "0.99", f"{mult_base_name}_res.txt", base_dir  ])
    ch_solver_applier.main([f"{mult_base_name}.gr", f"{probe_base_name}.gr", args.instances , "0.995", f"{mult_base_name}_res.txt", base_dir  ])
    for i in range(1,5):
        ch_solver_applier.main([f"{ lambda_base_name}{i}.gr", f"{probe_base_name}.gr", args.instances , "0.9", f"{ lambda_base_name}{i}_res.txt", base_dir  ])
        ch_solver_applier.main([f"{ lambda_base_name}{i}.gr", f"{probe_base_name}.gr", args.instances , "0.95", f"{ lambda_base_name}{i}_res.txt", base_dir  ])
        ch_solver_applier.main([f"{ lambda_base_name}{i}.gr", f"{probe_base_name}.gr", args.instances , "0.99", f"{ lambda_base_name}{i}_res.txt", base_dir  ])
        ch_solver_applier.main([f"{ lambda_base_name}{i}.gr", f"{probe_base_name}.gr", args.instances , "0.995", f"{ lambda_base_name}{i}_res.txt", base_dir  ])

if __name__ == "__main__":
    main()
