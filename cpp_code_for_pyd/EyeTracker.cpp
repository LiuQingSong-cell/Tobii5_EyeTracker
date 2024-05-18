#include "tobii.h"
#include "tobii_streams.h"
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <Python.h>
#include <vector>
#include <chrono>

static tobii_api_t* api = NULL;

static tobii_error_t result;

static tobii_device_t* device = NULL;

char url[ 256 ] = { 0 };

struct Point
{
    float x;
    float y;
};

static std::vector<Point> GazePoints;


void url_receiver( char const* url, void* user_data )
{
    char* buffer = (char*)user_data;
    if( *buffer != '\0' ) return; // only keep first value

    if( strlen( url ) < 256 )
        strcpy( buffer, url );
}

void gaze_point_callback(tobii_gaze_point_t const* gaze_point, void* /* user_data */)
{
    if (gaze_point->validity == TOBII_VALIDITY_VALID)
    {
        Point p;
        p.x = gaze_point->position_xy[0];
        p.y = gaze_point->position_xy[1];
        GazePoints.push_back(p);
        printf("%f, %f\n", p.x, p.y);
    }
}


void cleanup()
{
    result = tobii_gaze_point_unsubscribe( device );
    assert( result == TOBII_ERROR_NO_ERROR );
    result = tobii_device_destroy( device );
    assert( result == TOBII_ERROR_NO_ERROR );
    result = tobii_api_destroy( api );
    assert( result == TOBII_ERROR_NO_ERROR );
}


PyObject* CheckEyeTracker()
{
    result = tobii_api_create( &api, NULL, NULL );
    assert(result == TOBII_ERROR_NO_ERROR);


    result = tobii_enumerate_local_device_urls( api, url_receiver, url );
    assert( result == TOBII_ERROR_NO_ERROR );
    if(*url == '\0')
    {
        // printf("Error: No device found\n");
        return PyLong_FromLong(-1);
    }
    printf("EyeTracker 5 device url: %s\n", url);
    return PyLong_FromLong(1);
}


PyObject* InitEyeTracker()
{
    result = tobii_device_create( api, url, TOBII_FIELD_OF_USE_INTERACTIVE, &device );
    assert( result == TOBII_ERROR_NO_ERROR );

    // Subscribe to gaze data
    result = tobii_gaze_point_subscribe( device, gaze_point_callback, 0 );
    assert( result == TOBII_ERROR_NO_ERROR );

    return Py_None;
}


PyObject* get_eye_points(PyObject* self, PyObject* args)
{
    int seconds;
    if (!PyArg_ParseTuple(args, "i", &seconds))
    {
        return NULL;
    }
    
    auto start = std::chrono::system_clock::now();

    while (std::chrono::duration_cast<std::chrono::seconds>(std::chrono::system_clock::now() - start).count() < seconds)
    {
        // 处理眼动数据的回调函数
        result = tobii_wait_for_callbacks( 1, &device );
        assert( result == TOBII_ERROR_NO_ERROR || result == TOBII_ERROR_TIMED_OUT );

        // Process callbacks on this thread if data is available
        result = tobii_device_process_callbacks( device );
        assert( result == TOBII_ERROR_NO_ERROR );
    }

    auto gaze_num = GazePoints.size();
    auto all_gaze = PyTuple_New(gaze_num);

    for (unsigned i = 0; i < gaze_num; i ++)
    {
        auto PyPoint = PyTuple_New(2);
		PyTuple_SetItem(PyPoint, 0, PyFloat_FromDouble(GazePoints[i].x));
		PyTuple_SetItem(PyPoint, 1, PyFloat_FromDouble(GazePoints[i].y));
		PyTuple_SetItem(all_gaze, i, PyPoint);
    }
    GazePoints.clear();
    return all_gaze;
}


static PyMethodDef EyeTracker_methods[] = {
	// The first property is the name exposed to Python, fast_tanh, the second is the C++
	// function name that contains the implementation.
	{ "CheckEyeTracker", (PyCFunction)CheckEyeTracker, METH_NOARGS, nullptr },

    {"InitEyeTracker", (PyCFunction)InitEyeTracker, METH_NOARGS, nullptr},

    {"get_eye_points", (PyCFunction)get_eye_points, METH_VARARGS, nullptr}, 

	// Terminate the array with an object containing nulls.
	{ nullptr, nullptr, 0, nullptr }
};

static PyModuleDef EyeTracker_module = {
	PyModuleDef_HEAD_INIT,
	"EyeTracker",                        // Module name to use with Python import statements
	"Provides Tobii Eyetracker's Interface",  // Module description
	-1,
	EyeTracker_methods                   // Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_EyeTracker() {
	return PyModule_Create(&EyeTracker_module);
}