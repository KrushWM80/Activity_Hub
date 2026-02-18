module.exports = {
  component: {
    chip: {
      textLabel: {
        aliasName: {
          value: "text.body",
        },

        aliasOptions: {
          size: {
            value: "small",
          },
        },

        textColor: {
          _: {
            value: "{semantic.color.input.text.onFill._}",
          },

          disabled: {
            value: "{semantic.color.input.text.onFill.disabled}",
          },
        },

        textWrap: {
          value: false,
        },
      },
    },
  },
};
