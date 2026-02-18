module.exports = {
  component: {
    bottomSheet: {
      container: {
        backgroundColor: {
          value: "{semantic.color.surface.overlay}",
        },

        borderRadiusTopEnd: {
          value: "{primitive.scale.border.radius.200}",
        },

        borderRadiusTopStart: {
          value: "{primitive.scale.border.radius.200}",
        },

        elevation: {
          value: "{semantic.elevation.300}",
        },

        maxWidth: {
          value: "768px",
        },

        state: {
          enter: {
            translateY: {
              value: "100%",
              comment: "TODO: figure this out.",
            },
          },

          enterActive: {
            transitionDuration: {
              attributes: {
                category: "time",
              },
              value: 900,
            },

            transitionProperty: {
              value: "transform",
            },

            transitionTimingFunction: {
              value: "{primitive.timing.easeOut.100}",
            },

            translateY: {
              value: "none",
              comment: "TODO: figure this out.",
            },
          },

          exit: {
            translateY: {
              value: "none",
              comment: "TODO: figure this out.",
            },
          },

          exitActive: {
            transitionDuration: {
              value: "{primitive.duration.500}",
            },

            transitionProperty: {
              value: "transform",
            },

            transitionTimingFunction: {
              value: "{primitive.timing.easeIn.100}",
            },

            translateY: {
              value: "100%",
              comment: "TODO: figure this out.",
            },
          },
        },

        width: {
          value: "fill-parent",
        },
      },
    },
  },
};
