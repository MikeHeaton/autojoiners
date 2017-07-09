import argparse

import autojoiners_framesource as aj_framesource
import autojoiners_imagesource as aj_imagesource
import autojoiners_shatter as aj_shatter
import autojoiners_canvas as aj_canvas


DEFAULT_SIZE = ['800', '600']
DEFAULT_NREGIONS = 100
DEFAULT_SHATTER = 'Voroi'
DEFAULT_OUTPUTFILE = 'output'
DEFAULT_BORDERSIZE = [0, 0]

# For the following, no values with duplicated prefixes!
ALLOWED_INPUT_MODES_AND_ARGS = {
           'webcam': (aj_framesource.FramesFromWebcam,
                      []),
           'file': (aj_framesource.FramesFromVideo,
                    ['input_filename'])
           }

ALLOWED_SHATTERS_AND_ARGS = {
            'Voroi': (aj_shatter.VoroiShatter,
                      ['size', 'nregions']),
            'HockneySquares': (aj_shatter.RegularSquareShatter,
                               ['size', 'nregions']),
            'RandQuadrilaterals': (aj_shatter.RandQuadrilateralShatter,
                                   ['size', 'nregions']),
            'RandRectangles': (aj_shatter.RandRectangleShatter,
                               ['size', 'nregions'])
           }


def setup_argparser():
    parser = argparse.ArgumentParser(description="Create a joiner image")

    abbreviated_modes = [s[:i+1] for s in ALLOWED_INPUT_MODES_AND_ARGS
                         for i in range(len(s))]
    parser.add_argument('raw_mode', choices=abbreviated_modes)
    parser.add_argument('input_filename', nargs='?',
                        default=None)
    parser.add_argument('-size', action='store', nargs=2,
                        default=DEFAULT_SIZE)
    parser.add_argument('-nregions', action='store',
                        default=DEFAULT_NREGIONS, type=int)
    parser.add_argument('-pertubation', action='store',
                        default=0, type=int)
    parser.add_argument('-shatter', action='store', dest='raw_shatter',
                        default=DEFAULT_SHATTER, type=str)
    parser.add_argument('-filename', action='store', dest='output_filename',
                        default=DEFAULT_OUTPUTFILE, type=str)
    parser.add_argument('-border', action='store', nargs=2,
                        default=DEFAULT_BORDERSIZE,  dest='border_size')

    return parser


def clean_check_args(args,
                     allowed_input_modes=ALLOWED_INPUT_MODES_AND_ARGS,
                     allowed_shatters=ALLOWED_SHATTERS_AND_ARGS):

    def _sanitise_mode(args):
        mode = autocomplete(args.raw_mode, allowed_input_modes)

        if mode is None:
            raise ValueError("Invalid input mode.")

        if mode == 'webcam' and args.input_filename is not None:
            raise ValueError("Filename supplied with mode 'webcam'.")
        if mode == 'file' and args.input_filename is None:
            raise ValueError("No filename supplied.")
        return mode

    def _sanitise_size(args):
        try:
            size = [int(i) for i in args.size]
        except ValueError:
            raise ValueError("Invalid size passed to -size.")
        return size

    def _sanitise_nregions(args):
        if args.nregions <= 0:
            raise ValueError("Invalid value passed to -nregions.")
        return args.nregions

    def _sanitise_pertubation(args):
        if args.pertubation < 0:
            raise ValueError("Invalid value passed to -pertubation.")
        return args.pertubation

    def _sanitise_border(args):
        try:
            border = [int(i) for i in args.border_size]
        except ValueError:
            raise ValueError("Invalid size passed to -border.")
        return border

    def _sanitise_shatter(args):
        shatter = autocomplete(args.raw_shatter, allowed_shatters)
        if shatter is None:
            raise ValueError("Invalid shatter supplied." +
                             " Choices are:\n{}".format(allowed_shatters.keys()))
        return shatter

    new_args = {"mode": _sanitise_mode(args),
                "input_filename": args.input_filename,
                "output_filename": args.output_filename,
                "size": _sanitise_size(args),
                "pertubation": _sanitise_pertubation(args),
                "nregions": _sanitise_nregions(args),
                "shatter": _sanitise_shatter(args),
                "border_size": _sanitise_border(args)}

    return new_args


def autocomplete(value, argumentslist):
    for arg in argumentslist:
        if arg.startswith(value):
            return arg
    return None

def create_object_from_recipe(arg_name, all_args):

    if arg_name == "mode":
        recipe_book = ALLOWED_INPUT_MODES_AND_ARGS
    elif arg_name == "shatter":
        recipe_book = ALLOWED_SHATTERS_AND_ARGS
    else:
        raise ValueError("invalid arg_name passed to create_object_from_recipe")

    obj_creator, obj_args = recipe_book[all_args[arg_name]]
    obj = obj_creator(**{i: all_args[i] for i in obj_args})
    return obj

def args_from_input():
    parser = setup_argparser()
    args = parser.parse_args()
    args = clean_check_args(args)
    return args

if __name__ == "__main__":
    args = args_from_input()

    print("Creating face with the following params:\n{}".format(args))

    framesource = create_object_from_recipe('mode', args)
    imagesource = aj_imagesource.FacesFromVideo(
                                    framesource,
                                    pertubation=args['pertubation'],
                                    border=args['border_size'])
    shatter = create_object_from_recipe('shatter', args)
    canvas = aj_canvas.JoinerCanvas(args['size'], shatter,
                                    imagesource, args['output_filename'])

    canvas.create_canvas()
    canvas.show_save_canvas()
