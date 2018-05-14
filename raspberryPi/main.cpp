#include "common.h"

using namespace hyd;

//Global Variable
void init_setting();

int main(int argc, char *argv[] ){
	//Local variable + class

	cout << "wowong!"<< endl;


	//setting all (+multi thread)
	init_setting();
	//thread t1(&Fever::get_sensor, &room1.patient1);			//thread ¿¹½Ã.
	//thread t2(&Vegetative::get_sensor, &room1.patient2);

	// while loop
	while(true){
		cout << "in while\n"<< endl;
		//kaa part

	}
	//t1.join();
	//t2.join();
	return 0;
}



void init_setting(){
	printf("%s \n", "main setting Start!");
	fflush(stdout);
	
}
