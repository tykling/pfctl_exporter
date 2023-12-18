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
        """This empty describe method is needed for to avoid collect() being called on startup."""
        return []

    def collect(
        self, mock_output: Union[str, None] = None
    ) -> Iterator[Union[CounterMetricFamily, GaugeMetricFamily]]:
        """Run pfctl, parse output and return metrics."""
        cmd = ["pfctl", "-vvs", "info"]
        cmdstr = " ".join(cmd)
        if mock_output:
            logging.debug(f"NOT running '{cmdstr}', using mock_output instead")
            lines = mock_output.split("\n")
        else:
            logging.debug("Running '{cmdstr}' ...")
            proc = subprocess.run(cmd, text=True, capture_output=True)
            if proc.returncode != 0:
                logging.error(
                    f"Running '{cmdstr}' failed with exit code {proc.returncode}, bailing out"
                )
                raise RuntimeError(f"running {cmdstr} failed")
            else:
                logging.debug("pfctl returned something, checking it...")
                lines = proc.stdout.split("\n")
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
                key, value = self.get_kv(line)
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

    def get_kv(self, line: str) -> Union[tuple[str, int], tuple[None, None]]:
        """Turn the string "  searches                         4994939            2.3/s" into the tuple ("searches", 4994939)."""
        m = re.match(r"  (?P<key>[a-z\- ]+?) +(?P<value>[0-9]+).*", line)
        if not m:
            logging.debug(f"no regex match for line: '{line}'")
            return None, None
        return str(m.group("key")), int(m.group("value"))


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
