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
        if mock_output:
            logging.debug("NOT running 'pfctl -vvs info', using mock_output instead")
            lines = mock_output.split("\n")
        else:
            logging.debug("Running 'pfctl -vvs info' ...")
            proc = subprocess.run(
                ["pfctl", "-vvs", "info"], text=True, capture_output=True
            )
            lines = proc.stdout.split("\n")
            # TODO: error handling if pfctl fails somehow
        header: str = ""
        # loop over lines in the output
        for line in lines:
            while header == "" and line[:11] != "State Table":
                # still looking for the first header
                continue
            # header lines start from the line start, metrics start with two spaces
            if line[0:2] != "  ":
                # this is a header
                header = line.strip().lower().replace(" ", "_")
                logging.debug(f"Found new header {header}")
                continue
            elif line[0:2] == "  ":
                # this is a metric for the current header
                key, value = self.get_kv(line)
                if not all([key, value]):
                    logging.warning(
                        f"cannot parse metric for header {header}, skipping line: {line}"
                    )
                    continue
                key = f"{header}_{key}"
                logging.debug(f"found new metric {key} with value {value}")
                # pfctl returns mostly Counters but also a few Gauges,
                # the lines containing a Counter value ends in "/s"
                if line[-2:] == "/s":
                    # this is a Counter
                    yield CounterMetricFamily(key, key, value=value)
                else:
                    # this is a Gauge
                    yield GaugeMetricFamily(key, key, value=value)
            else:
                logging.warning(f"unknown line, skipping: {line}")
        logging.debug("no more lines, this is the end of collect()")

    def get_kv(self, line: str) -> Union[tuple[str, int], tuple[None, None]]:
        """Turn the string "  searches                         4994939            2.3/s" into the tuple ("searches", 4994939)."""
        m = re.match(f"\s{2}(?P<key>[a-z-\s]+)\s+(?P<value>\d+).*", line)
        if not m:
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
