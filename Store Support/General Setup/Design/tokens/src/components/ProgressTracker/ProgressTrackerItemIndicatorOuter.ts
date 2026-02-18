module.exports = {
  component: {
    progressTracker: {
      itemIndicatorOuter: {
        backgroundColor: {
          value: "{semantic.color.fill._}",
        },

        borderWidth: {
          value: "{primitive.scale.border.width.200}",
        },

        radius: {
          value: "{primitive.scale.border.radius.100}",
        },

        state: {
          activated: {
            variant: {
              error: {
                borderColor: {
                  value: "{semantic.color.progress.fill.negative}",
                },
              },

              info: {
                borderColor: {
                  value: "{semantic.color.progress.fill.info}",
                },
              },

              success: {
                borderColor: {
                  value: "{semantic.color.progress.fill.positive}",
                },
              },

              warning: {
                borderColor: {
                  value: "{semantic.color.progress.fill.warning}",
                },
              },
            },
          },
        },
      },
    },
  },
};
