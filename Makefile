.PHONY: build run clean

build:

run:
	python3 MyBot.py

clean:
	find . -name "*.pyc" -type f -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -rf ./*.hlt
	rm -rf ./*.log
	rm -rf ./visualizer/*x*.htm
	rm -rf ./replays/*x*.hlt