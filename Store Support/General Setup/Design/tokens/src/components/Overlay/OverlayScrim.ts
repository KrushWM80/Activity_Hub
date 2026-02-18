module.exports = {
  component: {
    overlay: {
      scrim: {
        backgroundColor: {
          value: "{semantic.color.scrim}",
        },

        state: {
          enter: {
            opacity: {
              value: 0,
            },
          },

          enterActive: {
            opacity: {
              value: 1,
            },

            transitionProperty: {
              value: "opacity",
            },

            transitionTimingFunction: {
              value: "{primitive.timing.linear.100}",
            },
          },

          exit: {
            opacity: {
              value: 1,
            },
          },

          exitActive: {
            opacity: {
              value: 0,
            },

            transitionProperty: {
              value: "opacity",
            },

            transitionTimingFunction: {
              value: "{primitive.timing.linear.100}",
            },
          },
        },
      },
    },
  },
};
