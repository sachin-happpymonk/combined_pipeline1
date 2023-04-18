import subprocess as sp

def cuda_status():
    command = "nvidia-smi"
    print(sp.getoutput(command))

while True:
    cuda_status()
