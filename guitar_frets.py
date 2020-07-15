import bpy
import numpy as np

def get_selected_pos(name):
    axis = {
    "x":0, "y":1, "z":2,
    "X":0, "Y":1, "Z":2}
    obj = bpy.context.selected_objects[0]
    return obj.location[axis[name]]

def duplicate_linear(distance):
    bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":distance, "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

def calc_angle(opposite, adjacent):
    tan = opposite/adjacent
    atan = np.arctan(tan)
    return np.rad2deg(atan)

def fretSpacing(dn):
    location = -dn/17.817 + dn
    # return location + end - start
    return location

def fretOffset(last, current, start, end):
    off_last = last + end - start
    off_curr = current + end - start
    return off_curr - off_last

# input data
count = 22 # total number of frets to create
start_y = get_selected_pos("Y") # y position of nut
end_y = -0.202374 # y position of bridge

start_z = get_selected_pos("Z") # z position of nut
tri_opp = 0.052675 - start_z # fretboard's highest point
tri_adj = start_y - 0.99367

# data needed for calculations
length = np.abs(start_y - end_y) # fretboard length
tan = tri_opp/tri_adj # tangent

fret_pos = length # y position of first fret
last_fret_pos = length
fret_z_offset = start_z
last_fret_z_offset = start_z

for i in range(count):
    # fret distance in y axis
    fret_y_offset = fretOffset(last_fret_pos, fret_pos, start_y, end_y)
    last_fret_pos = fret_pos
    fret_pos = fretSpacing(fret_pos)
    
    # creates the nth fret
    position = (0, fret_y_offset, last_fret_z_offset - fret_z_offset)
    duplicate_linear(position)
            
    # fret distance in z axis
    last_fret_z_offset = fret_z_offset
    fret_z_offset = fret_pos * tan


