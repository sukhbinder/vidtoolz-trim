import vidtoolz
import subprocess
import os
from moviepy.tools import convert_to_seconds


def format_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def get_length(filename):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return float(result.stdout)


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

        if os.path.exists(output_file):
            os.remove(output_file)

        # check if endtime is -1 that is till the end
        if end_time == -1:
            end_time = get_length(input_file)

        # convert time and end
        start_time = convert_to_seconds(start_time)
        end_time = convert_to_seconds(end_time)
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
            "libx264",
            "-c:a",
            "aac",
            output_file,
        ]

        # Re-encode for Precise Cuts
        # ffmpeg -i input.mov -ss 00:00:05 -to 00:00:10 -c:v libx264 -c:a aac output.mov

        #  MOV-Specific Considerations
        # ffmpeg -i input.mov -map 0 -map_metadata -1 -c copy output.mov

        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True)

        # Check for errors during FFmpeg execution
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")

    except FileNotFoundError as fnfe:
        print(f"Error: {fnfe}")
    except ValueError as ve:
        print(f"Error: {ve}")
    except RuntimeError as re:
        print(f"Error: {re}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return output_file


def create_parser(subparser):
    parser = subparser.add_parser("trim", description="Trim video using ffmpeg")
    parser.add_argument("input", type=str, help="Single file name")
    parser.add_argument(
        "-st",
        "--starttime",
        default=0,
        type=str,
        help="Start time in the seconds or in format 1:23 (default: %(default)s)",
    )
    parser.add_argument(
        "-et",
        "--endtime",
        default=-1,
        type=str,
        help="End time in the seconds or in format 1:23 (default: %(default)s)",
    )
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
        output = determine_output_path(args.input, args.output)
        outputfile = trim_video(args.input, output, args.starttime, args.endtime)
        print("{} created.".format(outputfile))

    def hello(self, args):
        # this routine will be called when "vidtoolz "trim is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


trim_plugin = ViztoolzPlugin()
