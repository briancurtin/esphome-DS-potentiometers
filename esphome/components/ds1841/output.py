from esphome import pins
import esphome.codegen as cg
from esphome.components import output
import esphome.config_validation as cv
from esphome.const import (
    CONF_INITIAL_VALUE,
    CONF_VOLTAGE_DIVIDER,
    CONF_SDA_PIN,
    CONF_SCL_PIN,
)
from esphome.types import ConfigType

CODEOWNERS = ["@briancurtin"]

ds1841_ns = cg.esphome_ns.namespace("ds1841")

ds1841Output = ds1841_ns.class_("ds1841Output", output.FloatOutput, cg.Component)

CONFIG_SCHEMA = cv.All(
    output.FLOAT_OUTPUT_SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(ds1841Output),
            # Need to know if this is connected to AO/A1 for addressing
            cv.Required(CONF_VOLTAGE_DIVIDER): pins.internal_gpio_pin_schema,
            cv.Required(CONF_SDA_PIN): pins.internal_gpio_output_pin_schema,
            cv.Required(CONF_SCL_PIN): pins.internal_gpio_output_pin_schema,
            cv.Optional(CONF_INITIAL_VALUE, default=1.0): cv.float_range(
                min=0.01, max=1.0
            ),
        }
    )
)


async def to_code(config: ConfigType) -> None:
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await output.register_output(var, config)

    vd_pin = await cg.gpio_pin_expression(config[CONF_VOLTAGE_DIVIDER])
    cg.add(var.set_voltage_divider(vd_pin))

    sda_pin = await cg.gpio_pin_expression(config[CONF_SDA_PIN])
    cg.add(var.set_sda_pin(sda_pin))

    scl_pin = await cg.gpio_pin_expression(config[CONF_SCL_PIN])
    cg.add(var.set_scl_pin(scl_pin))

    cg.add(var.set_initial_value(config[CONF_INITIAL_VALUE]))
