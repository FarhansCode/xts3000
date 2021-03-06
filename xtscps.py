#!/usr/bin/env python3


import os
import sys
from binascii import b2a_hex

import xtscontroller
import sbep

def print_results(options, xts):
    ''' Print Results table '''
    for v in xts.radiovalues:
        print("%s:\t\t%s" % (v, xts.radiovalues[v]))

def main():
    ''' Main Function '''
    options = options_parse()

    xts = xtscontroller.xtscontroller()
    xts.initialize(options.devfile)

#    b = xts.device.read(size=1)
#    if b != sbep.ACK:
#        print("Error 3: ACK not received")
#        sys.exit()

    print("Get Device info")
    xts.get_deviceinfo()
    xts.loadmap()
    xts.get_all_settings()

    if options.printmap:
        pass
    if options.memdump:
        xts.memdump()
        
    print_results(options, xts)

def options_parse():
    ''' Parse the cmdline options '''
    usage = "usage: %prog [-d] | [-i] [[--memdump]"
    version = "Currently not versioned"

    from optparse import OptionParser
    from optparse import OptionGroup

    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-d", "--device", dest="devfile", type="string",
                      help="Device File ie. /dev/ttyUSB0")

    group = OptionGroup(parser, "Retrieve Device Information")
    group.add_option("-i", dest="deviceinfo", help="Device Information", action="store_true")
    parser.add_option_group(group)

    group = OptionGroup(parser, "Write to Device")
    group.add_option("-w", "--write", dest="write", type="string", help="Unimplemented")
    parser.add_option_group(group)

    group = OptionGroup(parser, "Debug")
    group.add_option("--memdump", dest="memdump", action="store_true",
                     help="Dump the full memory")
    group.add_option("--printmap", dest="printmap", action="store_true",
                     help="Print memory map from maps file")
    parser.add_option_group(group)

    (options, args) = parser.parse_args()

    if not options.devfile:
        parser.error("Must specify device file with -d/--device")
    if options.write:
       parser.error("This is currently not implemented. Exiting.")
    if not options.memdump and not options.printmap and not options.deviceinfo:
        parser.error("You specified a device, but not what command to execute")

    (options, args) = parser.parse_args()
    return options

if __name__ == "__main__":
    main()
