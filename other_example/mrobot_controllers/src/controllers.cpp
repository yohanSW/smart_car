#include <mrobot_controllers/controllers/controllers.h>
#include <math.h> //for atan2,sin,cos
#include <stdio.h> //for printf
namespace mrobot_control
{

	controller::controller(int type): type(type) {}
	controller::controller(){}
	controller::~controller(){}
	void controller::setParam(params in){}
	int controller::execute(odometry& odm,laser_sensor& ls){}
	void controller::reset(){}

	stop::stop(){}
	stop::stop(int type)
	{
		out.o_v = 0;
		out.o_w = 0;
	}
	void stop::setParam(params in) {}
	int stop::execute(odometry& odm,laser_sensor& ls) {
		out.o_v = 0;
		out.o_w = 0;
	}
	void stop::reset() {}

	gotoangle::gotoangle(int type) : kp(0)
	{
		in.theta_g = 0;
		in.v_g = 0;
		out.o_v = 0;
		out.o_w = 0;
	}

	void gotoangle::setParam(params in)
	{
		printf("setParam called\n");
		kp = in.kp;
		this->in.v_g = in.argv[0];
		this->in.theta_g = in.argv[1];
		this->in.theta_g = this->in.theta_g * (M_PI/180); //degree to radian
	}

	int gotoangle::execute(odometry& odm, laser_sensor& ls)
	{
		//printf("gotoangle::execute called\n");
		double e_k = in.theta_g - odm.get_theta(); //calculate error
		//printf("&e_k = %p\n",&e_k);
		e_k = atan2(sin(e_k),cos(e_k)); //moderate value from -pi to pi

		double w = kp * e_k;// calculate omega

		out.o_v = in.v_g;
		out.o_w = w;
		printf("out.o_v = %lf, out.o_w = %lf\n",out.o_v,out.o_w);
		return 0;
	}

	void gotoangle::reset()
	{
		kp = 0;
		in.theta_g = 0;
		in.v_g = 0;
	}

	gotogoal::gotogoal(int type) : kp(0),ki(0),kd(0),E_k(0),e_k_1(0)
	{
		in.x_g = 0;
		in.y_g = 0;
		in.v_g = 0;
	}

	void gotogoal::setParam(params in)
	{
		//printf("gotogoal setParam called\n");
		kp = in.kp;
		ki = in.ki;
		kd = in.kd;
		this->in.v_g = in.argv[0];
		this->in.x_g = in.argv[1];
		this->in.y_g = in.argv[2];
		this->d_stop = in.argv[3];
		//printf(" kp %lf ki %lf kd %lf, %lf,%lf,%lf,\n",kp,ki,kd,in.v_g,in.x_g,in.y_g); 
	}

	int gotogoal::execute(odometry& odm,laser_sensor& ls)
	{
		//printf("gotoangle::execute called\n");
		double u_x, u_y; //reference x , y
		double theta_g; //theta goal (theta between goal and ev3)
		double e_k,e_P,e_I,e_D; //PID errors
		double w; //omega

		u_x = in.x_g - odm.get_x();
		u_y = in.y_g - odm.get_y();
		theta_g = atan2(u_y,u_x);
		e_k = theta_g - odm.get_theta();
		e_k = atan2(sin(e_k),cos(e_k));
		//printf("e_k = %lf\n",e_k);
		e_P = e_k;
		e_I = E_k + e_k*0.1; //dt
		e_D = (e_k - e_k_1)/0.1; //dt

		w = kp*e_P + ki*e_I + kd*e_D;

		E_k = e_I;
		e_k_1 = e_k;

		out.o_v = in.v_g;
		out.o_w = w;
		//printf("u_y , u_x , theta_g = %lf, %lf, %lf\n",u_y,u_x,theta_g);
		printf("out.o_v = %lf, out.o_w = %lf\n",out.o_v,out.o_w);
		if(check_event(odm)) return 1;
		return 0;
	}

	void gotogoal::reset()
	{
		kp = ki = kd = 0;
		d_stop = E_k = e_k_1 = 0;
		in.x_g = 0;
		in.y_g = 0;
		in.v_g = 0;
	}

	bool gotogoal::check_event(odometry& odm)
	{
		bool rc = false;
		double x, y, x_g, y_g, e; //current x,y goal x,y error
		x = odm.get_x();
		y = odm.get_y();
		x_g = in.x_g;
		y_g = in.y_g;
		e = d_stop;
		//printf("x = %lf , y = %lf, x_g = %lf, y_g = %lf, e = %lf\n",x,y,x_g,y_g,e);
		if(( x >= x_g - e) && (x <= x_g + e) && (y >= y_g - e) && (y <= y_g + e))//check if arrive
			rc = true;
		return rc;
	}

//---------------------------------------------------------------------------------------------------------------------------------------------------

