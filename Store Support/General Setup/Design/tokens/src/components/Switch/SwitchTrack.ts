module.exports = {
  component: {
    switch: {
      track: {
        transitionDuration: {
          value: "{primitive.duration.100}",
        },

        transitionProperty: {
          value: "backgroundColor",
        },

        backgroundColor: {
          _: {
            value: "{semantic.color.switch.fill._}",
          },

          hovered: {
            value: "{semantic.color.switch.fill.hovered}",
          },

          focused: {
            value: "{semantic.color.switch.fill.focused}",
          },

          pressed: {
            value: "{semantic.color.switch.fill.pressed}",
          },

          disabled: {
            value: "{semantic.color.switch.fill.disabled}",
          },
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.round}",
        },

        height: {
          value: "{primitive.scale.space.300}",
        },

        state: {
          activated: {
            backgroundColor: {
              _: {
                value: "{semantic.color.switch.fill.activated._}",
              },

              hovered: {
                value: "{semantic.color.switch.fill.activated.hovered}",
              },

              focused: {
                value: "{semantic.color.switch.fill.activated.focused}",
              },

              pressed: {
                value: "{semantic.color.switch.fill.activated.pressed}",
              },

              disabled: {
                value: "{semantic.color.switch.fill.activated.disabled}",
              },
            },
          },
        },

        width: {
          value: "{primitive.scale.space.600}",
        },
      },
    },
  },
};
