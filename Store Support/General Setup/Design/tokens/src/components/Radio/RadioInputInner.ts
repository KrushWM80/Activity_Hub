module.exports = {
  component: {
    radio: {
      inputInner: {
        borderRadius: {
          value: "{primitive.scale.border.radius.round}",
        },

        height: {
          value: "{primitive.scale.space.100}",
        },

        radius: {
          value: "4px",
        },

        width: {
          value: "{primitive.scale.space.100}",
        },

        state: {
          activated: {
            backgroundColor: {
              _: {
                value: "{semantic.color.input.indicator.activated}",
              },

              focused: {
                value: "{semantic.color.input.indicator.activated}",
              },

              hovered: {
                value: "{semantic.color.input.indicator.activated}",
              },

              pressed: {
                value: "{semantic.color.input.indicator.activated}",
              },

              disabled: {
                value: "{semantic.color.input.indicator.activated}",
              },
            },
          },
        },
      },
    },
  },
};