	gotomultigoal::gotomultigoal(int type) : kp(0),ki(0),kd(0),E_k(0),e_k_1(0)
	{
		in.x_g = 0;
		in.y_g = 0;
		in.v_g = 0;
		in.x_g2 = 0;
		in.y_g2 = 0;
		firstgoal = false;
	}

	void gotomultigoal::setParam(params in)
	{
		//printf("gotogoal setParam called\n");
		kp = in.kp;
		ki = in.ki;
		kd = in.kd;
		this->in.v_g = in.argv[0];
		this->in.x_g = in.argv[1];
		this->in.y_g = in.argv[2];
		this->d_stop = in.argv[3];
		this->in.x_g2 = in.argv[4];
		this->in.y_g2 = in.argv[5];
		//printf(" kp %lf ki %lf kd %lf, %lf,%lf,%lf,\n",kp,ki,kd,in.v_g,in.x_g,in.y_g); 
	}
	int gotomultigoal::execute(odometry& odm,laser_sensor& ls)
	{
		//printf("gotoangle::execute called\n");
		double u_x, u_y; //reference x , y
		double theta_g; //theta goal (theta between goal and ev3)
		double e_k,e_P,e_I,e_D; //PID errors
		double w; //omega
		
		if(firstgoal == false){
		u_x = in.x_g - odm.get_x();
		u_y = in.y_g - odm.get_y();
		}
		else{
		u_x = in.x_g2 - odm.get_x();
		u_y = in.y_g2 - odm.get_y();
		}
		theta_g = atan2(u_y,u_x);
		e_k = theta_g - odm.get_theta();
		e_k = atan2(sin(e_k),cos(e_k));
		//printf("e_k = %lf\n",e_k);
		e_P = e_k;
		e_I = E_k + e_k*0.1; //dt
		e_D = (e_k - e_k_1)/0.1; //dt

		w = kp*e_P + ki*e_I + kd*e_D;

		E_k = e_I;
		e_k_1 = e_k;

		out.o_v = in.v_g;
		out.o_w = w;
		//printf("u_y , u_x , theta_g = %lf, %lf, %lf\n",u_y,u_x,theta_g);
		printf("out.o_v = %lf, out.o_w = %lf\n",out.o_v,out.o_w);
		if(firstgoal == false)
			check_eventfirst(odm);	
		else
			if(check_event(odm)) return 1;
		return 0;
	}

	void gotomultigoal::reset()
	{
		kp = ki = kd = 0;
		d_stop = E_k = e_k_1 = 0;
		in.x_g = 0;
		in.y_g = 0;
		in.v_g = 0;
		in.x_g2 = 0;
		in.y_g2 = 0;
		firstgoal = false;
	}
	
	void gotomultigoal::check_eventfirst(odometry& odm)
	{
		bool rc = false;
		double x, y, x_g, y_g, e; //current x,y goal x,y error
		x = odm.get_x();
		y = odm.get_y();
		x_g = in.x_g;
		y_g = in.y_g;
		e = d_stop;
		//printf("x = %lf , y = %lf, x_g = %lf, y_g = %lf, e = %lf\n",x,y,x_g,y_g,e);
		if(( x >= x_g - e) && (x <= x_g + e) && (y >= y_g - e) && (y <= y_g + e))//check if arrive
			firstgoal = true;
	}

	bool gotomultigoal::check_event(odometry& odm)
	{
		bool rc = false;
		double x, y, x_g, y_g, e; //current x,y goal x,y error
		x = odm.get_x();
		y = odm.get_y();
		x_g = in.x_g2;
		y_g = in.y_g2;
		e = d_stop;
		//printf("x = %lf , y = %lf, x_g = %lf, y_g = %lf, e = %lf\n",x,y,x_g,y_g,e);
		if(( x >= x_g - e) && (x <= x_g + e) && (y >= y_g - e) && (y <= y_g + e))//check if arrive
			rc = true;
		return rc;
	}

//----------------------------------------------------------------------------------------------------------------------------------------------
	avoidobstacle::avoidobstacle(int type) : kp(0),ki(0),kd(0),E_k(0),e_k_1(0),v_g(0)
	{
	}

	void avoidobstacle::setParam(params in)
	{
		//printf("gotogoal setParam called\n");
		kp = in.kp;
		ki = in.ki;
		kd = in.kd;
		v_g = in.argv[0];
		//printf(" kp %lf ki %lf kd %lf\n",kp,ki,kd,in.v_g); 
	}

