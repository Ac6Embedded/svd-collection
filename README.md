# svd-collection

Every vendor SVD collection in one repo, as git submodules pinned to known commits.

| Path | Repo | Contents | License |
|---|---|---|---|
| st | [modm-io/cmsis-svd-stm32](https://github.com/modm-io/cmsis-svd-stm32) | STM32, all families | Apache-2.0 (repo), ST SLA on the SVD data |
| nxp | [nxp-mcuxpresso/mcux-soc-svd](https://github.com/nxp-mcuxpresso/mcux-soc-svd) | LPC, MCX, KW, K32, i.MX RT, i.MX 8/9 (official NXP, files named .xml) | BSD-3-Clause |
| nordic | [Ac6Embedded/svd-nordic](https://github.com/Ac6Embedded/svd-nordic) | nRF52/53/54L/54H/71/91/92 | BSD-3-Clause |
| silabs | [Ac6Embedded/svd-silabs](https://github.com/Ac6Embedded/svd-silabs) | EFM32, EFR32, modules, SiWG917 | mixed, see repo (private) |
| infineon | [Ac6Embedded/svd-infineon](https://github.com/Ac6Embedded/svd-infineon) | PSoC 4/6, TRAVEO, XMC, PSE84, AURIX TC375 | mostly Apache-2.0, see repo |
| ti | [Ac6Embedded/svd-ti](https://github.com/Ac6Embedded/svd-ti) | MSPM0, MSP432, TM4C, SimpleLink CC | BSD-3-Clause plus community files, see repo |
| microchip | [Ac6Embedded/svd-microchip](https://github.com/Ac6Embedded/svd-microchip) | SAM and PIC32C | Apache-2.0 |
| renesas | [Ac6Embedded/svd-renesas](https://github.com/Ac6Embedded/svd-renesas) | RA, RZ/T, RZ/N | unclear, see repo (private) |
| espressif | [Ac6Embedded/svd-espressif](https://github.com/Ac6Embedded/svd-espressif) | ESP32 series | Apache-2.0 |
| analog | [Ac6Embedded/svd-analog](https://github.com/Ac6Embedded/svd-analog) | MAX32, MAX78 | Apache-2.0 |
| raspberrypi | [Ac6Embedded/svd-raspberrypi](https://github.com/Ac6Embedded/svd-raspberrypi) | RP2040, RP2350 | BSD-3-Clause |

## Clone

Everything (needs access to the two private repos):

    git clone --recurse-submodules --shallow-submodules https://github.com/Ac6Embedded/svd-collection

Only what you need:

    git clone https://github.com/Ac6Embedded/svd-collection
    cd svd-collection
    git submodule update --init --depth 1 st nordic ti

silabs and renesas are private for license reasons. Anonymous submodule
init fails on those two, init the others selectively as shown above.

## Updates

The Ac6Embedded vendor repos refresh from their upstreams every Monday
06:00 UTC. This repo bumps all submodule pointers one hour later
(bump-submodules workflow). Run it locally with:

    python scripts/bump.py

The script only reads remote heads and stages new gitlinks, it never
clones submodules. The nxp submodule tracks the NXP release branch
(release/25.06.00 today); when NXP switches to a new release branch the
script falls back to the remote default branch automatically. Bumping the
private submodules from CI needs a GH_PAT repo secret with read access,
otherwise they are skipped and can be bumped locally.
