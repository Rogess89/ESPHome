import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, voltage_sampler
from esphome.const import (
    CONF_ID,
    CONF_SENSOR,
    CONF_NUMBER,
    ICON_FLASH,
    UNIT_VOLT,
    STATE_CLASS_MEASUREMENT,
    DEVICE_CLASS_VOLTAGE,
)
from . import cd4051be4s_ns, CD4051BE4SComponent

DEPENDENCIES = ["cd4051be4s"]

CD4051BE4SSensor = cd4051be4s_ns.class_(
    "CD4051BE4SSensor",
    sensor.Sensor,
    cg.PollingComponent,
    voltage_sampler.VoltageSampler,
)

CONF_CD4051BE4S_ID = "cd4051be4s_id"

CONFIG_SCHEMA = (
    sensor.sensor_schema(
        CD4051BE4SSensor,
        unit_of_measurement=UNIT_VOLT,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
        icon=ICON_FLASH,
    )
    .extend(
        {
            cv.GenerateID(CONF_CD4051BE4S_ID): cv.use_id(CD4051BE4SComponent),
            cv.Required(CONF_NUMBER): cv.int_range(0, 3),
            cv.Required(CONF_SENSOR): cv.use_id(voltage_sampler.VoltageSampler),
        }
    )
    .extend(cv.polling_component_schema("60s"))
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_CD4051BE4S_ID])

    var = cg.new_Pvariable(config[CONF_ID], parent)
    await sensor.register_sensor(var, config)
    await cg.register_component(var, config)
    cg.add(var.set_pin(config[CONF_NUMBER]))

    sens = await cg.get_variable(config[CONF_SENSOR])
    cg.add(var.set_source(sens))