	int avoidobstacle::execute(odometry& odm,laser_sensor& ls)
	{
		//printf("gotoangle::execute called\n");
		double u_x=0, u_y=0; //reference x , y
		double theta_g; //theta goal (theta between goal and ev3)
		double e_k,e_P,e_I,e_D; //PID errors
		double w; //omega
		double distance[NUM_IR_PTS];
		double v_gain[NUM_IR_PTS] = {0,0.5,0.4,0.3,0.2,0.1,0.2,0.3,0.4,0.5,0};
		
		
		for(int i=0;i<NUM_IR_PTS;i++){
			distance[i]= pow(ls.ir_points[i].x,2)+pow(ls.ir_points[i].y,2);// point (x,y)
			printf("distance = %lf, maxdis = %lf\n",distance[i], pow(MAX_DISTAN,2));
			if(distance[i]==0||distance[i]>pow(MAX_DISTAN,2))
				setmaxdistance(ls, i);
			u_x += v_gain[i] * ls.ir_points[i].x;
			u_y += v_gain[i] * ls.ir_points[i].y;
			printf("***ir_points[%d].x = %lf,ir_points[%d].y = %lf\n",i,ls.ir_points[i].x,i,ls.ir_points[i].y);
			printf("vgain+***ir_points[%d].x = %lf,ir_points[%d].y = %lf\n",i,v_gain[i]*ls.ir_points[i].x,i,v_gain[i]*ls.ir_points[i].y);
		}
		printf("u_x = %lf, u_y = %lf\n",u_x,u_y);

		theta_g = atan2(u_y,u_x); //sensor and robot frame destination -> x,y,theta

		u_x += odm.get_x();
		u_y += odm.get_y();
		//theta_g = atan2(u_y,u_x); //world frame destination

		e_k = theta_g; //- odm.get_theta();
		e_k = atan2(sin(e_k),cos(e_k));
		printf("e_k = %lf\n",e_k);	
		e_P = e_k;
		e_I = E_k + e_k*0.1; //dt
		e_D = (e_k - e_k_1)/0.1; //dt

		w = kp*e_P + ki*e_I + kd*e_D;

		E_k = e_I;
		e_k_1 = e_k;

		out.o_v = v_g;
		out.o_w = w;
		//printf("u_y , u_x , theta_g = %lf, %lf, %lf\n",u_y,u_x,theta_g);
		printf("out.o_v = %lf, out.o_w = %lf\n",out.o_v,out.o_w);
		return 0;
	}

	void avoidobstacle::reset()
	{
		kp = ki = kd = 0;
		d_stop = E_k = e_k_1 = 0;
		v_g = 0;
	}


	void avoidobstacle::setmaxdistance(laser_sensor& ls, int i){
		switch(i){
			case 0: ls.ir_points[i].x = -sqrt(pow(MAX_DISTAN,2)/2);
					ls.ir_points[i].y = sqrt(pow(MAX_DISTAN,2)/2);
					break;
			case 10: ls.ir_points[i].x = -sqrt(pow(MAX_DISTAN,2)/2);
					ls.ir_points[i].y = -sqrt(pow(MAX_DISTAN,2)/2);
					break;
			case 1: ls.ir_points[i].x = 0;
					ls.ir_points[i].y = MAX_DISTAN;
					break;
			case 9: ls.ir_points[i].x = 0;
					ls.ir_points[i].y = -MAX_DISTAN;
					break;
			case 2: ls.ir_points[i].x = sqrt(pow(MAX_DISTAN,2)/4);
					ls.ir_points[i].y = sqrt(3*pow(MAX_DISTAN,2)/4);
					break;
			case 8: ls.ir_points[i].x = sqrt(pow(MAX_DISTAN,2)/4);
					ls.ir_points[i].y = -sqrt(3*pow(MAX_DISTAN,2)/4);
					break;
			case 3: ls.ir_points[i].x = sqrt(pow(MAX_DISTAN,2)/2);
					ls.ir_points[i].y = sqrt(pow(MAX_DISTAN,2)/2);
					break;
			case 7: ls.ir_points[i].x = sqrt(pow(MAX_DISTAN,2)/2);
					ls.ir_points[i].y = -sqrt(pow(MAX_DISTAN,2)/2);
					break;
			case 4: ls.ir_points[i].x = sqrt(3*pow(MAX_DISTAN,2)/4);
					ls.ir_points[i].y = sqrt(pow(MAX_DISTAN,2)/4);
					break;
			case 6: ls.ir_points[i].x = sqrt(3*pow(MAX_DISTAN,2)/4);
					ls.ir_points[i].y = sqrt(pow(MAX_DISTAN,2)/4);
					break;
			case 5: ls.ir_points[i].x = MAX_DISTAN;
					ls.ir_points[i].y = 0;
					break;
			}
	}
}
