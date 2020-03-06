create_wmt:
	python3 src/main.py config/data/wmt19.yaml
create_wmt_pe_ok:
	python3 src/main.py config/data/wmt19_pe_ok.yaml
create_wmt_pe_synth:
	python3 src/main.py config/data/wmt19_pe_synth.yaml
create_wmt_opus_random:
	python3 src/main.py config/data/wmt19_opus_random.yaml
create_opus:
	python3 src/main.py config/data/opus_random.yaml


train:
	python3 src/main.py config/quetch.yaml
validate:
	python3 src/main.py config/validate.yaml

