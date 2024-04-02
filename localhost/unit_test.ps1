# You must explicitly set CUDA_VISIBLE_DEVICES if you want to use GPU
$env:CUDA_VISIBLE_DEVICES = "0"

# Create a copy of the 'official' config
Copy-Item -Path "exp/mlp/california/0_tuning.toml" -Destination "exp/mlp/california/1_tuning.toml"

# Run tuning (on GPU, it takes ~30-60min)
python bin/tune.py exp/mlp/california/1_tuning.toml

# Evaluate single models with 15 different random seeds
python bin/evaluate.py exp/mlp/california/1_tuning 15

# Evaluate ensembles (by default, three ensembles of size five each)
python bin/ensemble.py exp/mlp/california/1_evaluation

# Then use bin/results.ipynb to view the obtained results