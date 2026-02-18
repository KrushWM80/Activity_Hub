module.exports = {
  component: {
    dataTable: {
      headerIcon: {
        alignment: {
          left: {
            marginStart: {
              value: "{primitive.scale.space.50}",
            },
          },

          right: {
            marginEnd: {
              value: "{primitive.scale.space.50}",
            },
          },
        },

        iconColor: {
          value: "{semantic.color.text.subtle}",
        },

        iconSize: {
          value: "small",
        },

        sort: {
          ascending: {
            iconColor: {
              value: "{semantic.color.text._}",
            },

            iconName: {
              value: "ArrowUp",
              themable: true,
            },

            visibility: {
              value: "visible",
            },
          },

          descending: {
            iconColor: {
              value: "{semantic.color.text._}",
            },

            iconName: {
              value: "ArrowDown",
              themable: true,
            },

            visibility: {
              value: "visible",
            },
          },
        },

        visibility: {
          _: {
            value: "hidden",
            themable: true,
          },

          hovered: {
            value: "visible",
          },

          focused: {
            value: "visible",
          },
        },
      },
    },
  },
};
