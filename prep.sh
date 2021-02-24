#!/usr/bin/env bash
makedir weights
gdown "https://drive.google.com/uc?id=1ZPu1YR2UzGHQD0o1rEqy-j5bmEm3lbyP&export=download" -O "./weights/yolact_plus_resnet50_54_800000.pth"

