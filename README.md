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

# GR -> REDUCE

To zip 2 gr files

```
python3 gr_reduce2bin.py ./data/USA-road-d.NY.gr ./data/USA-road-t.NY.gr \
--output_multiplicative mult.dist.gr --output_lambda lambda.dist.gr \
```

# ch_solver_applier

To apply `contraction and ch_solver` to graph files

```
python3 p2p_applier.py graph1.gr graph2.gr instances.txt 0.9 output ./temp
```

# Run task1

To run `gr_reduce2` and `ch_solver_applier`

```
python3 run_task1.py c1.gr c2.gr
```
