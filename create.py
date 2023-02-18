import os
import sys
import math
import bpy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="path to svg file")
parser.add_argument("-rx", "--rotate-x", help="rotate x axis",
                    type=float, default=0)
parser.add_argument("-ry", "--rotate-y", help="rotate y axis",
                    type=float, default=0)
parser.add_argument("-rz", "--rotate-z", help="rotate z axis",
                    type=float, default=0)
parser.add_argument("-th",
                    "--thickness", help="thickness of the icon", type=float, default=1)
parser.add_argument(
    "-d",
    "--distance", help="distance of the camera", type=float, default=1)
parser.add_argument(
    "-lx",
    "--light-x", help="x position of the light", type=float, default=0)
parser.add_argument(
    "-ly",
    "--light-y", help="y position of the light", type=float, default=0)
parser.add_argument(
    "-lz",
    "--light-z", help="z position of the light", type=float, default=0)
parser.add_argument(
    "-ls",
    "--light-strength", help="strength of the light", type=float, default=1)
parser.add_argument("-r", "--red", help="red color",
                    type=float, default=-1)
parser.add_argument("-g", "--green", help="green color",
                    type=float, default=-1)
parser.add_argument("-b", "--blue", help="blue color",
                    type=float, default=-1)
parser.add_argument(
    "-s",
    "--size", help="size of the image", type=int, default=2048)
parser.add_argument(
    "--bevel", help="bevel depth of the icon", type=float, default=1
)


def main():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else argv[1:]
    if len(argv) >= 1:
        args = parser.parse_args(argv)

        filepath = args.filepath
        rotate_x = args.rotate_x
        rotate_y = args.rotate_y
        rotate_z = args.rotate_z
        thickness = args.thickness
        distance = args.distance
        light_x = args.light_x
        light_y = args.light_y
        light_z = args.light_z
        light_strength = args.light_strength
        color_r = args.red
        color_g = args.green
        color_b = args.blue
        size = args.size
        bevel = args.bevel

        capture(
            filepath,
            rotate_x,
            rotate_y,
            rotate_z,
            thickness,
            bevel,
            distance,
            light_x,
            light_y,
            light_z,
            light_strength,
            color_r,
            color_g,
            color_b,
            size
        )
    else:
        parser.print_help()


def capture(
    filepath,
    rotate_x=0,
    rotate_y=0,
    rotate_z=0,
    thickness=1,
    bevel=1,
    distance=1,
    light_x=0,
    light_y=0,
    light_z=0,
    light_strength=1,
    color_r=-1,
    color_g=-1,
    color_b=-1,
    size=2048
):
    reset()

    bpy.ops.import_curve.svg(filepath=filepath)

    collection = bpy.data.collections[os.path.basename(filepath)]
    x, y, z, min_x, min_y, min_z = collection_dimensions(collection)

    for obj in collection.objects:
        obj.select_set(True)

    # scale up the objects
    factor = 1 / max(x, y, z)
    bpy.ops.transform.resize(value=(factor, factor, factor))

    # move the objects
    bpy.ops.transform.translate(
        value=(0, factor * (-0.5 * x - min_x), factor * (-0.5 * y - min_y)))

    # rotate the objects
    bpy.ops.transform.rotate(value=math.pi * -0.5 +
                             deg_to_rad(rotate_x), orient_axis="X")
    bpy.ops.transform.rotate(value=deg_to_rad(rotate_y), orient_axis="Y")
    bpy.ops.transform.rotate(value=math.pi * -0.5 +
                             deg_to_rad(rotate_z), orient_axis="Z")

    material = bpy.data.materials.new("Color")
    material.diffuse_color = (
        color_r if color_r != -1 else 1, color_g if color_g != -1 else 1, color_b if color_b != -1 else 1, 1)

    for obj in collection.objects:
        obj.data.extrude = thickness * 0.0005
        obj.data.bevel_depth = bevel * 0.0001
        if color_r != -1 or color_g != -1 or color_b != -1:
            obj.active_material = material

    #  add light
    bpy.ops.object.light_add(
        type="POINT", location=(light_x, light_y, light_z))
    bpy.data.objects["Point"].data.energy = light_strength * 10

    #  add camera
    bpy.ops.object.camera_add(
        location=(distance * 3, 0, 0), rotation=(math.pi*0.5, 0, math.pi*0.5))
    bpy.context.scene.camera = bpy.data.objects["Camera"]

    render(filepath.replace(".svg", ".png"), size)

    return


def log(any):
    keys = dir(any)
    for key in keys:
        attr = getattr(any, key)
        if not callable(attr):
            print("prop:", key, attr)
        else:
            print("func:", key)


def render(out=os.path.join(os.getcwd(), "out.png"), size=2048):
    bpy.context.scene.render.filepath = out
    bpy.context.scene.render.resolution_x = size
    bpy.context.scene.render.resolution_y = size
    bpy.context.scene.render.film_transparent = True
    bpy.ops.render.render(write_still=True)


def collection_dimensions(collection):
    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = float("-inf")

    for obj in collection.objects:
        min_x = min(min_x, obj.bound_box[0][0])
        min_y = min(min_y, obj.bound_box[0][1])
        min_z = min(min_z, obj.bound_box[0][2])
        max_x = max(max_x, obj.bound_box[6][0])
        max_y = max(max_y, obj.bound_box[6][1])
        max_z = max(max_z, obj.bound_box[6][2])

    x, y, z = max_x - min_x, max_y - min_y, max_z - min_z

    return x, y, z, min_x, min_y, min_z


def deg_to_rad(deg):
    return deg * math.pi / 180


def reset():
    for objs in (
            bpy.data.objects,
            bpy.data.meshes,
            bpy.data.cameras,
    ):
        for obj in objs:
            objs.remove(obj)

    for collections in (
            bpy.data.collections,
    ):
        for collection in collections:
            collections.remove(collection)


if __name__ == "__main__":
    main()
