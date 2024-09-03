#pragma once

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
#ifndef deg2rad
#define deg2rad (M_PI / 180.0)
#define rad2deg (180.0 / M_PI)
#define deg2radf static_cast<float>(deg2rad)
#define rad2degf static_cast<float>(rad2deg)
#endif
