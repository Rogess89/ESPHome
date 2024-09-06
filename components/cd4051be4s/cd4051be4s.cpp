
#include "cd4051be4s.h"
#include "esphome/core/log.h"
#include <cinttypes>

namespace esphome {
namespace cd4051be4s {

static const char *const TAG = "cd4051be4s";

float CD4051BE4SComponent::get_setup_priority() const { return setup_priority::DATA; }

void CD4051BE4SComponent::setup() {
  ESP_LOGCONFIG(TAG, "Setting up CD4051BE4S...");

  this->pin_a_->setup();
  this->pin_b_->setup();

  // Set INH pin to LOW to enable the multiplexer
  this->pin_inh_->setup();
  this->pin_inh_->digital_write(false);

  // Set other pin, so that activate_pin will really switch
  this->active_pin_ = 1;
  this->activate_pin(0);
}

void CD4051BE4SComponent::dump_config() {
  ESP_LOGCONFIG(TAG, "CD4051BE4S Multiplexer:");
  LOG_PIN("  A Pin: ", this->pin_a_);
  LOG_PIN("  B Pin: ", this->pin_b_);
  ESP_LOGCONFIG(TAG, "Switch delay: %" PRIu32, this->switch_delay_);
}

void CD4051BE4SComponent::activate_pin(uint8_t pin) {
  if (this->active_pin_ != pin) {
    ESP_LOGD(TAG, "Switch to input %d", pin);

    static int mux_channel[4][2] = {
        {0, 0},  // channel 0
        {1, 0},  // channel 1
        {0, 1},  // channel 2
        {1, 1},  // channel 3

    };

    this->pin_a_->digital_write(mux_channel[pin][0]);
    this->pin_b_->digital_write(mux_channel[pin][1]);

    // Small delay is needed to let the multiplexer switch
    delay(this->switch_delay_);
    this->active_pin_ = pin;
  }
}

CD4051BE4SSensor::CD4051BE4SSensor(CD4051BE4SComponent *parent) : parent_(parent) {}

void CD4051BE4SSensor::update() {
  float value_v = this->sample();
  this->publish_state(value_v);
}

float CD4051BE4SSensor::get_setup_priority() const { return this->parent_->get_setup_priority() - 1.0f; }

float CD4051BE4SSensor::sample() {
  this->parent_->activate_pin(this->pin_);
  return this->source_->sample();
}

void CD4051BE4SSensor::dump_config() {
  LOG_SENSOR(TAG, "CD4051BE4S Sensor", this);
  ESP_LOGCONFIG(TAG, "  Pin: %u", this->pin_);
  LOG_UPDATE_INTERVAL(this);
}

}  // namespace cd4051be4s
}  // namespace esphome
