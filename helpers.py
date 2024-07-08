# This file is just to track the helper methods in main script file

def redraw():
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    
def render_base(isEdge):
    # Duplicate the model
    base_copy = base_tile.copy()
    base_copy.data = base_tile.data.copy()
    
    # Set the location of the new instance
    base_copy.location = (i-trans_offset, j-trans_offset, 1)
    
    # Save the new instance to the current collection + array
    base_coll.objects.link(base_copy)
    base_objects.append(base_copy)
    
    base_copy.data.materials[0] = plaster_mat
    
    if isEdge:
        base_edges.append((base_copy.location[0], base_copy.location[1]))
        

def render_ceiling(isRed):
    # Duplicate the model
    ceil_copy = ceil_tile.copy()
    ceil_copy.data = ceil_tile.data.copy()
    
    # Set the location of the new instance
    ceil_copy.location = (i-trans_offset, j-trans_offset, 5)
    
    # Add light if Red
    if isRed:
        addLights(i-trans_offset, j-trans_offset, 5)
    
    # Save the new instance to the current collection + array
    ceil_coll.objects.link(ceil_copy)
    ceil_objects.append(ceil_copy)
    
    ceil_copy.data.materials[0] = plaster_mat
    
def addLights(x, y, z):
    # Add fixture
    light_copy = light_fix.copy()
    light_copy.data = light_fix.data.copy()
    light_copy.location = (x, y, z-0.2)
    
    bpy.ops.object.light_add(type='POINT', location=(x, y, z-0.2))
    light = bpy.context.object
    light.data.energy = 500
    light.data.color = (1.0, 1.0, 1.0)
    light.data.shadow_soft_size = 0.06
    
    ceil_coll.objects.link(light_copy)
    ceil_coll.objects.link(light)
    ceil_objects.append(light_copy)
    ceil_objects.append(light)
    
def join_tiles(arr):
    for tile in arr:
        tile.select_set(True)
    bpy.context.view_layer.objects.active = arr[0]
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    bpy.ops.object.select_all(action='DESELECT')
    return arr[0]
    
def add_edges(base_parent):
    
    
    for edge in base_edges:
        create_wall("x", edge)
        
            
def create_wall(axis, location):
    
    # Don't create the wall if it's right in front of camera
    is_width_bad = math.fabs(location[0]) < math.fabs(camera.location[0]+1.5)
    is_depth_bad = location[1] > (camera.location[1]-3)
    if (is_width_bad and is_depth_bad):
        print("WALL IN FRONT")
        return
    
    # Duplicate the model
    wall_copy = wall_tile.copy()
    wall_copy.data = wall_tile.data.copy()
    
    # Set the location of the new instance
    wall_copy.location = (location[0], location[1], 3)
    
    # Save the new instance to the current collection
    wall_coll.objects.link(wall_copy)
    
    # Set rotation
    if axis == "y":
        bpy.context.view_layer.objects.active = wall_copy
        wall_copy.select_set(True)
        bpy.ops.transform.rotate(value=math.radians(90), orient_axis='Z')
        bpy.ops.object.select_all(action='DESELECT')
    
    wall_copy.data.materials[0] = plaster_mat
    
   