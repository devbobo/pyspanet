"""Main entry."""

import asyncio
import logging
import sys

from pyspanet import SpaMicroClient, SpaMicroConfig
from pyspanet.collections import (
        DateTimeDict,
        FiltrationDict,
        HeatPumpDict,
        PowerSaveDict,
        SleepDict,
        TimeCodedInteger
    )


def usage() -> None:
    """Print uage instructions."""
    print(f"Usage: {sys.argv[0]} <uart> <baudrate> <flag>")
    print("\tuart:\tUART id (required)")
    print("\tbaudrate:\tBaud rate (required)")
    print("\t-d, --debug:\tenable debug logs (optional)")


async def dump_data(data: SpaMicroConfig) -> None:
    """ dump_data """
    print("******** Testing spa connection and configuration **********")

    async with SpaMicroClient(data) as spa:
        if spa.data.device is not None:
            print()
            print("======================================")
            print('DEVICE:')
            print("--------------------------------------")
            for k, v in spa.data.device.items():
                print(f"{k.title()}     \t{v}")

        if spa.data.state is not None:
            print()
            print("======================================")
            print('STATUS:')
            print("--------------------------------------")
            for k, v in spa.data.state.items():
                print(f"{k.title()}      \t{v.name}")

        if spa.data.pumps is not None:
            print()
            print("======================================")
            print('PUMPS:')
            print("--------------------------------------")
            for k, v in spa.data.pumps.items():
                for k1, v1 in v.items():
                    if v1 is None:
                        continue
                    print(
                        "{label}\t{key}      \t{value}".format(
                            label='Pump ' + k[-1] if k1 == 'installed' else '',
                            key=k1.title(),
                            value=v1.name
                        )
                    )
                print()

        if spa.data.blower is not None:
            print("======================================")
            print('BLOWER:')
            print("--------------------------------------")
            for k, v in spa.data.blower.items():
                print(
                    "{key}    \t{value}\t".format(
                        key=k.title(),
                        value=v
                        if v.name.startswith('LEVEL_')
                        else v.name
                    )
                )

        if spa.data.lights is not None:
            print()
            print("======================================")
            print('LIGHTS:')
            print("--------------------------------------")
            for k, v in spa.data.lights.items():
                print(
                    "{key}    \t{value}\t".format(
                        key=k.title(),
                        value=v
                        if v.name.startswith('LEVEL_')
                        else v.name
                    )
                )

        if spa.data.temperature is not None:
            print()
            print("======================================")
            print('TEMPERATURE:')
            print("--------------------------------------")
            for k, v in spa.data.temperature.items():
                print(f"{k.title()} \t\t{v}")

        if spa.data.settings is not None:
            print()
            print("======================================")
            print('SETTINGS:')
            print("--------------------------------------")
            for k, v in spa.data.settings.items():
                if isinstance(v, DateTimeDict):
                    print(f"Date Time\tDate\t{v.day} {v.month.name.title()} {v.year}")
                    print(f"\t\tTime\t{v.hours}:{v.minutes}:{v.seconds}")
                    print()
                elif isinstance(v, FiltrationDict):
                    print(f"Filtration\tCycle\t{v.cycle}")
                    print(f"\t\tRuntime\t{v.runtime}")
                    print()
                elif isinstance(v, HeatPumpDict):
                    print(f"Heat Pump\tBoost\t{v.boost.name}")
                    print(f"\t\tMode\t{v.mode.name}")
                    print()
                elif isinstance(v, PowerSaveDict):
                    print(f"Power Save\tState\t{v.state.name}")
                    print(f"\t\tPeak\tStart\t{v.peak.start}")
                    print(f"\t\t\tStop\t{v.peak.stop}")
                    print()
                elif isinstance(v, SleepDict):
                    print(f"Sleep\t\tTimer1\tState\t{v.timer1.state.name}")
                    print(f"\t\t\tStart\t{v.timer1.start}")
                    print(f"\t\t\tStop\t{v.timer1.stop}")
                    print(f"\t\tTimer2\tState\t{v.timer2.state.name}")
                    print(f"\t\t\tStart\t{v.timer2.start}")
                    print(f"\t\t\tStop\t{v.timer2.stop}")
                    print()
                else:
                    print(f"{k.replace('_', ' ').title()} \t\t{v if isinstance(v, TimeCodedInteger) else v.name}")
                    print()

        print()


async def connect(uart: int, baudrate: int) -> None:
    """ connect """
    await dump_data(
        SpaMicroConfig(
            {
                'uart_id': uart,
                'baudrate': baudrate
            }
        )
    )

if __name__ == "__main__":
    if (args := len(sys.argv)) < 3:
        usage()
        sys.exit(1)

    if args > 3 and sys.argv[3] in ("-d", "--debug"):
        logging.basicConfig(level=logging.DEBUG)

    asyncio.run(connect(int(sys.argv[1]), int(sys.argv[2])))

    sys.exit(0)
