#ifndef SC_CAR
#define SC_CAR
#include "common.h"
#include "mcu.h"

namespace hyd_15th
{

	class Car{
		private:
			//double room_temp;									변수 예시
			
		public:
			Car(){		}										//기본생성자
			Mcu controller;										//Mcu class 선언
			
//			double get_room_temp(){return room_temp;}			변수 get함수 예시
//			void set_room_temp(double num){room_temp = num;}	변수 set함수 예시

			void print();										//필요 함수들 선언 ( 정의는 cpp파일에서 함. )

			
			void setup_raspberry();
			void gpio_setting(); 

	};

}
#endif /* SC_CAR */