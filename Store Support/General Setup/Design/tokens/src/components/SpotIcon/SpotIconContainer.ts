module.exports = {
  component: {
    spotIcon: {
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

        color: {
          brand: {
            backgroundColor: {
              value: "{semantic.color.fill.brand.subtle}",
            },
          },

          neutral: {
            backgroundColor: {
              value: "{semantic.color.fill._}",
            },
          },
        },

        size: {
          small: {
            height: {
              value: "{primitive.scale.space.600}",
            },

            width: {
              value: "{primitive.scale.space.600}",
            },
          },

          large: {
            height: {
              value: "{primitive.scale.space.700}",
            },

            width: {
              value: "{primitive.scale.space.700}",
            },
          },
        },
      },
    },
  },
};
