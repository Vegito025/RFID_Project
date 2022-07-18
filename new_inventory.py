from __future__ import print_function, division
import time
import logging
import pprint
from twisted.internet import reactor, defer
import os

from sllurp.util import monotonic
from sllurp.llrp import LLRPClientFactory

start_time = None

numtags = 0
logger = logging.getLogger(__name__)


def tag_report_cb(llrp_msg):
    """Function to run each time the reader reports seeing tags."""
    global numtags
    tags = llrp_msg.msgdict['RO_ACCESS_REPORT']['TagReportData']
    if len(tags):
        for i in tags:
            print('saw tag(s): %s', i)
        for tag in tags:
            numtags += tag['TagSeenCount'][0]
    else:
        print("no tag seen")
    reactor.stop()

def main():
    global start_time
    fac = LLRPClientFactory(
        reconnect=True,
        tag_content_selector={
            'EnableROSpecID': False,
            'EnableSpecIndex': False,
            'EnableInventoryParameterSpecID': False,
            'EnableAntennaID': True,
            'EnableChannelIndex': True,
            'EnablePeakRSSI': False,
            'EnableFirstSeenTimestamp': True,
            'EnableLastSeenTimestamp': True,
            'EnableTagSeenCount': True,
            'EnableAccessSpecID': False
        })

    # tag_report_cb will be called every time the reader sends a TagReport
    # message (i.e., when it has "seen" tags).
    fac.addTagReportCallback(tag_report_cb)

    reactor.connectTCP("10.240.0.35", 5084, fac, timeout=3)

    reactor.run()

main()
