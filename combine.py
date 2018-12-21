import pyzed.sl as sl # has zed stuff

def main():
	zed = sl.Camera() # creates camera object

	# Configuration parameters
	init_params = sl.InitParameters()
	init_params.camera_resolution = sl.RESOLUTION.RESOLUTION_HD1080
	init_params.camera_fps = 30
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.COORDINATE_SYSTEM_RIGHT_HANDED_Y_UP # Use a right-handed Y-up coordinate system
    init_params.coordinate_units = sl.UNIT.UNIT_METER # Set units in meters

	err = zed.open(init_params)
	if err != sl.ERROR_CODE.SUCCESS:
    	exit(-1)

    #enable everything
    image = sl.Mat()
    depth_map = sl.Mat()
    zed_pose = sl.Pose()
    mesh = sl.Mesh() 
    runtime_parameters = sl.RuntimeParameters()
    mapping_parameters = sl.SpatialMappingParameters()
    mapping_parameters.resolution_meter = 0.03 # Set resolution to 3cm
    mapping_parameters.resolution_meter = mapping_parameters.get_resolution_preset(sl.MAPPING_RESOLUTION.MAPPING_RESOLUTION_LOW) # Or use preset
    mapping_parameters.save_texture = True ;  # Scene texture will be recorded
    filter_params = sl.MeshFilterParameters()
    filter_params.set(sl.MESH_FILTER.MESH_FILTER_LOW)
    tracking_parameters = sl.TrackingParameters()
    zed.enable_tracking(tracking_parameters)
    zed.enable_spatial_mapping(mapping_parameters)
    mesh = sl.Mesh() 
    timer=0

    while !exit_app:
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.VIEW_LEFT)
            zed.retrieve_image(depth_for_display, sl.VIEW.VIEW_DEPTH) #depth that can be viewed.
            state = zed.get_position(zed_pose, sl.REFERENCE_FRAME.REFERENCE_FRAME_WORLD)
            print(zed.get_spatial_mapping_state())

            # Display translation and timestamp
            py_translation = sl.Translation()
            tx = round(zed_pose.get_translation(py_translation).get()[0], 3)
            ty = round(zed_pose.get_translation(py_translation).get()[1], 3)
            tz = round(zed_pose.get_translation(py_translation).get()[2], 3)
            print("Translation: tx: {0}, ty:  {1}, tz:  {2}, timestamp: {3}\n".format(tx, ty, tz, zed_pose.timestamp))
            #Display orientation quaternion
            py_orientation = sl.Orientation()
            ox = round(zed_pose.get_orientation(py_orientation).get()[0], 3)
            oy = round(zed_pose.get_orientation(py_orientation).get()[1], 3)
            oz = round(zed_pose.get_orientation(py_orientation).get()[2], 3)
            ow = round(zed_pose.get_orientation(py_orientation).get()[3], 3)
            print("Orientation: ox: {0}, oy:  {1}, oz: {2}, ow: {3}\n".format(ox, oy, oz, ow))

    zed.extract_whole_mesh(mesh)
    mesh.filter(filter_params)
    mesh.apply_texture()
    mesh.save("mesh.obj")
    zed.disable_spatial_mapping()
    zed.disable_tracking()
    zed.close()

if __name__ == "__main__":
    main()