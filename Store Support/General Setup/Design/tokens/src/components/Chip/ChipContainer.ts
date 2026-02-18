module.exports = {
  component: {
    chip: {
      container: {
        alignVertical: {
          value: "center",
        },

        backgroundColor: {
          _: {
            value: "{semantic.color.input.fill._}",
          },

          hovered: {
            value: "{semantic.color.input.fill.hovered}",
          },

          focused: {
            value: "{semantic.color.input.fill.focused}",
          },

          pressed: {
            value: "{semantic.color.input.fill.pressed}",
          },

          disabled: {
            value: "{semantic.color.input.fill.disabled}",
          },
        },

        borderColor: {
          _: {
            value: "{semantic.color.input.border._}",
          },

          hovered: {
            value: "{semantic.color.input.border.hovered}",
          },

          focused: {
            value: "{semantic.color.input.border.focused}",
          },

          pressed: {
            value: "{semantic.color.input.border.pressed}",
          },

          disabled: {
            value: "{semantic.color.input.border.disabled}",
          },
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.50}",
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

        paddingHorizontal: {
          value: "{primitive.scale.space.200}",
        },

        paddingVertical: {
          value: "0px",
        },

        size: {
          large: {
            height: {
              value: "{primitive.scale.space.500}",
            },
          },

          small: {
            height: {
              value: "{primitive.scale.space.400}",
            },
          },
        },

        state: {
          activated: {
            borderColor: {
              _: {
                value: "{semantic.color.input.border.activated._}",
              },

              hovered: {
                value: "{semantic.color.input.border.activated.hovered}",
              },

              focused: {
                value: "{semantic.color.input.border.activated.focused}",
              },

              pressed: {
                value: "{semantic.color.input.border.activated.pressed}",
              },

              disabled: {
                value: "{semantic.color.input.border.activated.disabled}",
              },
            },

            borderWidth: {
              _: {
                value: "{semantic.scale.border.width.interactive.activated._}",
              },

              hovered: {
                value:
                  "{semantic.scale.border.width.interactive.activated.hovered}",
              },

              focused: {
                value:
                  "{semantic.scale.border.width.interactive.activated.focused}",
              },

              pressed: {
                value:
                  "{semantic.scale.border.width.interactive.activated.pressed}",
              },

              disabled: {
                value: "{semantic.scale.border.width.interactive.activated._}",
              },
            },
          },
        },
      },
    },
  },
};
