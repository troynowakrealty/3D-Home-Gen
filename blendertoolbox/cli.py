import argparse


def main(argv=None):
    """Command-line interface for BlenderToolbox rendering."""
    parser = argparse.ArgumentParser(
        description="Render a mesh with Blender Toolbox")
    parser.add_argument(
        "mesh",
        help="Path to mesh file (.obj, .ply, etc.)")
    parser.add_argument(
        "-o",
        "--output",
        default="render.png",
        help="Output image path")
    args = parser.parse_args(argv)

    import blendertoolbox as bt

    arguments = {
        "output_path": args.output,
        "image_resolution": [720, 720],
        "number_of_samples": 200,
        "mesh_path": args.mesh,
        "mesh_position": (1.12, -0.14, 0),
        "mesh_rotation": (90, 0, 227),
        "mesh_scale": (1.5, 1.5, 1.5),
        "shading": "smooth",
        "subdivision_iteration": 0,
        "mesh_RGB": [144.0 / 255, 210.0 / 255, 236.0 / 255],
        "light_angle": (6, -30, -155),
    }

    bt.render_mesh_default(arguments)


if __name__ == "__main__":
    main()
