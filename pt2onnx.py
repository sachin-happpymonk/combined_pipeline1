
import torch
from memory_profiler import profile


model = torch.hub.load('ultralytics/yolov5', 'custom', path='./three_class_05_dec.pt')
model = torch.quantization.quantize_dynamic(
    model,  # the original model
    {torch.nn.Linear},  # a set of layers to dynamically quantize
    dtype=torch.qint8)  # the target dtype for quantized weights

@profile
def checkk():
    return

checkk()