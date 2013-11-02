__author__ = 'Dima'
import logging
import tornado
from subprocess import Popen, PIPE, check_call
from tornado.options import define, options

define("command", default="gphoto2", help="Command to execute for gphoto", type=str)


class ShutterSpeedController(object):

    shutter_speeds = {}

    def __init__(self, config):
        self.init_shutter_speeds(config["shutter"])

    def init_shutter_speeds(self, file):
        logging.info("Opening file <%s>", file)
        with open(file, "r") as f:
            line_arr = f.readline().split()
            if line_arr[0] == "Choice:":
                logging.info("Adding speed %s with index %s", line_arr[2], line_arr[1])
                self.shutter_speeds[int(line_arr[2])] = line_arr[1]

    def get_current_speed_index(self):
        p1 = Popen([options.command, "--get-config", "/main/capturesettings/shutterspeed"], stdout=PIPE)
        p2 = Popen(["grep", "Current:"], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()
        output = p2.communicate()[0].decode("UTF-8")
        logging.info("Output : <%s>", output)
        current_value = output.split()[1]
        logging.info("Parsed current value as : <%s>", current_value)
        res = self.shutter_speeds[current_value]
        logging.info("Matching index is : %d", res)
        return res

    @staticmethod
    def set_shutter_speed_index(index):
        logging.info("Setting shutter speed index to %i", index)
        #check_call([options.command, "--set-config-index", "/main/capturesettings/shutterspeed="+str(index)])

    @staticmethod
    def capture_image():
        logging.info("Capturing image.")
        #check_call([options.command, "--capture-image"])

    def bracket(self, steps):
        cur_index = self.get_current_speed_index()
        for i in range(cur_index-steps, cur_index+steps+1):
            self.set_shutter_speed_index(i)
            self.capture_image()
        self.set_shutter_speed_index(cur_index)


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("Starting main in Controller")
    tornado.options.parse_command_line()
    controller = ShutterSpeedController({"shutter": "capture_speed.list"})
    controller.bracket(3)


if __name__ == "__main__":
    main()
