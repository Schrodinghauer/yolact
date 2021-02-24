#!/usr/bin/env bash
python3 eval.py --trained_model=weights/yolact_plus_resnet50_54_800000.pth --score_threshold=0.3 --top_k=2 --images=./input:./output

