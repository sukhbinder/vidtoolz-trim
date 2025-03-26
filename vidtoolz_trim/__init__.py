import vidtoolz
import subprocess
import os


def determine_output_path(input_file, output_file):
    input_dir, input_filename = os.path.split(input_file)
    name, _ = os.path.splitext(input_filename)

    if output_file:
        output_dir, output_filename = os.path.split(output_file)
        if not output_dir:  # If no directory is specified, use input file's directory
            return os.path.join(input_dir, output_filename)
        return output_file
    else:
        return os.path.join(input_dir, f"{name}_trim.mp4")


def get_seconds(ts):
    secs = sum(int(x) * 60**i for i, x in enumerate(reversed(ts.split(":"))))
    return secs


def trim_by_ffmpeg(inputfile, starttime, endtime, outputfile, duration=None):
    if isinstance(starttime, str):
        if ":" in starttime:
            starttime = get_seconds(starttime)
    if isinstance(endtime, str):
        if ":" in endtime:
            endtime = get_seconds(endtime)

    if duration is not None:
        cmdline = "ffmpeg -y -ss {starttime:0.4f} -i {inputfile} -t {duration:0.4f} -c copy {outputfile}".format(
            starttime=float(starttime),
            inputfile=inputfile,
            duration=float(duration),
            outputfile=outputfile,
        )
    else:
        cmdline = "ffmpeg -y -ss {starttime:0.4f} -i {inputfile} -to {endtime:0.4f} -map 0 -vcodec copy -acodec copy  {outputfile}".format(
            starttime=float(starttime),
            inputfile=inputfile,
            endtime=float(endtime),
            outputfile=outputfile,
        )
    cmdlist = cmdline.split()
    iret = subprocess.call(cmdlist)
    return iret


def trim_video(input_file, output_file, start_time, end_time):
    try:
        # Check if the input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found.")

        # Ensure start time and end time are valid
        if start_time < 0 or end_time <= start_time:
            raise ValueError(
                "Invalid time range: 'start_time' should be non-negative and less than 'end_time'."
            )

        # Define the FFmpeg command
        command = [
            "ffmpeg",
            "-i",
            input_file,
            "-ss",
            str(start_time),
            "-to",
            str(end_time),
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            output_file,
        ]

        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True)

        # Check for errors during FFmpeg execution
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")

        print(f"Video trimmed successfully! Output saved to '{output_file}'.")

    except FileNotFoundError as fnfe:
        print(f"Error: {fnfe}")
    except ValueError as ve:
        print(f"Error: {ve}")
    except RuntimeError as re:
        print(f"Error: {re}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def create_parser(subparser):
    parser = subparser.add_parser("trim", description="Trim video using ffmpeg")
    parser.add_argument("inputfile", type=str, help="Single file name")
    parser.add_argument("-st", "--starttime", type=float, help="Start time in the s")
    parser.add_argument("-et", "--endtime", type=float, help="End time in the s")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file (default: %(default)s)",
        default=None,
    )
    # parser.add_argument(
    #     "-d",
    #     "--duration",
    #     type=float,
    #     help="Duration time in seconds (default: %(default)s)",
    #     default=None,
    # )

    return parser


class ViztoolzPlugin:
    """Trim video using ffmpeg"""

    __name__ = "trim"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        iret = trim_by_ffmpeg(
            args.inputfile, args.starttime, args.endtime, args.outputfile, args.duration
        )
        print("{} created.".format(args.outputfile))

    def hello(self, args):
        # this routine will be called when "vidtoolz "trim is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


trim_plugin = ViztoolzPlugin()
