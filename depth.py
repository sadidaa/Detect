import pyzed.sl as sl # has zed stuff

def main():
	zed = sl.Camera() # creates camera object

	# Configuration parameters
	init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_ULTRA # Use ULTRA depth mode
    init_params.coordinate_units = sl.UNIT.UNIT_MILLIMETER # Use millimeter units (for depth measurements)

    image = sl.Mat()
    depth_map = sl.Mat()
    runtime_parameters = sl.RuntimeParameters() 
    if zed.grab(runtime_parameters) ==  sl.ERROR_CODE.SUCCESS :
        # A new image and depth is available if grab() returns SUCCESS
        zed.retrieve_image(image, sl.VIEW.VIEW_LEFT) # Retrieve left image
        zed.retrieve_measure(depth_map, sl.MEASURE.MEASURE_DEPTH) # Retrieve depth as 32 bit image

        depth_value = depth_map.get_value(x,y) #gets depth value at (x,y)

        depth_for_display = sl.Mat()
        zed.retrieve_image(depth_for_display, sl.VIEW.VIEW_DEPTH) # gives 8 bit depth that can be visuallised

        #can get point cloud also as matrix
        point_cloud = sl.Mat()
        zed.retrieve_measure(point_cloud, sl.MEASURE.MEASURE_XYZRGBA)
	    
        # get x,y,z values of a pixel
        point3D = point_cloud.get_value(i,j)
        x = point3D[0]
        y = point3D[1]
        z = point3D[2]
        color = point3D[3]

        #measures distance of a point. not jsut depth value
        point3D = point_cloud.get_value(i,j)
        distance = math.sqrt(point3D[0]*point3D[0] + point3D[1]*point3D[1] + point3D[2]*point3D[2])

        #changing depth resolution and running on gpu:
        point_cloud = sl.Mat()
        # Retrieve a resized point cloud
        # width and height specify the total number of columns and rows for the point cloud dataset
        width = zed.get_resolution().width / 2;
        height = zed.get_resolution().height / 2;
        zed.retrieve_measure(point_cloud, sl.MEASURE.MEASURE_XYZRGBA, sl.MEM.MEM_GPU, width, height)

if __name__ == "__main__":
    main()