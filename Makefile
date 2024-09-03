@PHONY: setup
setup:
	@echo "Setting up environment..."
	pip install -r requirements.txt

@PHONY: init
init:
	@echo "Initializing data..."
	python init_data.py

@PHONY: run
run: init
	@echo "Running performance tests..."
	locust -f "vexination.py, bombastic.py" -u 60 -r 2 -t 30s --headless --csv=results/locust

run-ui: init
	@echo "Running performance tests..."
	locust -f "vexination.py, bombastic.py" -u 60 -r 2 -t 30s --csv=results/locust


all: setup run
	@echo "Done!"