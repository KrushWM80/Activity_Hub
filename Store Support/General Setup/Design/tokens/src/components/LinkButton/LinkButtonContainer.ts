module.exports = {
  component: {
    linkButton: {
      container: {
        alignHorizontal: {
          value: "center",
        },

        alignVertical: {
          value: "center",
        },

        gap: {
          value: "{primitive.scale.space.100}",
        },

        size: {
          large: {
            height: {
              value: "{primitive.scale.space.600}",
            },
          },

          medium: {
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
          isFullWidth: {
            width: {
              value: "fill-parent",
            },
          },
        },
      },
    },
  },
};
