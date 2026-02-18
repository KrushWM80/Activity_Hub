module.exports = {
  semantic: {
    color: {
      field: {
        border: {
          _: {
            darkValue: "{primitive.color.gray.50}",
            themeable: true,
            value: "{primitive.color.gray.80}",
          },

          hovered: {
            darkValue: "{primitive.color.gray.40}",
            themeable: true,
            value: "{primitive.color.gray.160}",
          },

          focused: {
            darkValue: "{primitive.color.white}",
            themeable: true,
            value: "{primitive.color.gray.160}",
          },

          disabled: {
            darkValue: "{primitive.color.gray.100}",
            themeable: true,
            value: "{primitive.color.gray.50}",
          },

          magic: {
            _: {
              darkValue: "{primitive.color.magic.1}",
              themeable: true,
              value: "{primitive.color.magic.1}",
            },

            hovered: {
              darkValue: "{primitive.color.magic.1}",
              themeable: true,
              value: "{primitive.color.magic.1}",
            },

            focused: {
              darkValue: "{primitive.color.magic.1}",
              themeable: true,
              value: "{primitive.color.magic.1}",
            },
          },

          negative: {
            _: {
              darkValue: "{primitive.color.red.50}",
              themeable: true,
              value: "{primitive.color.red.100}",
            },

            hovered: {
              darkValue: "{primitive.color.red.50}",
              themeable: true,
              value: "{primitive.color.red.100}",
            },

            focused: {
              darkValue: "{primitive.color.red.50}",
              themeable: true,
              value: "{primitive.color.red.100}",
            },

            disabled: {
              darkValue: "{primitive.color.gray.100}",
              themeable: true,
              value: "{primitive.color.gray.50}",
            },
          },
        },

        fill: {
          _: {
            darkValue: "{primitive.color.transparentLight.0}",
            themeable: true,
            value: "{primitive.color.white}",
          },

          hovered: {
            darkValue: "{primitive.color.transparentLight.0}",
            themeable: true,
            value: "{primitive.color.white}",
          },

          focused: {
            darkValue: "{primitive.color.transparentLight.0}",
            themeable: true,
            value: "{primitive.color.white}",
          },

          disabled: {
            darkValue: "{primitive.color.transparentLight.0}",
            themeable: true,
            value: "{primitive.color.white}",
          },

          negative: {
            _: {
              darkValue: "{primitive.color.transparentLight.0}",
              themeable: true,
              value: "{primitive.color.white}",
            },

            hovered: {
              darkValue: "{primitive.color.transparentLight.0}",
              themeable: true,
              value: "{primitive.color.white}",
            },

            focused: {
              darkValue: "{primitive.color.transparentLight.0}",
              themeable: true,
              value: "{primitive.color.white}",
            },

            disabled: {
              darkValue: "{primitive.color.transparentLight.0}",
              themeable: true,
              value: "{primitive.color.white}",
            },
          },
        },

        text: {
          onFill: {
            _: {
              darkValue: "{primitive.color.white}",
              themeable: true,
              value: "{primitive.color.gray.160}",
            },

            disabled: {
              darkValue: "{primitive.color.white}",
              themeable: true,
              value: "{primitive.color.gray.50}",
            },
          },

          subtle: {
            onFill: {
              _: {
                comment: "Use for a field's leading icon",
                darkValue: "{primitive.color.gray.50}",
                themeable: true,
                value: "{primitive.color.gray.130}",
              },

              disabled: {
                comment: "Use for a field's leading icon when disabled",
                darkValue: "{primitive.color.gray.100}",
                themeable: true,
                value: "{primitive.color.gray.50}",
              },
            },
          },
        },
      },
    },
  },
};
