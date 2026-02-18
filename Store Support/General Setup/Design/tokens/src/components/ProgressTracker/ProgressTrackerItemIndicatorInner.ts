module.exports = {
  component: {
    progressTracker: {
      itemIndicatorInner: {
        backgroundColor: {
          value: "{semantic.color.progress.fill._}",
        },

        radius: {
          value: "{primitive.scale.border.radius.50}",
        },

        state: {
          activated: {
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
    },
  },
};
