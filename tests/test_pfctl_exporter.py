# type: ignore

import logging
from pfctl_exporter import PfctlCollector
from .samples import (
    sample_info_output,
    sample_interfaces_output,
    sample_rules_output,
    sample_tables_output,
)

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
        'Adding new Gauge metric pfctl_interface_cleared_timestamp_seconds{interface="em0.7"} 1700416241'
        in caplog.text
    )


def test_parse_rules_output(caplog) -> None:
    caplog.set_level(logging.DEBUG)
    c = PfctlCollector()
    for _ in c.collect_rules(mock_output=sample_rules_output.split("\n")):
        pass
    assert (
        'Adding new Counter metric: pfctl_rule_bytes_total{rule="pass in quick on em0.7 proto tcp from <prometheus6> to <nuc2> port = 9999 flags S/SA keep state"} 33758359'
        in caplog.text
    )


def test_parse_tables_output(caplog) -> None:
    caplog.set_level(logging.DEBUG)
    c = PfctlCollector()
    for _ in c.collect_tables(mock_output=sample_tables_output.split("\n")):
        pass
    assert (
        'Adding new Gauge metric pfctl_table_addresses{table="allowssh"} 12'
        in caplog.text
    )
    assert (
        'Adding new Gauge metric pfctl_table_cleared_timestamp_seconds{table="allowssh"} 1700416241'
        in caplog.text
    )
    assert (
        'Adding new Gauge metric pfctl_table_flags_persistent{table="portknock"} 1'
        in caplog.text
    )
    assert (
        'Adding new Counter metric pfctl_table_bytes_total{table="portknock", direction="Out", action="Pass"} 830514949'
        in caplog.text
    )
