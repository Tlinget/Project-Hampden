import bpy
from mathutils import Vector

# =====================================================
# Project Hampden Restoration
# HPH_Project_Scaffold.py
# Blender 4.x
# =====================================================

# ---------- Clean Scene ----------

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Remove unused collections
for c in list(bpy.data.collections):
    if c.name != "Collection":
        bpy.data.collections.remove(c)

scene = bpy.context.scene

# ---------- Units ----------

scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'
scene.unit_settings.scale_length = 1.0

# ---------- Collections ----------

collection_names = [
    "Reference",
    "Blueprints",
    "Stations",
    "Airframe",
    "Interior",
    "Cockpit",
    "Engines",
    "Landing Gear",
    "Control Surfaces",
    "Textures",
    "Materials",
    "Lighting",
    "Cameras",
    "Renders"
]

collections = {}

master = bpy.context.scene.collection

for name in collection_names:

    col = bpy.data.collections.new(name)

    master.children.link(col)

    collections[name] = col

# ---------- World ----------

world = bpy.data.worlds["World"]
world.color = (0.03,0.03,0.03)

# ---------- Origin Empty ----------

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
origin = bpy.context.active_object
origin.name = "Aircraft_Origin"

collections["Reference"].objects.link(origin)
master.objects.unlink(origin)

# ---------- Datum Line ----------

bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
datum = bpy.context.object
datum.name = "Datum"

datum.scale = (20,0.01,0.01)

collections["Reference"].objects.link(datum)
master.objects.unlink(datum)

# ---------- Centerline ----------

bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
center = bpy.context.object
center.name = "Centerline"

center.scale = (0.01,20,0.01)

collections["Reference"].objects.link(center)
master.objects.unlink(center)

# ---------- Fuselage Stations ----------

station_spacing = 0.6096     # 24 inches in meters

station_count = 28

for i in range(station_count):

    x = i * station_spacing

    bpy.ops.object.empty_add(
        type='SINGLE_ARROW',
        location=(x,0,0)
    )

    s = bpy.context.object

    s.name = f"FS_{i:02d}"

    collections["Stations"].objects.link(s)
    master.objects.unlink(s)

# ---------- Wing Datum ----------

bpy.ops.mesh.primitive_plane_add(location=(5.5,0,0))

wing = bpy.context.object

wing.name = "Wing_Datum"

wing.scale=(4,12,1)

collections["Reference"].objects.link(wing)
master.objects.unlink(wing)

# ---------- Cameras ----------

views = {
    "Front":(30,0,0),
    "Side":(0,-30,0),
    "Top":(0,0,30),
    "Perspective":(20,-20,12)
}

for name,pos in views.items():

    bpy.ops.object.camera_add(location=pos)

    cam=bpy.context.object

    cam.name=name+"_Camera"

    collections["Cameras"].objects.link(cam)
    master.objects.unlink(cam)

# ---------- Lights ----------

light_data = bpy.data.lights.new("Sun","SUN")

light = bpy.data.objects.new("Sun",light_data)

light.rotation_euler=(0.7,0.5,0.3)

collections["Lighting"].objects.link(light)

# ---------- Materials ----------

material_names=[
    "RAF_Green",
    "RAF_Brown",
    "Night",
    "Aluminum",
    "Fabric",
    "Glass",
    "Rubber"
]

for m in material_names:

    bpy.data.materials.new(m)

# ---------- View ----------

for area in bpy.context.screen.areas:

    if area.type=="VIEW_3D":

        area.spaces.active.shading.type='SOLID'

print("----------------------------------------")
print("Project Hampden Scaffold Created")
print("----------------------------------------")
print("Units : Metric")
print("Station spacing : 24 inches")
print("Collections : OK")
print("Materials : OK")
print("----------------------------------------")
