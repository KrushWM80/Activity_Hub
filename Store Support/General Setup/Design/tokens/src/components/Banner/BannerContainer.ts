module.exports = {
  component: {
    banner: {
      container: {
        alignVertical: {
          value: "start",
        },

        variant: {
          error: {
            backgroundColor: {
              value: "{semantic.color.notice.fill.negative}",
            },
          },

          info: {
            backgroundColor: {
              value: "{semantic.color.notice.fill.info}",
            },
          },

          success: {
            backgroundColor: {
              value: "{semantic.color.notice.fill.positive}",
            },
          },

          warning: {
            backgroundColor: {
              value: "{semantic.color.notice.fill.warning}",
            },
          },
        },
      },
    },
  },
};
