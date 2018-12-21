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

    # mapping params 
    mapping_parameters = sl.SpatialMappingParameters()
    mapping_parameters.resolution_meter = 0.03 # Set resolution to 3cm
    mapping_parameters.resolution_meter = mapping_parameters.get_resolution_preset(sl.MAPPING_RESOLUTION.MAPPING_RESOLUTION_LOW) # Or use preset
    mapping_parameters.save_texture = True ;  # Scene texture will be recorded

    #some filter params
    filter_params = sl.MeshFilterParameters()
    filter_params.set(sl.MESH_FILTER.MESH_FILTER_LOW)

    tracking_parameters = sl.TrackingParameters()
    zed.enable_tracking(tracking_parameters)
    zed.enable_spatial_mapping(mapping_parameters)

    mesh = sl.Mesh() # Create a mesh object
    timer=0
    runtime_parameters = sl.RuntimeParameters()

    while timer < 500 :
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS :
        # When grab() = SUCCESS, a new image, depth and pose is available.
        # Spatial mapping automatically ingests the new data to build the mesh.*****
        timer+=1


    # Retrieve the mesh
    zed.extract_whole_mesh(mesh)
    # Filter the mesh
    mesh.filter(filter_params)
    # Apply the texture
    mesh.apply_texture()
    # Save the mesh in .obj format
    mesh.save("mesh.obj")


    # Disable spatial mapping, positional tracking and close the camera
    zed.disable_spatial_mapping()
    zed.disable_tracking()
    zed.close()

    # can error handle
    state = zed.get_spatial_mapping_state()


if __name__ == "__main__":
    main()