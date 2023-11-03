# Define variables
VENV_NAME = venv
PYTHON = python3
PIP = $(VENV_NAME)/bin/pip
TARGET = xtest_game_state.py
SCRIPT_NAME = xtest_game_state  # Name of the bash script

# Invokes the whole file when "make" is written in the command line
all: install generate_script

# Create virtual environment
$(VENV_NAME):
	$(PYTHON) -m venv $(VENV_NAME)
	$(PIP) install -U pip

# Install Pillow 
install: $(VENV_NAME)
	$(PIP) install multiline Pillow

# Generate a bash script to invoke the Python script
generate_script:
	echo "#!/bin/bash" >  $(SCRIPT_NAME)
	echo "$(VENV_NAME)/bin/$(PYTHON) $(TARGET)" >> $(SCRIPT_NAME)
	chmod +x $(SCRIPT_NAME) 

# Run the Python script using the generated bash script
run: install generate_script
	./$(SCRIPT_NAME)

# Clean up
clean:
	rm -rf $(VENV_NAME) __pycache__ $(SCRIPT_NAME)

.PHONY: all install generate_script run clean