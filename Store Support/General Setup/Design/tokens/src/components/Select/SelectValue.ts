module.exports = {
  component: {
    select: {
      _value: {
        aliasName: {
          value: "text.body",
        },

        size: {
          small: {
            aliasOptions: {
              size: {
                value: "small",
              },
            },
          },

          large: {
            aliasOptions: {
              size: {
                value: "medium",
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
