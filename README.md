# 使い方
詳しくはesa

dockerで環境をつくってあるので、opencvが面倒だったり、ubuntu18.04 melodicならdockerを使える

```
#catchroboの中で

docker compose up -d
docker exec -it ros-noetic bash

#dockerが起動したら
cd catkin_ws
catkin_make
cd
bash
rosrun catchrobo detect_jagariko.py
```