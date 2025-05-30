# Running NVIDIA Triton Inference Server with NERSC Superfacility API

## Overview
This is a simple proof of concept to run NVIDIA Triton Inference Server with NERSC Superfacility API. The code in this repository is designed to run tests such as the procedures described in [slurm_triton_deployment](https://github.com/asnaylor/slurm_triton_deployment).

## Acquiring credentials
To run the code in this repository, you will need to acquire credentials for the NERSC Superfacility API. You can do this by following the instructions in the [NERSC Superfacility API documentation](https://docs.nersc.gov/services/sfapi/).

Once you have your credentials, you should copy them to a safe location and update the `settings.cfg` file in the root of this directory with their location.

## Cloning slurm_triton_deployment
You will need to clone the [slurm_triton_deployment](https://github.com/asnaylor/slurm_triton_deployment) in the root of this directory. This repository contains the code that will be used to run the tests.

```bash
git clone https://github.com/asnaylor/slurm_triton_deployment.git
```

## Setting up the environment

### In a devcontainer
This repository includes a devcontainer configuration that allows you to run the code in a containerized environment that includes most depndencies and tools needed to run the code.

## Installing dependencies
You will need to install the dependencies for the code. This repository uses `uv` to manage the dependencies. You can install the dependencies by running the following commands:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # not needed in devcontainer
uv sync
source .venv/bin/activate
```

## Setup
You will need to make changes to the `settings.cfg` file in the root of this directory to configure the code to use your account and storage locations. At a minimum, you will need to set change the `UserName` and `TransferDir` settings. The transfer directory (`TransferDir`) is the location where the code will transfer files to and from Perlmutter.

## Running the code
You can run the code by executing the `main.py` script. This script will submit a job to Perlmutter that starts an NVIDIA Triton Inference Server instance and registers the woker node with a proxy server running on Spin.
```bash
python3 main.py
```

## Accessing the Triton Inference Server
Once the job is running, you can access the Triton Inference Server by connecting to the proxy server running on Spin. The proxy server will forward requests to the Triton Inference Server instance running on Perlmutter.
The proxy is accessible from the NERSC network at the following URL:
```
frontend-loadbalancer.nersonic.development.svc.spin.nersc.org:4873
```

## Debugging
If you use Visual Studio Code, you can use the Python extension to debug the code with the `Python Debugger: Current File` configuration. You can set breakpoints and run the code in debug mode. This works specially well in the devcontainer.

If you are running the code in a Shifter container, you can use `debugpy` to start a debug server in the container. You can then connect to the debug server using the `Python Debugger: Remote Attach` debug configuration. The `debugpy` module is included in this repository dependencies, so you don't need to install it separately. To start the debug server, you can run the following command in the Shifter container:
```bash
python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client main.py
```
