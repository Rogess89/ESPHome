#pragma once

#include "esphome/core/component.h"
#include "esphome/core/hal.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/voltage_sampler/voltage_sampler.h"

namespace esphome {
namespace cd4051be4s {

class CD4051BE4SComponent : public Component {
 public:
  /// Set up the internal sensor array.
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override;

  /// setting pin active by setting the right combination of the four multiplexer input pins
  void activate_pin(uint8_t pin);

  /// set the pin connected to multiplexer control pin a
  void set_pin_a(GPIOPin *pin) { this->pin_a_ = pin; }
  /// set the pin connected to multiplexer control pin b
  void set_pin_b(GPIOPin *pin) { this->pin_b_ = pin; }
  /// set the pin connected to multiplexer control pin inh
  void set_pin_inh(GPIOPin *pin) { this->pin_inh_ = pin; }

  /// set the delay needed after an input switch
  void set_switch_delay(uint32_t switch_delay) { this->switch_delay_ = switch_delay; }

 private:
  GPIOPin *pin_a_;
  GPIOPin *pin_b_;
  GPIOPin *pin_inh_;
  /// the currently active pin
  uint8_t active_pin_;
  uint32_t switch_delay_;
};

class CD4051BE4SSensor : public sensor::Sensor, public PollingComponent, public voltage_sampler::VoltageSampler {
 public:
  CD4051BE4SSensor(CD4051BE4SComponent *parent);

  void update() override;

  void dump_config() override;
  /// `HARDWARE_LATE` setup priority.
  float get_setup_priority() const override;
  void set_pin(uint8_t pin) { this->pin_ = pin; }
  void set_source(voltage_sampler::VoltageSampler *source) { this->source_ = source; }

  float sample() override;

 protected:
  CD4051BE4SComponent *parent_;
  /// The sampling source to read values from.
  voltage_sampler::VoltageSampler *source_;

  uint8_t pin_;
};
}  // namespace cd4051be4s
}  // namespace esphome
