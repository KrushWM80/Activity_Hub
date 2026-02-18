module.exports = {
  component: {
    snackbar: {
      container: {
        alignVertical: {
          value: "start",
        },

        backgroundColor: {
          value: "{semantic.color.fill.inverse}",
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.50}",
        },

        elevation: {
          value: "{semantic.elevation.300}",
        },

        maxWidth: {
          bS: {
            value: "343px",
          },

          bM: {
            value: "none",
            comment: "TODO: figure this out",
          },
        },

        paddingBottom: {
          bS: {
            value: "{primitive.scale.space.100}",
          },

          bM: {
            value: "{primitive.scale.space.200}",
          },
        },

        paddingHorizontal: {
          value: "{primitive.scale.space.200}",
        },

        paddingTop: {
          value: "0px",
        },

        state: {
          enter: {
            opacity: {
              value: 0,
            },
          },

          enterActive: {
            transitionDuration: {
              value: "{primitive.duration.500}",
            },

            transitionProperty: {
              value: "opacity",
            },

            transitionTimingFunction: {
              value: "ease-in",
            },

            opacity: {
              value: 1,
            },
          },

          exit: {
            opacity: {
              value: 1,
            },
          },

          exitActive: {
            transitionDuration: {
              attributes: {
                category: "time",
              },
              value: 750,
            },

            transitionProperty: {
              value: "opacity",
            },

            transitionTimingFunction: {
              value: "ease-in",
            },

            opacity: {
              value: 0,
            },
          },
        },
      },
    },
  },
};
