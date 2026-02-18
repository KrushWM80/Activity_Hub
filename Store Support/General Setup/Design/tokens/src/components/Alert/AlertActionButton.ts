module.exports = {
  component: {
    alert: {
      actionButton: {
        aliasName: {
          value: "text.body",
        },

        aliasOptions: {
          size: {
            value: "small",
          },
        },

        textDecoration: {
          _: {
            value: "underline",
          },

          hovered: {
            value: "none",
          },

          focused: {
            value: "none",
          },

          pressed: {
            value: "none",
          },
        },

        textWrap: {
          value: false,
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
