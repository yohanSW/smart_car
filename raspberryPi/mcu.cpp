#include "ICU.h"

namespace hyd_15th
{
	void Mcu::setup_aduino(string device_port){
		cout << "aduino setting" <<endl;

		//get filedescriptor
		if ((fd = serialOpen (device_port.c_str(), 9600)) < 0){
			fprintf (stderr, "Unable to open serial device: %s\n", strerror (errno)) ;
			exit(1); //error
		}
 
		//setup GPIO in wiringPi mode
		if (wiringPiSetup () == -1){
			fprintf (stdout, "Unable to start wiringPi: %s\n", strerror (errno)) ;
			exit(1); //error
		}

		//setup the others
		
	}

	
	void Mcu::print(){
		
		cout << endl;
	}
	
}