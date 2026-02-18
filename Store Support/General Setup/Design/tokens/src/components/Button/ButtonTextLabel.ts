module.exports = {
  component: {
    button: {
      textLabel: {
        fontFamily: {
          value: "{primitive.font.family.sans}",
        },

        fontWeight: {
          value: "{semantic.font.action.weight}",
        },

        size: {
          small: {
            fontSize: {
              value: "{primitive.font.size.50}",
            },

            lineHeight: {
              value: "{primitive.scale.space.400}",
            },
          },

          medium: {
            fontSize: {
              value: "{primitive.font.size.100}",
            },

            lineHeight: {
              value: "{primitive.scale.space.500}",
            },
          },

          large: {
            fontSize: {
              value: "{primitive.font.size.150}",
            },

            lineHeight: {
              value: "{primitive.scale.space.600}",
            },
          },
        },

        textWrap: {
          value: false,
        },

        variant: {
          primary: {
            textColor: {
              _: {
                value: "{semantic.color.action.text.onFill.primary._}",
              },

              hovered: {
                value: "{semantic.color.action.text.onFill.primary.hovered}",
              },

              focused: {
                value: "{semantic.color.action.text.onFill.primary.focused}",
              },

              pressed: {
                value: "{semantic.color.action.text.onFill.primary.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.text.onFill.primary.disabled}",
              },
            },
          },

          secondary: {
            textColor: {
              _: {
                value: "{semantic.color.action.text.onFill.secondary._}",
              },

              hovered: {
                value: "{semantic.color.action.text.onFill.secondary.hovered}",
              },

              focused: {
                value: "{semantic.color.action.text.onFill.secondary.focused}",
              },

              pressed: {
                value: "{semantic.color.action.text.onFill.secondary.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.text.onFill.secondary.disabled}",
              },
            },
          },

          tertiary: {
            textColor: {
              _: {
                value: "{semantic.color.action.text.onFill.tertiary._}",
              },

              hovered: {
                value: "{semantic.color.action.text.onFill.tertiary.hovered}",
              },

              focused: {
                value: "{semantic.color.action.text.onFill.tertiary.focused}",
              },

              pressed: {
                value: "{semantic.color.action.text.onFill.tertiary.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.text.onFill.tertiary.disabled}",
              },
            },
          },

          destructive: {
            textColor: {
              _: {
                value: "{semantic.color.action.text.onFill.negative._}",
              },

              hovered: {
                value: "{semantic.color.action.text.onFill.negative.hovered}",
              },

              focused: {
                value: "{semantic.color.action.text.onFill.negative.focused}",
              },

              pressed: {
                value: "{semantic.color.action.text.onFill.negative.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.text.onFill.negative.disabled}",
              },
            },
          },
        },
      },
    },
  },
};
