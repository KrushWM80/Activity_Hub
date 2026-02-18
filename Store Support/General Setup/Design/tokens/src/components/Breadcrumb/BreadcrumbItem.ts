module.exports = {
  component: {
    breadcrumb: {
      item: {
        aliasName: {
          value: "text.body",
        },

        aliasOptions: {
          size: {
            value: "small",
          },
        },

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

        textDecoration: {
          value: "underline",
        },

        state: {
          isCurrent: {
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

            textDecoration: {
              value: "none",
            },
          },
        },
      },
    },
  },
};
