.PHONY: run build clean

run:
	python main.py

build:
	python -m py_compile main.py simulation.py \
		market/market.py market/financial_instrument.py market/transaction.py \
		investor/investor.py investor/conservative_investor.py \
		investor/aggressive_investor.py investor/algorithmic_investor.py \
		event/event.py event/growth_event.py event/decline_event.py \
		event/crash_event.py event/bubble_event.py
	@echo "Build successful — all files compiled without errors."

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -f simulation_results.csv
