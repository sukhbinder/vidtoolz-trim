import vidtoolz
import subprocess


def get_seconds(ts):
    secs = sum(int(x) * 60 ** i for i, x in enumerate(reversed(ts.split(":"))))
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


def create_parser(subparser):
    parser = subparser.add_parser("trim", description="Trim video using ffmpeg")
    parser.add_argument("inputfile", type=str, help="Single file name")
    parser.add_argument(
        "-st", "--starttime", type=str, help="Start time in the format hh:mm:ss"
    )
    parser.add_argument(
        "-et", "--endtime", type=str, help="End time in the format hh:mm:ss"
    )
    parser.add_argument(
        "-o",
        "--outputfile",
        type=str,
        help="Output file (default: %(default)s)",
        default="output.mp4",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=float,
        help="Duration time in seconds (default: %(default)s)",
        default=None,
    )

    return parser


class ViztoolzPlugin:
    """ Trim video using ffmpeg """

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
