#!/bin/bash

export BUS_NUMBER='A123AA22'

export YOLO_MODEL_NAME='./models/yolo/hookahs_v0.3_m_Epochs_80.pt'
export CONF_THRESHOLD=0.6
export TRACKER='./tracker.yaml'

export SOURCE='./videos/output_2024-03-16_23-16-03,46.mp4'
# export SOURCE='./videos/output_2024-03-16_22-44-07,55.mp4'

export SERVER_URL='http://localhost:8001'

export FRAMES_WITHOUT_AN_OBJECT=75
