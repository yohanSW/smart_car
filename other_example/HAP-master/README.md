# HAP
<h3>Picar autonomous driving car</h3>

ball_tracker_version0.1 : Picar의 카메라가 빨간색 공을 인식합니다. 공이 있는 방향으로 자동차가 움직이게 하는 소스입니다.


line_tracker_version0.1 : 파란색 라인을 따라서 Picar가 움직입니다. 선이 끝나면 카메라가 50, 70, 90, 110, 130 도 방향을 탐색하고 
                          선이 없으면 운행을 종료하는 소스입니다.

line_tracker_version0.9 : line_tracker_version0.1 + Face_detection()코드가 추가되어 있는 소스입니다.


line_tracker_version1.0 : line_tracker_version0.9 에 lightOn()코드가 추가되어 있는 소스입니다.
                          * lightOn() function은 신호등의 색깔을 인식합니다. 아직 작업 중에 있습니다.(2017. 07. 02.)
                          
                          완료된 코드입니다. 자동차의 카메라가 빨간원을 인식하면 멈춥니다. 파란원을 인식하면 출발합니다.(2017. 07. 04.)
