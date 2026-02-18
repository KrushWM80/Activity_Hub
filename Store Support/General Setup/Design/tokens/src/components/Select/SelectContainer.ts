module.exports = {
  component: {
    select: {
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
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.50}",
        },

        size: {
          small: {
            paddingEnd: {
              value: "36px",
            },

            paddingStart: {
              value: "{primitive.scale.space.150}",
            },

            paddingVertical: {
              value: "10px",
              comment:
                "This takes into account the extra 2px missed in figma: 8px + 2px = 10px",
            },
          },

          large: {
            paddingEnd: {
              value: "36px",
            },

            paddingStart: {
              value: "{primitive.scale.space.200}",
            },

            paddingVertical: {
              value: "{primitive.scale.space.200}",
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
