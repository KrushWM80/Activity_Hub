module.exports = {
  component: {
    banner: {
      textLabel: {
        aliasName: {
          value: "text.body",
        },

        aliasOptions: {
          size: {
            value: "small",
          },
        },

        maxWidth: {
          value: "700px",
        },

        textAlign: {
          value: "center",
        },

        variant: {
          error: {
            textColor: {
              value: "{semantic.color.notice.text.onFill.negative}",
            },
          },

          info: {
            textColor: {
              value: "{semantic.color.notice.text.onFill.info}",
            },
          },

          success: {
            textColor: {
              value: "{semantic.color.notice.text.onFill.positive}",
            },
          },

          warning: {
            textColor: {
              value: "{semantic.color.notice.text.onFill.warning}",
            },
          },
        },
      },
    },
  },
};
