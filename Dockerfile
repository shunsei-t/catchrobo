# osrfが提供するrosイメージ（タグがnoetic-desktop-full）をベースとしてダウンロード
FROM osrf/ros:noetic-desktop-full

# Docker実行してシェルに入ったときの初期ディレクトリ（ワークディレクトリ）の設定
WORKDIR /root/

# ROSの環境整理
# ROSのセットアップシェルスクリプトを.bashrcファイルに追記
RUN echo "source /opt/ros/noetic/setup.sh" >> .bashrc
RUN echo "source /root/catkin_ws/devel/setup.bash" >> .bashrc

RUN apt-get update
RUN apt-get install -y python3-pip
RUN python3 -m pip install opencv-python
RUN apt-get install -y ros-noetic-cv-bridge

ENTRYPOINT [ "bash" ]
