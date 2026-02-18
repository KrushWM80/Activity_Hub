module.exports = {
  component: {
    button: {
      container: {
        alignHorizontal: {
          value: "center",
        },

        alignVertical: {
          value: "center",
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.round}",
        },

        size: {
          small: {
            paddingHorizontal: {
              value: "{primitive.scale.space.200}",
            },

            paddingVertical: {
              value: "0px",
            },
          },

          medium: {
            paddingHorizontal: {
              value: "{primitive.scale.space.300}",
            },

            paddingVertical: {
              value: "0px",
            },
          },

          large: {
            paddingHorizontal: {
              value: "{primitive.scale.space.300}",
            },

            paddingVertical: {
              value: "0px",
            },
          },
        },

        state: {
          isFullWidth: {
            width: {
              value: "fill-parent",
            },
          },
        },

        transitionDuration: {
          value: "{primitive.duration.100}",
        },

        transitionProperty: {
          value: "all",
        },

        transitionTimingFunction: {
          value: "{primitive.timing.easeInOut.100}",
        },

        variant: {
          primary: {
            backgroundColor: {
              _: {
                value: "{semantic.color.action.fill.primary._}",
              },

              hovered: {
                value: "{semantic.color.action.fill.primary.hovered}",
              },

              focused: {
                value: "{semantic.color.action.fill.primary.focused}",
              },

              pressed: {
                value: "{semantic.color.action.fill.primary.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.fill.primary.disabled}",
              },
            },
          },

          secondary: {
            backgroundColor: {
              _: {
                value: "{semantic.color.action.fill.secondary._}",
              },

              hovered: {
                value: "{semantic.color.action.fill.secondary.hovered}",
              },

              focused: {
                value: "{semantic.color.action.fill.secondary.focused}",
              },

              pressed: {
                value: "{semantic.color.action.fill.secondary.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.fill.secondary.disabled}",
              },
            },

            borderColor: {
              _: {
                value: "{semantic.color.action.border.secondary._}",
              },

              hovered: {
                value: "{semantic.color.action.border.secondary.hovered}",
              },

              focused: {
                value: "{semantic.color.action.border.secondary.focused}",
              },

              pressed: {
                value: "{semantic.color.action.border.secondary.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.border.secondary.disabled}",
              },
            },

            borderWidth: {
              _: {
                value: "{semantic.scale.border.width.interactive._}",
              },

              hovered: {
                value: "{semantic.scale.border.width.interactive.hovered}",
              },

              focused: {
                value: "{semantic.scale.border.width.interactive.focused}",
              },

              pressed: {
                value: "{semantic.scale.border.width.interactive.pressed}",
              },

              disabled: {
                value: "{semantic.scale.border.width.interactive._}",
              },
            },
          },

          tertiary: {
            backgroundColor: {
              _: {
                value: "{semantic.color.action.fill.tertiary._}",
              },

              hovered: {
                value: "{semantic.color.action.fill.tertiary.hovered}",
              },

              focused: {
                value: "{semantic.color.action.fill.tertiary.focused}",
              },

              pressed: {
                value: "{semantic.color.action.fill.tertiary.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.fill.tertiary.disabled}",
              },
            },

            borderColor: {
              _: {
                value: "{semantic.color.action.border.tertiary._}",
              },

              hovered: {
                value: "{semantic.color.action.border.tertiary.hovered}",
              },

              focused: {
                value: "{semantic.color.action.border.tertiary.focused}",
              },

              pressed: {
                value: "{semantic.color.action.border.tertiary.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.border.tertiary.disabled}",
              },
            },

            borderWidth: {
              _: {
                value: "{semantic.scale.border.width.interactive._}",
              },

              hovered: {
                value: "{semantic.scale.border.width.interactive.hovered}",
              },

              focused: {
                value: "{semantic.scale.border.width.interactive.focused}",
              },

              pressed: {
                value: "{semantic.scale.border.width.interactive.pressed}",
              },

              disabled: {
                value: "{semantic.scale.border.width.interactive._}",
              },
            },
          },

          destructive: {
            backgroundColor: {
              _: {
                value: "{semantic.color.action.fill.negative._}",
              },

              hovered: {
                value: "{semantic.color.action.fill.negative.hovered}",
              },

              focused: {
                value: "{semantic.color.action.fill.negative.focused}",
              },

              pressed: {
                value: "{semantic.color.action.fill.negative.pressed}",
              },

              disabled: {
                value: "{semantic.color.action.fill.negative.disabled}",
              },
            },
          },
        },
      },
    },
  },
};
