import autojoiners_framesource as aj_framesource
import autojoiners_imagesource as aj_imagesource
import autojoiners_shatter as aj_shatter
import autojoiners_canvas as aj_canvas
import autojoiner_io as aj_io

if __name__ == "__main__":
    parser = aj_io.setup_argparser()

    args = parser.parse_args()
    args = aj_io.clean_check_args(args)
    print("Creating face with the following params:\n{}".format(args))

    framesource = aj_io.create_object_from_recipe(
                                    'mode', args)
    imagesource = aj_imagesource.RawImages(
                                    framesource
                                    )
    shatter = aj_io.create_object_from_recipe(
                                    'shatter', args)
    canvas = aj_canvas.JoinerCanvas(args['size'], shatter,
                                    imagesource, args['output_filename'])

    canvas.create_canvas()
    canvas.show_save_canvas()
