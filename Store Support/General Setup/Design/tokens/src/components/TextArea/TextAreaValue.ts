module.exports = {
  component: {
    textArea: {
      _value: {
        aliasName: {
          value: "text.body",
        },

        size: {
          large: {
            aliasOptions: {
              size: {
                value: "medium",
              },
            },
          },

          small: {
            aliasOptions: {
              size: {
                value: "small",
              },
            },
          },
        },

        textColor: {
          _: {
            value: "{semantic.color.field.text.onFill._}",
          },

          disabled: {
            value: "{semantic.color.field.text.onFill.disabled}",
          },
        },
      },
    },
  },
};
