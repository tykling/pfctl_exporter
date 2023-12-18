# type: ignore

import logging
from pfctl_exporter import PfctlCollector
from .samples import sample_info_output, sample_interfaces_output
logging.basicConfig(level=logging.DEBUG)



def test_parse_info_output(caplog) -> None:
    caplog.set_level(logging.DEBUG)
    c = PfctlCollector()
    print("collecting..")
    for _ in c.collect_info(mock_output=sample_info_output):
        pass
    assert (
        "found new Counter metric pfctl_state_table_searches with value 5165885"
        in caplog.text
    )
    assert (
        "found new Gauge metric pfctl_syncookies_highwater with value 25" in caplog.text
    )
