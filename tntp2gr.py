import re
import argparse

def parse_tntp_file(input_file):

    volume_data = []
    cost_data = []
    nodes = set()  # count unique nodes
    edges = 0  # count edges
    max_node = 0

    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Regex for tntp line
    edge_pattern = re.compile(r"(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)")

    for line in lines:
        match = edge_pattern.match(line.strip())
        if match:
            from_node = int(match.group(1))
            to_node = int(match.group(2))
            volume = match.group(3)
            cost = match.group(4)

            volume_data.append(f"a {from_node} {to_node} {volume}")
            cost_data.append(f"a {from_node} {to_node} {cost}")
            
            nodes.add(from_node)
            nodes.add(to_node)
            max_node = max(max_node, from_node, to_node)
            
            edges += 1

    return volume_data, cost_data, len(nodes), edges, max_node

def write_gr_file(output_file, data, num_nodes, num_edges, max_node):
    with open(output_file, 'w') as file:
        file.write("c This file is generated by a script\n")
        file.write(f"p sp {max_node} {num_edges}\n")
        for line in data:
            file.write(f"{line}\n")

def convert_tntp_to_gr(input_file, volume_output_file, cost_output_file):
    volume_data, cost_data, num_nodes, num_edges, max_node = parse_tntp_file(input_file)

    write_gr_file(volume_output_file, volume_data, num_nodes, num_edges, max_node)
    write_gr_file(cost_output_file, cost_data, num_nodes, num_edges, max_node)

def main():
    parser = argparse.ArgumentParser(description="Convert .tntp file to two .gr files containing volume and cost data.")
    parser.add_argument("input_file", type=str, help="Input .tntp file")
    parser.add_argument("volume_output_file", type=str, help="Output .gr file for volume data")
    parser.add_argument("cost_output_file", type=str, help="Output .gr file for cost data")

    args = parser.parse_args()

    convert_tntp_to_gr(args.input_file, args.volume_output_file, args.cost_output_file)

if __name__ == "__main__":
    main()
