import argparse
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        img = img.resize(size)
        img.save(output_path)

def crop_image(input_path, output_path, crop_box):
    with Image.open(input_path) as img:
        img = img.crop(crop_box)
        img.save(output_path)

def adjust_brightness(input_path, output_path, factor):
    with Image.open(input_path) as img:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(factor)
        img.save(output_path)

def adjust_contrast(input_path, output_path, factor):
    with Image.open(input_path) as img:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(factor)
        img.save(output_path)

def convert_to_grayscale(input_path, output_path):
    with Image.open(input_path) as img:
        img = ImageOps.grayscale(img)
        img.save(output_path)

def apply_filter(input_path, output_path, filter_type):
    with Image.open(input_path) as img:
        if filter_type == 'blur':
            img = img.filter(ImageFilter.BLUR)
        elif filter_type == 'sharpen':
            img = img.filter(ImageFilter.SHARPEN)
        elif filter_type == 'edge':
            img = img.filter(ImageFilter.FIND_EDGES)
        else:
            raise ValueError("Invalid filter type. Choose from 'blur', 'sharpen', 'edge'.")
        img.save(output_path)

def convert_format(input_path, output_path, format):
    with Image.open(input_path) as img:
        img.save(output_path, format=format)

def main():
    parser = argparse.ArgumentParser(description="Image processing toolkit")
    parser.add_argument('action', choices=['resize', 'crop', 'brightness', 'contrast', 'grayscale', 'filter', 'convert'], help="Action to perform on the image")
    parser.add_argument('input', help="Path to the input image file")
    parser.add_argument('output', help="Path to the output image file")
    parser.add_argument('--size', nargs=2, type=int, help="Size for resizing (width height)")
    parser.add_argument('--crop', nargs=4, type=int, help="Crop box (left top right bottom)")
    parser.add_argument('--brightness', type=float, help="Brightness factor (e.g., 1.5 for 50% brighter)")
    parser.add_argument('--contrast', type=float, help="Contrast factor (e.g., 1.5 for 50% more contrast)")
    parser.add_argument('--filter', choices=['blur', 'sharpen', 'edge'], help="Filter type to apply")
    parser.add_argument('--format', help="Format to convert the image to (e.g., PNG, JPEG)")

    args = parser.parse_args()

    if args.action == 'resize':
        if not args.size:
            print("Size is required for resizing")
            return
        resize_image(args.input, args.output, tuple(args.size))

    elif args.action == 'crop':
        if not args.crop:
            print("Crop box is required for cropping")
            return
        crop_image(args.input, args.output, tuple(args.crop))

    elif args.action == 'brightness':
        if args.brightness is None:
            print("Brightness factor is required")
            return
        adjust_brightness(args.input, args.output, args.brightness)

    elif args.action == 'contrast':
        if args.contrast is None:
            print("Contrast factor is required")
            return
        adjust_contrast(args.input, args.output, args.contrast)

    elif args.action == 'grayscale':
        convert_to_grayscale(args.input, args.output)

    elif args.action == 'filter':
        if not args.filter:
            print("Filter type is required")
            return
        apply_filter(args.input, args.output, args.filter)

    elif args.action == 'convert':
        if not args.format:
            print("Format is required for conversion")
            return
        convert_format(args.input, args.output, args.format)

if __name__ == '__main__':
    main()
