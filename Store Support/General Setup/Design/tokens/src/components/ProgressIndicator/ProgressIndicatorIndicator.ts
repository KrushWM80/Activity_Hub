module.exports = {
  component: {
    progressIndicator: {
      indicator: {
        transitionDuration: {
          value: "{primitive.duration.500}",
        },

        transitionProperty: {
          value: "width",
        },

        transitionTimingFunction: {
          value: "{primitive.timing.linear.100}",
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.round}",
        },

        height: {
          value: "{primitive.scale.space.50}",
        },

        variant: {
          error: {
            backgroundColor: {
              value: "{semantic.color.progress.fill.negative}",
            },
          },

          info: {
            backgroundColor: {
              value: "{semantic.color.progress.fill.info}",
            },
          },

          success: {
            backgroundColor: {
              value: "{semantic.color.progress.fill.positive}",
            },
          },

          warning: {
            backgroundColor: {
              value: "{semantic.color.progress.fill.warning}",
            },
          },
        },
      },
    },
  },
};
