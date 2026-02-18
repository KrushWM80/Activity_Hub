module.exports = {
  component: {
    iconButton: {
      container: {
        color: {
          default: {
            backgroundColor: {
              _: {
                value: "{semantic.color.action.fill.transparent._}",
              },

              hovered: {
                value: "{semantic.color.action.fill.transparent.hovered}",
              },

              focused: {
                value: "{semantic.color.action.fill.transparent.focused}",
              },

              pressed: {
                value: "{semantic.color.action.fill.transparent.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.fill.transparent.disabled}",
              },
            },
          },

          white: {
            backgroundColor: {
              _: {
                value: "{semantic.color.action.fill.accent.white._}",
              },

              hovered: {
                value: "{semantic.color.action.fill.accent.white.hovered}",
              },

              focused: {
                value: "{semantic.color.action.fill.accent.white.focused}",
              },

              pressed: {
                value: "{semantic.color.action.fill.accent.white.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.fill.accent.white.disabled}",
              },
            },
          },
        },

        size: {
          xsmall: {
            padding: {
              value: "{primitive.scale.space.50}",
            },
          },

          small: {
            padding: {
              value: "{primitive.scale.space.100}",
            },
          },

          medium: {
            padding: {
              value: "{primitive.scale.space.100}",
            },
          },

          large: {
            padding: {
              value: "{primitive.scale.space.100}",
            },
          },
        },

        variant: {
          full: {
            borderRadius: {
              value: "{primitive.scale.border.radius.50}",
            },
          },

          round: {
            borderRadius: {
              value: "{primitive.scale.border.radius.round}",
            },
          },
        },
      },
    },
  },
};
