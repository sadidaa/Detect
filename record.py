import pyzed.sl as sl # has zed stuff

def main():
	zed = sl.Camera() # creates camera object

	# Configuration parameters
	init_params = sl.InitParameters()
	init_params.camera_resolution = sl.RESOLUTION.RESOLUTION_HD1080
	init_params.camera_fps = 30

	err = zed.open(init_params)
	if err != sl.ERROR_CODE.SUCCESS:
    	exit(-1)

    image = sl.Mat()
    runtime_parameters = sl.RuntimeParameters()
    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
    	zed.retrieve_image(image, sl.VIEW.VIEW_LEFT) # retrieves left image. stored in image

   #can use zed.setcamerasettings or something to change settings

   #recording
    path_output = #put output video file here
    err = zed.enable_recording(path_output, sl.SVO_COMPRESSION_MODE.SVO_COMPRESSION_MODE_LOSSLESS)
    while !exit_app :
    if zed.grab() == sl.ERROR_CODE.SUCCESS :
        # Each new frame is added to the SVO file
        zed.record()
        zed.disable_recording() #disable recording at end


if __name__ == "__main__":
    main()