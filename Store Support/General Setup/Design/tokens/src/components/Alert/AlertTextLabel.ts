module.exports = {
  component: {
    alert: {
      textLabel: {
        aliasName: {
          value: "text.body",
        },

        aliasOptions: {
          size: {
            value: "small",
          },
        },

        variant: {
          error: {
            textColor: {
              value: "{semantic.color.text.onFill.negative.subtle}",
            },
          },

          info: {
            textColor: {
              value: "{semantic.color.text.onFill.info.subtle}",
            },
          },

          success: {
            textColor: {
              value: "{semantic.color.text.onFill.positive.subtle}",
            },
          },

          warning: {
            textColor: {
              value: "{semantic.color.text.onFill.warning.subtle}",
            },
          },
        },
      },
    },
  },
};
