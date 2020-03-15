create_wmt:
	python3 src/main.py config/data/wmt19.yaml
create_wmt_pe_ok:
	python3 src/main.py config/data/wmt19_pe_ok.yaml
create_wmt_pe_synth:
	python3 src/main.py config/data/wmt19_pe_synth.yaml
create_wmt_opus_random:
	python3 src/main.py config/data/wmt19_opus_random.yaml
create_opus_random:
	python3 src/main.py config/data/opus_random.yaml


train_quetch:
	python3 src/main.py config/quetch.yaml
train_quetch_transfer:
	# this also creates opus data, then trains, then created wmt data, and trains again
	python3 src/main.py config/data/opus.yaml           # load opus data
	python3 src/main.py config/quetch.yaml   # train on opus data and save
	python3 src/mani.py config/data/wmt19.yaml			# load wmt19 data
	python3 src/main.py config/quetch_load_train.yaml	# load model and train 

validate:
	python3 src/main.py config/validate.yaml

