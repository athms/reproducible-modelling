# run analysis steps even if outputs exist
.PHONY : all load evaluate plot
.PHONY : \
	(\
	data/hand_written_digits_data.npy \
	results/data/hyper_params_performance.csv \
	results/figures/fig_hyper_params_effects.png\
)

# define a target for sequentially running each analysis step 
# (can be called with: 'make all')
all : load evaluate plot

# 1. load the handwritten digits dataset
# this analysis step can be called with 'make load'
load : data/hand_written_digits_data.npy 
data/hand_written_digits_data.npy : scripts/load_data.py
	mkdir -p data/;
	python scripts/load_data.py --data-path 'data/'

# 2. evaluate effect of hyper-parameter on predictive model performance
# this analysis step can be called with 'make evaluate'
evaluate : results/data/hyper_params_performance.csv
results/data/hyper_params_performance.csv : scripts/evaluate_hyper_params_effect.py
	mkdir -p results/;
	python scripts/evaluate_hyper_params_effect.py --n 100 --data-path 'data/' --results-path 'results/'

# 3. plot effect of hyper-parameters on predictive model performance
# this analysis step can be called with 'make plot'
plot : results/figures/fig_hyper_params_effects.png
results/figures/fig_hyper_params_effects.png : scripts/plot_hyper_params_effect.py
	python scripts/plot_hyper_params_effect.py --results-path 'results/'



	