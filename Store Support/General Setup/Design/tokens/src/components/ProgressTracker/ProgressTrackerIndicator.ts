module.exports = {
  component: {
    progressTracker: {
      indicator: {
        height: {
          value: "{primitive.scale.space.25}",
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
