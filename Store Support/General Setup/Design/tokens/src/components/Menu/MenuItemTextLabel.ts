module.exports = {
  component: {
    menu: {
      itemTextLabel: {
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
            value: "{semantic.color.action.text.onFill.transparent._}",
          },

          hovered: {
            value: "{semantic.color.action.text.onFill.transparent.hovered}",
          },

          focused: {
            value: "{semantic.color.action.text.onFill.transparent.focused}",
          },

          pressed: {
            value: "{semantic.color.action.text.onFill.transparent.pressed}",
          },

          disabled: {
            value: "{semantic.color.action.text.onFill.transparent.disabled}",
          },
        },

        textWrap: {
          value: false,
        },
      },
    },
  },
};
