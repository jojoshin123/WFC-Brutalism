import os
import sys
import bpy
dir = os.path.dirname(bpy.data.filepath) + "/MJr/runtime/"
sys.path.append(dir)
path = os.path.dirname(bpy.data.filepath) + "/compiled_base.py"
exec(open(path).read())

#-------------------------------------------------------------------
dim = 20
coordinates = []
base_objects = []
ceil_objects = []
plaster_mat = bpy.data.materials.get("Plaster")
base_coll = bpy.data.collections.new("Base")
ceil_coll = bpy.data.collections.new("Ceiling")
base_tile = bpy.data.objects.get('base')
ceil_tile = bpy.data.objects.get('base_c')
light_fix = bpy.data.objects.get('light_fix')
#-------------------------------------------------------------------

def redraw():
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    
def render_base():
    # Duplicate the model
    base_copy = base_tile.copy()
    base_copy.data = base_tile.data.copy()
    
    # Set the location of the new instance
    base_copy.location = (i-trans_offset, j-trans_offset, 1)
    
    # Save the new instance to the current collection + array
    base_coll.objects.link(base_copy)
    base_objects.append(base_copy)
    
    base_copy.data.materials[0] = plaster_mat

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
    
def join_tiles_and_apply(arr):
    for tile in arr:
        tile.select_set(True)
    bpy.context.view_layer.objects.active = arr[0]
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
    bpy.ops.object.join()
    bpy.ops.object.select_all(action='DESELECT')
#-------------------------------------------------------------------

bpy.context.scene.collection.children.link(base_coll)
bpy.context.scene.collection.children.link(ceil_coll)

# Run MJr & get result grid
*_, last = main(dim, dim)
row_maj_data = last.grid.data # row-major order

trans_offset = dim//2
for i in range(dim):
    for j in range(dim):
        if row_maj_data[(i*dim)+j] > 0 :
            render_base()
            redraw()
            render_ceiling(row_maj_data[(i*dim)+j] == 2) # send in "Red" bool
            redraw()

join_tiles_and_apply(base_objects)
join_tiles_and_apply(ceil_objects)

base_objects[0].select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
    
print("done.")

