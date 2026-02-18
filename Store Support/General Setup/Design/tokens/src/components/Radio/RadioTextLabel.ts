module.exports = {
  component: {
    radio: {
      textLabel: {
        aliasName: {
          value: "text.body",
        },

        aliasOptions: {
          size: {
            value: "small",
          },
        },

        marginStart: {
          value: "{primitive.scale.space.150}",
        },

        state: {
          activated: {
            aliasOptions: {
              weight: {
                value: "alt",
              },
            },
          },
        },

        textColor: {
          _: {
            value: "{semantic.color.text._}",
          },

          disabled: {
            value: "{semantic.color.text.disabled}",
          },
        },
      },
    },
  },
};
