module.exports = {
  component: {
    switch: {
      handle: {
        backgroundColor: {
          _: {
            value: "{semantic.color.switch.indicator._}",
          },

          disabled: {
            value: "{semantic.color.switch.indicator.disabled}",
          },
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.round}",
        },

        elevation: {
          value: "{semantic.elevation.100}",
        },

        height: {
          value: "{primitive.scale.space.250}",
        },

        offsetStart: {
          value: "{primitive.scale.space.25}",
        },

        offsetTop: {
          value: "{primitive.scale.space.25}",
        },

        state: {
          activated: {
            translateX: {
              value: "24px",
            },
          },
        },

        backgroundColorTransition: {
          transitionDuration: {
            value: "{primitive.duration.100}",
          },

          transitionProperty: {
            value: "backgroundColor",
          },
        },

        transformTransition: {
          transitionDuration: {
            value: "{primitive.duration.100}",
          },

          transitionProperty: {
            value: "transform",
          },

          transitionTimingFunction: {
            value: "{primitive.timing.easeInOut.100}",
          },
        },

        width: {
          value: "{primitive.scale.space.250}",
        },
      },
    },
  },
};
