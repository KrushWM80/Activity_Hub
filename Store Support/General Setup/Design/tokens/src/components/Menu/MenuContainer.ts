module.exports = {
  component: {
    menu: {
      container: {
        backgroundColor: {
          value: "{semantic.color.surface.overlay}",
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.50}",
        },

        elevation: {
          value: "{semantic.elevation.300}",
        },

        paddingHorizontal: {
          value: "0px",
        },

        paddingVertical: {
          value: "{primitive.scale.space.100}",
        },

        state: {
          enter: {
            opacity: {
              value: 0,
            },

            position: {
              bottom: {
                translateY: {
                  value: "-8px",
                },
              },

              top: {
                translateY: {
                  value: "8px",
                },
              },
            },
          },

          enterActive: {
            opacity: {
              value: 1,
            },

            transitionDuration: {
              value: "{primitive.duration.100}",
            },

            transitionProperty: {
              value: "all",
            },

            transitionTimingFunction: {
              value: "{primitive.timing.easeOut.100}",
            },

            translateY: {
              value: "0px",
            },
          },

          exit: {
            opacity: {
              value: 1,
            },

            translateY: {
              value: "0px",
            },
          },

          exitActive: {
            opacity: {
              value: 0,
            },

            position: {
              bottom: {
                translateY: {
                  value: "-8px",
                },
              },

              top: {
                translateY: {
                  value: "8px",
                },
              },
            },

            transitionDuration: {
              value: "{primitive.duration.100}",
            },

            transitionProperty: {
              value: "all",
            },

            transitionTimingFunction: {
              value: "{primitive.timing.easeOut.100}",
            },
          },
        },
      },
    },
  },
};
