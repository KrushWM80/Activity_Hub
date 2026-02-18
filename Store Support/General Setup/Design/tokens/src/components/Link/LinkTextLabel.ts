module.exports = {
  component: {
    link: {
      textLabel: {
        color: {
          default: {
            textColor: {
              _: {
                value: "{semantic.color.link.text._}",
              },

              hovered: {
                value: "{semantic.color.link.text.hovered}",
              },

              focused: {
                value: "{semantic.color.link.text.focused}",
              },

              pressed: {
                value: "{semantic.color.link.text.pressed}",
              },
            },
          },

          subtle: {
            textColor: {
              _: {
                value: "{semantic.color.link.text.subtle._}",
              },

              hovered: {
                value: "{semantic.color.link.text.subtle.hovered}",
              },

              focused: {
                value: "{semantic.color.link.text.subtle.focused}",
              },

              pressed: {
                value: "{semantic.color.link.text.subtle.pressed}",
              },
            },
          },

          white: {
            textColor: {
              _: {
                value: "{semantic.color.link.text.accent.white._}",
              },

              hovered: {
                value: "{semantic.color.link.text.accent.white.hovered}",
              },

              focused: {
                value: "{semantic.color.link.text.accent.white.focused}",
              },

              pressed: {
                value: "{semantic.color.link.text.accent.white.pressed}",
              },
            },
          },
        },

        fontFamily: {
          value: "{primitive.font.family.sans}",
        },

        fontWeight: {
          value: "{primitive.font.weight.400}",
        },

        textDecoration: {
          _: {
            value: "underline",
          },

          hovered: {
            value: "none",
          },

          focused: {
            value: "none",
          },

          pressed: {
            value: "none",
          },
        },
      },
    },
  },
};
