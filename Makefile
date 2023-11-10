MODULE := outliers
PROJECT_NAME := mlewp-ed2-ch4-outliers
PYTHON_INTERPRETER := python3
ARCH := $(shell $(PYTHON_INTERPRETER) -c "import platform;
print(platform.platform())")
VIRTUALENV := conda
CONDA_EXE ?= ~/anaconda3/bin/conda
EASYDATA_LOCKFILE := environment.$(ARCH).lock.yml