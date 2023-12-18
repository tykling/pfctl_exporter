# type: ignore

import logging
from pfctl_exporter import PfctlCollector

logging.basicConfig(level=logging.DEBUG)

sample_output = """Status: Enabled for 25 days 16:23:32          Debug: Urgent

Hostid:   0x68d01842
Checksum: 0x1d921dc03c175342eebc265ff2573361

State Table                          Total             Rate
  current entries                        2               
  searches                         5165885            2.3/s
  inserts                            94115            0.0/s
  removals                           94113            0.0/s
Source Tracking Table
  current entries                        0               
  searches                               0            0.0/s
  inserts                                0            0.0/s
  removals                               0            0.0/s
Counters
  match                            3177960            1.4/s
  bad-offset                             0            0.0/s
  fragment                               0            0.0/s
  short                                  0            0.0/s
  normalize                              0            0.0/s
  memory                                 0            0.0/s
  bad-timestamp                          0            0.0/s
  congestion                             0            0.0/s
  ip-option                              0            0.0/s
  proto-cksum                            0            0.0/s
  state-mismatch                         0            0.0/s
  state-insert                           0            0.0/s
  state-limit                            0            0.0/s
  src-limit                              0            0.0/s
  synproxy                               0            0.0/s
  map-failed                             0            0.0/s
Limit Counters
  max states per rule                    0            0.0/s
  max-src-states                         0            0.0/s
  max-src-nodes                          0            0.0/s
  max-src-conn                           0            0.0/s
  max-src-conn-rate                      0            0.0/s
  overload table insertion               0            0.0/s
  overload flush states                  0            0.0/s
  synfloods detected                     0            0.0/s
  syncookies sent                        0            0.0/s
  syncookies validated                   0            0.0/s
Syncookies
  mode                      never
  active                    inactive
  highwater                 25 %
  lowwater                  12 %
  halfopen states           0
"""


def test_parse_output(caplog) -> None:
    caplog.set_level(logging.DEBUG)
    c = PfctlCollector()
    print("collecting..")
    for _ in c.collect(mock_output=sample_output):
        pass
    assert (
        "found new Counter metric pfctl_state_table_searches with value 5165885"
        in caplog.text
    )
    assert (
        "found new Gauge metric pfctl_syncookies_highwater with value 25" in caplog.text
    )
