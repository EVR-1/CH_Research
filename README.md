# CH_Research

Contraction Hierarchy Research
Solution Bi-Objective TA task with:
* Linear approximation + SO-CH + Search
* Bi-CH + Search


# TNTP -> GR

To convert `tntp` to `gr` files use `tntp2gr.py` script:

```
python tntp2gr.py source.tntp values.gr cost.gr
```

`tntp2gr` split `tntp` into 2 `gr` files where first contains values, second - cost

# GR -> REDUCE -> BIN + CSV

To zip 2 gr files and generate bin + csv (input for task1)

```
python3 gr_reduce2bin.py ./data/USA-road-d.NY.gr ./data/USA-road-t.NY.gr \
--output_multiplicative mult.dist.gr --output_lambda lambda.dist.gr \
--lambda_value 0.5
```

`gr_reduce2bin.py` take 2 `gr` files as input, process their zip via 3 heuristics, then it generates `bin` graph and `csv` pairs

HINT: use `.dist.gr` extenstion for compatability with routing-framework

# P2P_Applier

To apply `RunP2PAlgo` to bin and csv files

```
python3 p2p_applier.py graph.gr.bin 30 result ch_result graph_graph_pairs.csv
```

# Run task1

To run `gr_reduce2bin` and `p2p_applier`

```
python3 run_task1.py c1.gr c2.gr
```
