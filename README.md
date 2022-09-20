# 使い方
詳しくはesa

python3なのでnoetic対応
dockerで環境をつくってあるので、dockerで走らせつつ、melodicでトピックを受け取るなどできる

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

numpyとMultiArray変換の参考記事
https://qiita.com/kotarouetake/items/3c467e3c8aee0c51a50f
