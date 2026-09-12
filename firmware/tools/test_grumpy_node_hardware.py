#!/usr/bin/env python3
"""Focused source contract for the Grumpy Node hardware port."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIRMWARE = ROOT / "firmware"

platformio = (FIRMWARE / "platformio.ini").read_text()
section = platformio.split("[env:grumpy_node]", 1)[1].split("[env:", 1)[0]
for setting in (
    "board = seeed_xiao_esp32c3",
    "board_build.f_cpu = 80000000L",
    "board_build.partitions = partitions/grumpy_node.csv",
    "-DBOARD_GRUMPY_NODE",
    "-DDEFAULT_FREQ=915800000",
    "-DDEFAULT_POWER=20",
):
    assert setting in section

board_config = (FIRMWARE / "include/board_config.h").read_text()
board = (FIRMWARE / "include/boards/grumpy_node.h").read_text()
assert "defined(BOARD_GRUMPY_NODE)" in board_config
assert "bool     en_high_from_boot = false;" in board_config

for setting in (
    ".pin_lora_nss  = 20",
    ".pin_lora_rst  = 3",
    ".pin_lora_busy = 5",
    ".pin_lora_dio1 = 4",
    ".pin_lora_sck  = 8",
    ".pin_lora_miso = 9",
    ".pin_lora_mosi = 10",
    ".en_pin             = 21",
    ".en_high_from_boot  = true",
    ".dio2_as_rf_switch  = true",
    ".pin_i2c_sda      = 6",
    ".pin_i2c_scl      = 7",
    ".fuel_gauge_i2c_addr = 0x36",
    ".fuel_gauge_vcell_reg = 0x02",
    ".fuel_gauge_crate_reg = 0x16",
    ".fuel_gauge_repeated_start = true",
    ".max_tx_power_dbm = 22",
    ".tcxo_voltage  = 1.8f",
    ".sx126x_current_limit_ma = 140",
    ".sx126x_rx_boosted_gain = true",
):
    assert setting in board

for other_board in (FIRMWARE / "include/boards").glob("*.h"):
    if other_board.name != "grumpy_node.h":
        assert ".en_high_from_boot  = true" not in other_board.read_text()

main = (FIRMWARE / "src/main.cpp").read_text()
assert "static SPIClass loraSpi(FSPI);" in main
assert ".freq_hz      = DEFAULT_FREQ" in main
assert ".power_dbm    = DEFAULT_POWER" in main
assert main.index("rfSwitchEnAtBoot();") < main.index("WifiManager::checkResetButton();")

battery = (FIRMWARE / "src/battery_monitor.cpp").read_text()
assert "Wire.endTransmission(!repeatedStart)" in battery

assets = (FIRMWARE / "tools/build_firmware_assets.py").read_text()
assert '"grumpy_node": {' in assets
assert '"chip_family": "ESP32-C3"' in assets
assert '"firmware/include/boards/grumpy_node.h": "grumpy_node"' in assets

partitions = (FIRMWARE / "partitions/grumpy_node.csv").read_text()
assert "app0,     app,  ota_0,   0x10000, 0x1E0000" in partitions
assert "app1,     app,  ota_1,   0x1F0000,0x1E0000" in partitions

print("Grumpy Node hardware contract: PASS")
