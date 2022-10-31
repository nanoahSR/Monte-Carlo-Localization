#ifndef	 _DRIVE_H_
#define  _DRIVE_H_

#include "Points.h"
Pose MoveExact(int i);

class Move {
public:
	int v;
	int omega;
	int time;
};

extern int loop;
extern Move DriveCommand[25];
extern Pose RobotPose[30];
extern int DCLen;

#endif