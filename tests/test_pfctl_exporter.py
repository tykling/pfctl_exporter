# type: ignore

import logging
from pfctl_exporter import PfctlCollector
from .samples import sample_info_output, sample_interfaces_output

logging.basicConfig(level=logging.DEBUG)


def test_parse_info_output(caplog) -> None:
    caplog.set_level(logging.DEBUG)
    c = PfctlCollector()
    for _ in c.collect_info(mock_output=sample_info_output.split("\n")):
        pass
    assert (
        "found new Counter metric pfctl_state_table_searches with value 5165885"
        in caplog.text
    )
    assert (
        "found new Gauge metric pfctl_syncookies_highwater with value 25" in caplog.text
    )


def test_parse_interfaces_output(caplog) -> None:
    caplog.set_level(logging.DEBUG)
    c = PfctlCollector()
    for _ in c.collect_interfaces(mock_output=sample_interfaces_output.split("\n")):
        pass
    assert "got 67 lines of output from 'pfctl -vvs Interfaces'" in caplog.text
    assert "found new interface: 'em0.3' - getting metrics..." in caplog.text
    assert (
        'Adding new Gauge metric pfctl_interfaces_cleared_timestamp_seconds{interface="em0.7"} 1700416241'
        in caplog.text
    )
