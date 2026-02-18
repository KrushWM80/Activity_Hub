module.exports = {
  component: {
    textField: {
      container: {
        backgroundColor: {
          _: {
            value: "{semantic.color.field.fill._}",
          },

          hovered: {
            value: "{semantic.color.field.fill.hovered}",
          },

          focused: {
            value: "{semantic.color.field.fill.focused}",
          },

          disabled: {
            value: "{semantic.color.field.fill.disabled}",
          },

          readOnly: {
            value: "{semantic.color.field.fill._}",
          },
        },

        borderColor: {
          _: {
            value: "{semantic.color.field.border._}",
          },

          hovered: {
            value: "{semantic.color.field.border.hovered}",
          },

          focused: {
            value: "{semantic.color.field.border.focused}",
          },

          disabled: {
            value: "{semantic.color.field.border.disabled}",
          },

          readOnly: {
            value: "{semantic.color.field.border._}",
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

          disabled: {
            value: "{semantic.scale.border.width.interactive._}",
          },

          readOnly: {
            value: "{semantic.scale.border.width.interactive._}",
          },
        },

        size: {
          large: {
            paddingHorizontal: {
              value: "{primitive.scale.space.200}",
            },

            paddingVertical: {
              value: "{primitive.scale.space.200}",
            },
          },

          small: {
            paddingHorizontal: {
              value: "{primitive.scale.space.150}",
            },

            paddingVertical: {
              value: "{primitive.scale.space.100}",
            },
          },
        },

        state: {
          error: {
            backgroundColor: {
              _: {
                value: "{semantic.color.field.fill.negative._}",
              },

              hovered: {
                value: "{semantic.color.field.fill.negative.hovered}",
              },

              focused: {
                value: "{semantic.color.field.fill.negative.focused}",
              },

              disabled: {
                value: "{semantic.color.field.fill.negative.disabled}",
              },

              readOnly: {
                value: "{semantic.color.field.fill._}",
              },
            },

            borderColor: {
              _: {
                value: "{semantic.color.field.border.negative._}",
              },

              hovered: {
                value: "{semantic.color.field.border.negative.hovered}",
              },

              focused: {
                value: "{semantic.color.field.border.negative.focused}",
              },

              disabled: {
                value: "{semantic.color.field.border.negative.disabled}",
              },

              readOnly: {
                value: "{semantic.color.field.border._}",
              },
            },
          },

          isMagic: {
            borderColor: {
              _: {
                value: "{semantic.color.field.border.magic._}",
              },

              hovered: {
                value: "{semantic.color.field.border.magic.hovered}",
              },

              focused: {
                value: "{semantic.color.field.border.magic.focused}",
              },
            },
          },

          hasLeadingIcon: {
            size: {
              small: {
                paddingStart: {
                  value: "44px",
                },
              },

              large: {
                paddingStart: {
                  value: "52px",
                },
              },
            },
          },
        },
      },
    },
  },
};
