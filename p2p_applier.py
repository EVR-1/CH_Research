import subprocess
import argparse

def run_p2p_algo_cch(input_file, output_file, balance):
    """Выполняет команду RunP2PAlgo для алгоритма CCH"""
    try:
        subprocess.run(
            ["RunP2PAlgo", "-a", "CCH", "-o", output_file, "-g", input_file, "-b", str(balance)],
            check=True
        )
        print("RunP2PAlgo CCH выполнен успешно.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения CCH: {e}")

def run_p2p_algo_ch(output_file, h_file, d_file):
    """Выполняет команду RunP2PAlgo для алгоритма CH"""
    try:
        subprocess.run(
            ["RunP2PAlgo", "-a", "CH", "-o", output_file, "-h", h_file, "-d", d_file],
            check=True
        )
        print("RunP2PAlgo CH выполнен успешно.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения CH: {e}")

def main(raw_args=None):
    parser = argparse.ArgumentParser(description="Скрипт для выполнения RunP2PAlgo.")
    parser.add_argument("input_file", help="Имя входного файла (bin).")
    parser.add_argument("balance", type=int, help="Параметр balance.")
    parser.add_argument("output_file", help="Имя выходного файла (o).")
    parser.add_argument("h_file", help="Файл для параметра h.")
    parser.add_argument("d_file", help="Файл для параметра d.")
    
    args = parser.parse_args(raw_args)
    
    # Выполнение команд
    run_p2p_algo_cch(args.input_file, args.h_file, args.balance)
    run_p2p_algo_ch(args.output_file, args.h_file, args.d_file)

if __name__ == "__main__":
    main()
