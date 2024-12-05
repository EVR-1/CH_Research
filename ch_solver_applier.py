import subprocess
import argparse

def run_contraction(input_file1, input_file2, output_file, limit, alg):
    """Выполняет команду RunP2PAlgo для алгоритма CCH"""
    try:
        subprocess.run(
            ["contraction", "--map", input_file1, input_file2, "--output", output_file, "-l", str(limit), "-a", alg],
            check=True
        )
        print("contraction выполнен успешно.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения contraction: {e}")

def run_solver(input, instances, output):
    """Выполняет команду RunP2PAlgo для алгоритма CH"""
    try:
        subprocess.run(
            ["ch_solver", "-i", input, "-q", instances, "-o", output],
            check=True
        )
        print("ch_solver выполнен успешно.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения ch_solver: {e}")

def main(raw_args=None):
    parser = argparse.ArgumentParser(description="Скрипт для выполнения contraction и ch_solver.")
    parser.add_argument("input_file1", help="Имя входного файла (gr).")
    parser.add_argument("input_file2", help="Имя входного файла (gr).")
    parser.add_argument("instances")
    parser.add_argument("limit", type=str, help="Параметр limit.")
    parser.add_argument("output_file", help="Имя выходного файла.")
    parser.add_argument("base_dir")
    
    args = parser.parse_args(raw_args)
    
    # Выполнение команд
    base_name = args.output_file.replace(".txt","")
    lm_str = args.limit.replace("0.","")
    basic = f"{args.base_dir}ch_{base_name}{lm_str}_basic.txt"
    batched = f"{args.base_dir}ch_{base_name}{lm_str}_batched.txt"
    basic_res = f"{args.base_dir}ch_{base_name}{lm_str}_basic_res.txt"
    batched_res = f"{args.base_dir}ch_{base_name}{lm_str}_batched_res.txt"
    
    run_contraction(args.input_file1, args.input_file2, basic, float(args.limit), "basic")
    run_contraction(args.input_file1, args.input_file2, batched, float(args.limit), "batched")
    
    run_solver(basic, args.instances, basic_res)
    run_solver(batched, args.instances, batched_res)

if __name__ == "__main__":
    main()
