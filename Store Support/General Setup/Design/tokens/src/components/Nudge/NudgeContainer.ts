module.exports = {
  component: {
    nudge: {
      container: {
        alignVertical: {
          value: "start",
        },

        backgroundColor: {
          value: "{semantic.color.surface.brand}",
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.100}",
        },

        paddingHorizontal: {
          value: "{primitive.scale.space.200}",
        },

        paddingVertical: {
          value: "{primitive.scale.space.200}",
        },

        state: {
          hasCloseButton: {
            paddingEnd: {
              value: "0px",
            },
          },

          hasNoContent: {
            alignVertical: {
              value: "center",
            },
          },
        },
      },
    },
  },
};
