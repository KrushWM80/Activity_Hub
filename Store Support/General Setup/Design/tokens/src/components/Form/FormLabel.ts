module.exports = {
  component: {
    form: {
      label: {
        size: {
          large: {
            aliasName: {
              value: "text.body",
            },

            aliasOptions: {
              size: {
                value: "small",
              },

              weight: {
                value: "alt",
              },
            },
          },

          small: {
            aliasName: {
              value: "text.caption",
            },

            aliasOptions: {
              weight: {
                value: "alt",
              },
            },
          },
        },

        state: {
          disabled: {
            textColor: {
              value: "{semantic.color.text.disabled}",
            },
          },
        },

        textColor: {
          value: "{semantic.color.text._}",
        },
      },
    },
  },
};
