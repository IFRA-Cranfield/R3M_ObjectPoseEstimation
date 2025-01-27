cmake_minimum_required(VERSION 3.8)
project(ros2_ope)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# =========================================================== #
# REQUIRED TO EXECUTE .py scripts:
install(
  DIRECTORY 
    python
    opencv
    yolo
  DESTINATION 
    share/${PROJECT_NAME}
)
install(PROGRAMS
  
  python/imgROS2.py
  python/convertSAMPLES.py
  python/RecordSamples_Gazebo.py
  python/RecordSamples_Camera.py

  yolo/train.py
  yolo/predict.py

  opencv/calibration/calibrate.py
  opencv/calibration/getsample_Gz.py
  
  opencv/arucoMRKR.py
  opencv/gridPARAMS.py
  opencv/PositionEstimation_SingleMarker.py
  opencv/PositionEstimation_MarkerGrid.py

  DESTINATION lib/${PROJECT_NAME} 
)

ament_package()