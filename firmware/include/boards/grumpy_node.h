// =============================================================
// boards/grumpy_node.h - Grumpy Node
// Seeed XIAO ESP32-C3 + Ebyte E22P-915M30S (SX1262 + 1 W PA).
// Ported from MeshCore's feature/grumpy-web-setup target.
// =============================================================
#pragma once

inline const BoardConfig BOARD = {
    .name        = "Grumpy Node",
    .fw_suffix   = "grumpy_node",
    .mdns_prefix = "grumpy-node",

    .pin_lora_nss  = 20,  // D7
    .pin_lora_rst  = 3,   // D1
    .pin_lora_busy = 5,   // D3
    .pin_lora_dio1 = 4,   // D2
    .pin_lora_sck  = 8,   // D8
    .pin_lora_miso = 9,   // D9
    .pin_lora_mosi = 10,  // D10

    .rf_switch = {
        // GPIO21 is UART0 TX after reset. Claim it at the start of setup and
        // keep it HIGH so the E22P remains enabled throughout startup.
        .en_pin             = 21,  // D6
        .en_low_hold_ms     = 0,
        .rx_pin             = -1,
        .tx_pin             = -1,
        .dio2_as_rf_switch  = true,
        .en_high_from_boot  = true,
    },

    // Shared I2C bus for the MAX17048 fuel gauge. No OLED is fitted.
    .pin_i2c_sda      = 6,  // D4
    .pin_i2c_scl      = 7,  // D5
    .pin_i2c_oled_rst = -1,
    .pin_vext_enable_low = -1,

    // GPIO9 is both the XIAO BOOT button and LoRa MISO, so it cannot be used
    // as the runtime reset/settings button.
    .pin_user_button        = -1,
    .user_button_active_low = true,

    .battery = {
        .pin = -1,
        .enable_pin = -1,
        .enable_active_high = false,
        .multiplier = 0.0f,
        .fuel_gauge_i2c_addr = 0x36,
        .fuel_gauge_vcell_reg = 0x02,
        .fuel_gauge_crate_reg = 0x16,
        .fuel_gauge_repeated_start = true,
    },

    // This is SX1262 drive into the E22P PA, not antenna-side output power.
    .max_tx_power_dbm = 22,
    .use_dio3_tcxo = true,
    .tcxo_voltage  = 1.8f,
    .sx126x_current_limit_ma = 140,
    .sx126x_rx_boosted_gain = true,

    .has_lora_radio = true,
    .has_wifi       = true,
    .has_network    = true,

    .pin_protocol_uart_rx = -1,
    .pin_protocol_uart_tx = -1,
    .protocol_uart_baud   = 921600,

    .ethernet = { .enabled = false },
    .static_gpios = {},
    .static_gpio_count = 0,
};
