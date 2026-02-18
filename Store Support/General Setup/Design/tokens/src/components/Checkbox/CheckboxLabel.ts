module.exports = {
  component: {
    checkbox: {
      label: {
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

          indeterminate: {
            fontWeight: {
              value: "{primitive.font.weight.700}",
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
