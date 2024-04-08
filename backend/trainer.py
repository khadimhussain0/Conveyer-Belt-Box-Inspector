import os
import json
from ultralytics import YOLO


hyperparameters = {
    "model": 'yolov8m.pt',
    "task":"detect",
    "data":f"{os.path.join(os.getcwd(), 'dataset', 'data.yaml')}",
    "save_period":-1,
    "mask_ratio":2,
    "batch": 1,
    "epochs": 300,
    "retina_masks":True,
    "lr0":0.0001,
    "lrf":0.0001,
    "close_mosaic":0,
    "weight_decay":0.005,
    "warmup_epochs":5,
    "optimizer":"NAdam",
    "imgsz" : [640, 640],
    "cos_lr":True,
    "amp":True,
    "augment":False,
    "cache":False,
    "workers":0,
    "patience":10,
    "resume":False,
    "resume_epoch":"",
    "log_mode":"false",
    "compress_logging_images":True,
    "class_mappings": [
                        {
                            "id": 0,
                            "label": "Box"
                        }
    ]
}

with open("hyperparameters.json", "w") as outfile:
    json.dump(hyperparameters, outfile)

model = YOLO(hyperparameters.get("model", 'yolov8s.pt'))

keys = ["model", "compress_logging_images", "resume_epoch", "class_mappings", "log_mode"]
for key in keys:
    hyperparameters.pop(key)

model.train(**hyperparameters)


