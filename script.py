import bpy
import os
import addon_utils

# Ensure OBJ import add-on is enabled
if not addon_utils.check("io_scene_obj")[1]:
    addon_utils.enable("io_scene_obj")

# === Path to your .obj file (update if needed)
obj_path = "C:/Users/14478/Downloads/office-room-set-ozcan-ozaltin-1.snapshot.2/office.obj"

# === Import office.obj if not already in scene
if "office" not in bpy.data.objects:
    bpy.ops.import_scene.obj(filepath=obj_path)
    office = bpy.context.selected_objects[0]
    office.name = "office"
    office.location = (-13.956, -25.035, 0.001)
    office.rotation_euler = (0, 0, 0)
    office.scale = (1.0, 1.0, 1.0)
else:
    office = bpy.data.objects["office"]

# === Create Suzanne (monkey head) if not already present
if "Suzanne" not in bpy.data.objects:
    bpy.ops.mesh.primitive_monkey_add(location=(10.115, -31.129, 45.947))
    suzanne = bpy.context.active_object
    suzanne.name = "Suzanne"
    suzanne.rotation_euler = (1.5708, 0, 0)
    suzanne.scale = (9.047, 9.047, 9.047)
else:
    suzanne = bpy.data.objects["Suzanne"]

# === Remove old camera if exists
if "AnimatedCam" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["AnimatedCam"], do_unlink=True)

# === Create new camera
bpy.ops.object.camera_add(location=(-297, -140, 500))
cam = bpy.context.active_object
cam.name = "AnimatedCam"

# === Add two Track To constraints: office first, then Suzanne
track_office = cam.constraints.new(type='TRACK_TO')
track_office.name = "TrackOffice"
track_office.target = office
track_office.track_axis = 'TRACK_NEGATIVE_Z'
track_office.up_axis = 'UP_Y'

track_suzanne = cam.constraints.new(type='TRACK_TO')
track_suzanne.name = "TrackSuzanne"
track_suzanne.target = suzanne
track_suzanne.track_axis = 'TRACK_NEGATIVE_Z'
track_suzanne.up_axis = 'UP_Y'

# === Animate constraint influence
track_office.influence = 1
track_suzanne.influence = 0
track_office.keyframe_insert(data_path="influence", frame=1)
track_suzanne.keyframe_insert(data_path="influence", frame=1)

track_office.influence = 0
track_suzanne.influence = 1
track_office.keyframe_insert(data_path="influence", frame=150)
track_suzanne.keyframe_insert(data_path="influence", frame=150)

# === Animate camera movement
cam.location = (-296, -140, 500)     # Far overview
cam.keyframe_insert(data_path="location", frame=1)

cam.location = (-2.7, -9, 108)       # Top-down view
cam.keyframe_insert(data_path="location", frame=75)

cam.location = (17.439, -31.315, 47.624)  # Close-up inside room
cam.keyframe_insert(data_path="location", frame=150)

# === Set scene camera and timeline
bpy.context.scene.camera = cam
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 150

