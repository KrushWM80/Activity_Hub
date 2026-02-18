module.exports = {
  component: {
    panel: {
      layoutContainer: {
        height: {
          value: "100%",
        },

        position: {
          left: {
            alignHorizontal: {
              value: "start",
            },

            paddingEnd: {
              value: "{primitive.scale.space.300}",
            },
          },

          right: {
            alignHorizontal: {
              value: "end",
            },

            paddingStart: {
              value: "{primitive.scale.space.300}",
            },
          },
        },

        width: {
          value: "fill-screen",
        },
      },
    },
  },
};
