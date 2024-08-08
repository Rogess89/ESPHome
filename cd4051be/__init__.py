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

cd4051be_ns = cg.esphome_ns.namespace("cd4051be")

CD4051BEComponent = cd4051be_ns.class_(
    "CD4051BEComponent", cg.Component, cg.PollingComponent
)

CONF_PIN_A = "pin_a"
CONF_PIN_B = "pin_b"
CONF_PIN_C = "pin_c"
CONF_PIN_INH = "pin_inh"

DEFAULT_DELAY = "2ms"


CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(CD4051BEComponent),
        cv.Required(CONF_PIN_A): pins.gpio_output_pin_schema,
        cv.Required(CONF_PIN_B): pins.gpio_output_pin_schema,
        cv.Required(CONF_PIN_C): pins.gpio_output_pin_schema,
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
    pin_c = await cg.gpio_pin_expression(config[CONF_PIN_C])
    cg.add(var.set_pin_c(pin_c))
    pin_inh = await cg.gpio_pin_expression(config[CONF_PIN_INH])
    cg.add(var.set_pin_inh(pin_inh))

    cg.add(var.set_switch_delay(config[CONF_DELAY]))
