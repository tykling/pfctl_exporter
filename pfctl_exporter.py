from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
import time
from typing import Iterator, Union
import re
from prometheus_client.registry import Collector
from prometheus_client import start_http_server
import argparse
import logging
import subprocess
from importlib.metadata import PackageNotFoundError, version

# get version
try:
    __version__ = version("pfctl_exporter")
except PackageNotFoundError:
    # package is not installed, version unknown
    __version__ = "0.0.0"


class PfctlCollector(Collector):  # type: ignore
    """Custom Collector class which runs pfctl on each scrape."""

    def describe(self) -> list[str]:
        """This empty describe method is needed to avoid collect() being called on startup."""
        return []

    def collect(
        self, mock_output: Union[str, None] = None
    ) -> Iterator[Union[CounterMetricFamily, GaugeMetricFamily]]:
        """Run pfctl, parse output and yield metrics."""
        yield from self.collect_info()
        yield from self.collect_interfaces()
        yield from self.collect_rules()
        yield from self.collect_tables()
        yield GaugeMetricFamily(
            "up",
            "The value of this Gauge is always 1 when the pfctl_exporter is up",
            value=1,
        )

    def run_pfctl_command(self, cmd: list[str]) -> list[str]:
        """Run a pfctl command. Hardcode full path for now."""
        cmd.insert(0, "/sbin/pfctl")
        cmdstr = " ".join(cmd)
        logging.debug("Running '{cmdstr}' ...")
        # run without shell semantics
        proc = subprocess.run(cmd, text=True, capture_output=True)
        if proc.returncode != 0:
            logging.error(
                f"Running '{cmdstr}' failed with exit code {proc.returncode}, bailing out"
            )
            raise RuntimeError(f"running {cmdstr} failed")
        else:
            lines = proc.stdout.split("\n")
        logging.debug(f"returning {len(lines)} lines of output from pfctl")
        return lines

    def collect_info(
        self, mock_output: Union[list[str], None] = None
    ) -> Iterator[Union[CounterMetricFamily, GaugeMetricFamily]]:
        """Run pfctl -vvs info, parse output and return metrics."""
        cmd = ["-vvs", "info"]
        lines = mock_output or self.run_pfctl_command(cmd)
        logging.debug(f"got {len(lines)} lines of output from pfctl")
        header: str = ""
        # loop over lines in the output
        for line in lines:
            if not line:
                # skip empty lines
                continue
            if header == "" and line[:11] != "State Table":
                # still looking for the first header
                continue
            # header lines start from the line start, metrics start indented with two spaces
            if line[0:2] != "  ":
                # this is a header line
                if "Total             Rate" in line:
                    # this header needs some trimming
                    line = line[: line.find("  ")]
                header = line.strip().lower().replace(" ", "_")
                logging.debug(f"Found new header: '{header}'")
                continue
            elif line[0:2] == "  ":
                # this is a metric for the current header
                key, value = self.get_info_kv(line)
                if key is None or value is None:
                    logging.warning(
                        f"cannot parse metric for header '{header}', skipping line: '{line}'"
                    )
                    continue
                # replace illegal chars in the key
                key = key.replace(" ", "_").replace("-", "_")
                metric = f"pfctl_{header}_{key}"
                # pfctl returns mostly Counters but also a few Gauges,
                # the lines containing a Counter value ends in "/s"
                if line[-2:] == "/s":
                    # this is a Counter
                    logging.debug(
                        f"found new Counter metric {metric} with value {value}"
                    )
                    yield CounterMetricFamily(metric, metric, value=value)
                else:
                    # this is a Gauge
                    logging.debug(f"found new Gauge metric {metric} with value {value}")
                    yield GaugeMetricFamily(metric, metric, value=value)
            else:
                logging.warning(f"unknown line, skipping: {line}")
        logging.debug("no more lines, this is the end of collect()")

    def get_info_kv(self, line: str) -> Union[tuple[str, int], tuple[None, None]]:
        """Turn the string "  searches                         4994939            2.3/s" into the tuple ("searches", 4994939)."""
        m = re.match(r"  (?P<key>[a-z\- ]+?) +(?P<value>[0-9]+).*", line)
        if not m:
            logging.debug(f"no regex match for line: '{line}'")
            return None, None
        return str(m.group("key")), int(m.group("value"))

    def collect_interfaces(
        self, mock_output: Union[list[str], None] = None
    ) -> Iterator[Union[CounterMetricFamily, GaugeMetricFamily]]:
        """Run pfctl -vvs Interfaces, parse output and return metrics."""
        cmd = ["-vvs", "Interfaces"]
        lines = mock_output or self.run_pfctl_command(cmd)
        logging.debug(f"got {len(lines)} lines of output from 'pfctl -vvs Interfaces'")
        interface: str = ""

        # define metrics
        metrics: dict[str, Union[GaugeMetricFamily, CounterMetricFamily]] = {}
        metrics["cleared"] = GaugeMetricFamily(
            "pfctl_interface_cleared_timestamp_seconds",
            "Timestamp for when the counters for this interface were last reset",
            labels=["interface"],
        )
        metrics["references"] = GaugeMetricFamily(
            "pfctl_interface_ruleset_references",
            "The number of rules in the current pf ruleset referencing this interface",
            labels=["interface"],
        )
        metrics["counters_packets"] = CounterMetricFamily(
            "pfctl_interface_packets_total",
            "The number of packets on this interface aggregated by direction, family, and action",
            labels=["interface", "direction", "family", "action"],
        )
        metrics["counters_bytes"] = CounterMetricFamily(
            "pfctl_interface_bytes_total",
            "The number of bytes on this interface aggregated by direction, family, and action",
            labels=["interface", "direction", "family", "action"],
        )
        metrics["skip"] = GaugeMetricFamily(
            "pfctl_interface_skip",
            "This Gauge is 1 if filtering on the interface is disabled with 'set skip' or 0 if filtering is enabled on the interface",
            labels=["interface"],
        )

        # loop over lines in the output
        for line in lines:
            if not line:
                # skip empty lines
                continue

            # look for interface headers
            m = re.match(r"^(?P<interface>[a-z0-9.]+)(?P<skip> \(skip\))?$", line)
            if m:
                interface = m.group("interface")
                logging.debug(
                    f"found new interface: '{interface}' - getting metrics..."
                )
                if m.group("skip") is None:
                    # filtering is active on this interface
                    logging.debug('Adding new Gauge metric pfctl_interface_skip{interface="%s"} %s' % (interface, 0))
                    metrics["skip"].add_metric([interface], 0)
                else:
                    # this interface has "set skip"
                    logging.debug('Adding new Gauge metric pfctl_interface_skip{interface="%s"} %s' % (interface, 1))
                    metrics["skip"].add_metric([interface], 1)
                continue

            # look for References in a line like "	References:  27                "
            m = re.match(r"\tReferences:\s+(?P<references>\d+)\s*", line)
            if m:
                logging.debug(
                    'Adding new Gauge metric pfctl_interface_ruleset_references{interface="%s"} %s'
                    % (interface, m.group("references"))
                )
                metrics["references"].add_metric([interface], m.group("references"))
                continue

            # look for Cleared: in a line like "	Cleared:     Sun Nov 19 18:50:41 2023"
            m = re.match(r"\tCleared:\s+(?P<cleared>.+)", line)
            if m:
                cleared = int(
                    time.mktime(
                        time.strptime(m.group("cleared"), "%a %b %d %H:%M:%S %Y")
                    )
                )
                logging.debug(
                    'Adding new Gauge metric pfctl_interface_cleared_timestamp_seconds{interface="%s"} %s'
                    % (interface, cleared)
                )
                metrics["cleared"].add_metric([interface], cleared)
                continue

            # this should be a metrics line for the current interface in this format:
            # "	In4/Block:   [ Packets: 184339             Bytes: 29172941           ]"
            # where "In" can be "In" or "Out", "4" can be "4" or "6", and "Block" can be "Block" or "Pass"
            direction, family, action, packets, byts = self.parse_interface_metric(line)
            if direction is None:
                logging.warning(
                    f"cannot parse metric for interface '{interface}', skipping line: '{line}'"
                )
                continue
            logging.debug(
                'Adding new Counter metric: pfctl_interface_packets_total{interface="%s", direction="%s", family="%s", action="%s"} %s'
                % (interface, direction, family, action, packets)
            )
            metrics["counters_packets"].add_metric(
                [interface, direction, family, action], packets
            )
            metrics["counters_bytes"].add_metric(
                [interface, direction, family, action], byts
            )

        # done, yield everything
        for metric in metrics.values():
            yield metric

    def parse_interface_metric(
        self, line: str
    ) -> Union[tuple[str, str, str, int, int], tuple[None, None, None, None, None]]:
        """Parse a line of 'pfctl -vvs Interfaces' metrics output.

        Turn the string "	In4/Block:   [ Packets: 184339             Bytes: 29172941           ]" into
        a tuple of (direction, family, action, packets, bytes).
        """
        p = r"	(?P<direction>In|Out)(?P<family>4|6)\/(?P<action>Block|Pass): +\[ +Packets: +(?P<packets>[0-9]+) +Bytes: +(?P<bytes>[0-9]+) +\]"
        m = re.match(p, line)
        if not m:
            logging.debug(f"no regex match for line: '{line}'")
            return None, None, None, None, None
        return (
            str(m.group("direction")),
            f"ipv{m.group('family')}",
            str(m.group("action")),
            int(m.group("packets")),
            int(m.group("bytes")),
        )

    def collect_rules(
        self, mock_output: Union[list[str], None] = None
    ) -> Iterator[Union[CounterMetricFamily, GaugeMetricFamily]]:
        """Run pfctl -Pvs rules, parse output and return metrics."""
        cmd = ["-Pvs", "rules"]
        lines = mock_output or self.run_pfctl_command(cmd)
        logging.debug(f"got {len(lines)} lines of output from 'pfctl -Pvs rules'")

        # define metrics
        metrics: dict[str, Union[GaugeMetricFamily, CounterMetricFamily]] = {}
        for metric in ["evaluations", "packets", "bytes", "states"]:
            metrics[metric] = CounterMetricFamily(
                f"pfctl_rule_{metric}_total",
                "Total number of {metric} for this pf rule",
                labels=["rule"],
            )

        # loop over lines in the output
        for line in lines:
            if not line:
                # skip empty lines
                continue

            # look for interface headers
            m = re.match(r"^(?P<rule>[a-z]+.*)$", line)
            if m:
                rule = m.group("rule")
                logging.debug(f"found new rule: '{rule}' - getting metrics...")
                continue

            # find the metrics for this rule
            m = re.match(
                r"^  \[ Evaluations: (?P<evaluations>[0-9]+)\s+Packets: (?P<packets>[0-9]+)\s+Bytes: (?P<bytes>[0-9]+)\s+States: (?P<states>[0-9]+)\s+\]$",
                line,
            )
            if m:
                for metric in ["evaluations", "packets", "bytes", "states"]:
                    logging.debug(
                        'Adding new Counter metric: pfctl_rule_%s_total{rule="%s"} %s'
                        % (metric, rule, m.group(metric))
                    )
                    metrics[metric].add_metric([rule], m.group(metric))

        # done, yield everything
        for metric in metrics.values():
            yield metric

    def collect_tables(
        self, mock_output: Union[list[str], None] = None
    ) -> Iterator[Union[CounterMetricFamily, GaugeMetricFamily]]:
        """Run pfctl -vvs Tables, parse output and return metrics."""
        cmd = ["-vvs", "Tables"]
        lines = mock_output or self.run_pfctl_command(cmd)
        logging.debug(f"got {len(lines)} lines of output from 'pfctl -vvs Tables'")

        # define metrics
        metrics: dict[str, Union[GaugeMetricFamily, CounterMetricFamily]] = {}
        # table flags line like "--a-r-- prometheus6"
        for flag in [
            "constant",
            "persistent",
            "active",
            "inactive",
            "referenced",
            "hidden",
            "counters",
        ]:
            metrics[f"pfctl_table_flags_{flag}"] = GaugeMetricFamily(
                f"pfctl_table_flags_{flag}",
                f"Gauge set to 1 if this pf table has the {flag} flag, 0 if not.",
                labels=["table"],
            )
        # Addresses: line
        metrics["addresses"] = GaugeMetricFamily(
            "pfctl_table_addresses",
            "Total number of addresses in this pf table",
            labels=["table"],
        )
        # Cleared: line
        metrics["cleared"] = GaugeMetricFamily(
            "pfctl_table_cleared_timestamp_seconds",
            "Timestamp for when the counters for this table were last reset",
            labels=["table"],
        )
        # References: line
        metrics["references_anchors"] = GaugeMetricFamily(
            "pfctl_table_anchor_references",
            "The number of anchors in the current pf ruleset referencing this table",
            labels=["table"],
        )
        metrics["references_rules"] = GaugeMetricFamily(
            "pfctl_table_ruleset_references",
            "The number of rules in the current pf ruleset referencing this table",
            labels=["table"],
        )
        # Evaluations: line
        metrics["evaluations_nomatch"] = CounterMetricFamily(
            "pfctl_table_nomatch_evaluations",
            "The number of evaluations of this pf table resulting in a no-match",
            labels=["table"],
        )
        metrics["evaluations_match"] = CounterMetricFamily(
            "pfctl_table_match_evaluations",
            "The number of evaluations of this pf table resulting in a match",
            labels=["table"],
        )
        # counters
        metrics["counters_packets"] = CounterMetricFamily(
            "pfctl_table_packets_total",
            "The number of packets for this table aggregated by traffic direction and firewall action",
            labels=["table", "direction", "action"],
        )
        metrics["counters_bytes"] = CounterMetricFamily(
            "pfctl_table_bytes_total",
            "The number of bytes for this table aggregated by traffic direction and firewall action",
            labels=["table", "direction", "action"],
        )

        # loop over lines in the output
        for line in lines:
            if not line:
                # skip empty lines
                continue

            # look for table headers like "--a-r-- prometheus6"
            m = re.match(
                r"^(?P<constant>[c-])(?P<persistent>[p-])(?P<active>[a-])(?P<inactive>[i-])(?P<referenced>[r-])(?P<hidden>[h-])(?P<counters>[C-])\t(?P<table>[a-z0-9-_]+)$",
                line,
            )
            if m:
                table = m.group("table")
                logging.debug(
                    f"found new table: '{table}' - getting flags and metrics..."
                )
                for flag in [
                    "constant",
                    "persistent",
                    "active",
                    "inactive",
                    "referenced",
                    "hidden",
                    "counters",
                ]:
                    value = 0 if m.group(flag) == "-" else 1
                    # the value is - if the flag is not enabled and a letter if it is enabled
                    logging.debug(
                        'Adding new Gauge metric pfctl_table_flags_%s{table="%s"} %s'
                        % (flag, table, value)
                    )
                    metrics[f"pfctl_table_flags_{flag}"].add_metric([table], value)
                continue

            # look for Addresses: in a line like "	Addresses:   12"
            m = re.match(r"^\tAddresses:\s+(?P<addresses>[0-9]+)", line)
            if m:
                logging.debug(
                    'Adding new Gauge metric pfctl_table_addresses{table="%s"} %s'
                    % (table, m.group("addresses"))
                )
                metrics["addresses"].add_metric([table], m.group("addresses"))
                continue

            # look for Cleared: in a line like "	Cleared:     Sun Nov 19 18:50:41 2023"
            m = re.match(r"\tCleared:\s+(?P<cleared>.+)", line)
            if m:
                cleared = int(
                    time.mktime(
                        time.strptime(m.group("cleared"), "%a %b %d %H:%M:%S %Y")
                    )
                )
                logging.debug(
                    'Adding new Gauge metric pfctl_table_cleared_timestamp_seconds{table="%s"} %s'
                    % (table, cleared)
                )
                metrics["cleared"].add_metric([table], cleared)
                continue

            # look for References: line like "	References:  [ Anchors: 0                  Rules: 2                  ]"
            m = re.match(
                r"^\tReferences:\s+\[ Anchors: (?P<anchors>[0-9]+)\s+Rules: (?P<rules>[0-9]+)\s+\]$",
                line,
            )
            if m:
                logging.debug(
                    'Adding new Gauge metric pfctl_table_anchor_references{table="%s"} %s'
                    % (table, m.group("anchors"))
                )
                metrics["references_anchors"].add_metric([table], m.group("anchors"))
                logging.debug(
                    'Adding new Gauge metric pfctl_table_ruleset_references{table="%s"} %s'
                    % (table, m.group("rules"))
                )
                metrics["references_rules"].add_metric([table], m.group("rules"))

            # look for Evaluations: line like "	Evaluations: [ NoMatch: 0                  Match: 25                 ]"
            m = re.match(
                r"^\tEvaluations:\s+\[ NoMatch: (?P<nomatch>[0-9]+)\s+Match: (?P<match>[0-9]+)\s+\]$",
                line,
            )
            if m:
                logging.debug(
                    'Adding new Gauge metric pfctl_table_nomatch_evaluations{table="%s"} %s'
                    % (table, m.group("nomatch"))
                )
                metrics["evaluations_nomatch"].add_metric([table], m.group("nomatch"))
                logging.debug(
                    'Adding new Gauge metric pfctl_table_match_evaluations{table="%s"} %s'
                    % (table, m.group("match"))
                )
                metrics["evaluations_match"].add_metric([table], m.group("match"))

            # look for table counters like "	In/Pass:     [ Packets: 461268             Bytes: 57925850           ]"
            m = re.match(
                r"^\t(?P<direction>In|Out)/(?P<action>Block|Pass|XPass):\s+\[ Packets: (?P<packets>[0-9]+)\s+Bytes: (?P<bytes>[0-9]+)\s+\]",
                line,
            )
            if m:
                logging.debug(
                    'Adding new Counter metric pfctl_table_packets_total{table="%s", direction="%s", action="%s"} %s'
                    % (
                        table,
                        m.group("direction"),
                        m.group("action"),
                        m.group("packets"),
                    )
                )
                metrics["counters_packets"].add_metric(
                    [table, m.group("direction"), m.group("action")], m.group("packets")
                )
                logging.debug(
                    'Adding new Counter metric pfctl_table_bytes_total{table="%s", direction="%s", action="%s"} %s'
                    % (table, m.group("direction"), m.group("action"), m.group("bytes"))
                )
                metrics["counters_bytes"].add_metric(
                    [table, m.group("direction"), m.group("action")], m.group("bytes")
                )

        # done, yield everything
        for metric in metrics.values():
            yield metric


REGISTRY.register(PfctlCollector())


def main() -> None:
    """Parse arguments and start exporter."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--listen-ip",
        type=str,
        help="Listen IP. Defaults to 0.0.0.0 (all v4 IPs). Set to :: to listen on all v6 IPs.",
        default="0.0.0.0",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="Portnumber. Defaults to 9630.",
        default=9630,
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const="DEBUG",
        help="Debug mode.",
        default="INFO",
    )

    args = parser.parse_args()
    logging.basicConfig(
        level=args.loglevel,
        datefmt="%Y-%m-%d %H:%M:%S %z",
        format="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
    )
    logging.info(
        f"Starting pfctl_exporter v{__version__} - logging at level {args.loglevel}"
    )
    logging.info(
        f"Starting HTTP listener on address '{args.listen_ip}' port '{args.port}'"
    )
    start_http_server(addr=args.listen_ip, port=args.port)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
