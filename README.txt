Install ROS with catkin

cd ~/catkin_ws
catkin_make

. ~/catkin_ws/devel/setup.bash
roscd cv_basics
cd launch
roslaunch cv_basics cv_basics_py.launch
