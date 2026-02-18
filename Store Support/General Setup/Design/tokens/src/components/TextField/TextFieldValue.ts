module.exports = {
  component: {
    textField: {
      _value: {
        fontFamily: {
          value: "{primitive.font.family.sans}",
        },

        fontWeight: {
          value: "{primitive.font.weight.400}",
        },

        size: {
          large: {
            fontSize: {
              value: "{primitive.font.size.100}",
            },

            lineHeight: {
              value: "{primitive.scale.space.300}",
            },
          },

          small: {
            fontSize: {
              value: "{primitive.font.size.50}",
            },

            lineHeight: {
              value: "{primitive.scale.space.300}",
              comment:
                "This takes into account the extra 4px missed in figma: 20px + 4px = 24px",
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
