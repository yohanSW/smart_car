#ifndef SH_ICU
#define SH_ICU
#include "common.h"
#include "mcu.h"

namespace han
{

	class ICU{
		private:
			double room_temp;
			int danger_situation;
			
		public:
			ICU(){	room_temp = 0;	danger_situation = 0;	}
			Fever patient1;
			Vegetative patient2;
			Nurse nurse;
			int get_danger_situation(){return danger_situation;}
			double get_room_temp(){return room_temp;}
			void print();

			void gpio_setting(); // ¹ÎÁö
			void setup_raspberry();
			void upload_data(); //kaa°ü·Ã

			void situation_control(); // ¹ÎÁö
	};

}
#endif /* SH_ICU */