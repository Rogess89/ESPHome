import esphome.codegen as cg
from esphome import pins
import esphome.config_validation as cv
from esphome.const import (
    CONF_DELAY,
    CONF_ID,
)

AUTO_LOAD = ["sensor", "voltage_sampler"]
CODEOWNERS = ["@asoehlke"]
MULTI_CONF = True

cd4051be4s_ns = cg.esphome_ns.namespace("cd4051be4s")

CD4051BE4SComponent = cd4051be4s_ns.class_(
    "CD4051BE4SComponent", cg.Component, cg.PollingComponent
)

CONF_PIN_A = "pin_a"
CONF_PIN_B = "pin_b"
CONF_PIN_INH = "pin_inh"

DEFAULT_DELAY = "2ms"


CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(CD4051BE4SComponent),
        cv.Required(CONF_PIN_A): pins.gpio_output_pin_schema,
        cv.Required(CONF_PIN_B): pins.gpio_output_pin_schema,
        cv.Required(CONF_PIN_INH): pins.gpio_output_pin_schema,
        cv.Optional(
            CONF_DELAY, default=DEFAULT_DELAY
        ): cv.positive_time_period_milliseconds,
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    pin_a = await cg.gpio_pin_expression(config[CONF_PIN_A])
    cg.add(var.set_pin_a(pin_a))
    pin_b = await cg.gpio_pin_expression(config[CONF_PIN_B])
    cg.add(var.set_pin_b(pin_b))
    pin_inh = await cg.gpio_pin_expression(config[CONF_PIN_INH])
    cg.add(var.set_pin_inh(pin_inh))

    cg.add(var.set_switch_delay(config[CONF_DELAY]))
