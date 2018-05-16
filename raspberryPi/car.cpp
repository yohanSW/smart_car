#include "car.h"

namespace hyd_15th
{

	void Car::gpio_setting(){
/*		//setup GPIO in wiringPi mode
		if (wiringPiSetupGpio() == -1){
		fprintf (stdout, "Unable to start wiringPi: %s\n", strerror (errno)) ;
		exit(1);
		}
		
		pinMode(FAN, OUTPUT);
		pinMode(BUTTON, INPUT);
		pinMode(LED_RED, OUTPUT);
		pinMode(LED_YELLOW, OUTPUT);*/

	}

	void Car::setup_raspberry(){
				cout << "raspberry setting" <<endl;
				controller.setup_aduino("/dev/tty0");
				gpio_setting();
	}

	
	void Car::print(){
//		cout << "Car print << \t room temp : " << room_temp <<  endl;				변수 출력 예시
		controller.print();
		
		cout << endl;
	}
	
	

}