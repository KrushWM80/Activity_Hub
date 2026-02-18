module.exports = {
  component: {
    modal: {
      container: {
        backgroundColor: {
          value: "{semantic.color.surface.overlay}",
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.200}",
        },

        elevation: {
          value: "{semantic.elevation.300}",
        },

        size: {
          small: {
            maxWidth: {
              value: "400px",
            },
          },

          medium: {
            maxWidth: {
              value: "600px",
            },
          },

          large: {
            maxWidth: {
              value: "800px",
            },
          },
        },

        state: {
          enter: {
            opacity: {
              value: 0,
              comment: "TODO: figure this out",
            },

            scale: {
              value: 0,
              comment: "TODO: figure this out",
            },
          },

          enterActive: {
            opacityTransition: {
              transitionDuration: {
                value: "{primitive.duration.300}",
              },

              transitionProperty: {
                value: "opacity",
              },

              transitionTimingFunction: {
                value: "{primitive.timing.linear.100}",
              },
            },

            transformTransition: {
              transitionDuration: {
                value: "{primitive.duration.500}",
              },

              transitionProperty: {
                value: "transform",
              },

              transitionTimingFunction: {
                value: "{primitive.timing.easeOut.100}",
              },
            },

            opacity: {
              value: 1,
              comment: "TODO: figure this out",
            },

            scale: {
              value: 1,
              comment: "TODO: figure this out",
            },
          },

          exit: {
            opacity: {
              value: 1,
              comment: "TODO: figure this out",
            },

            scale: {
              value: 1,
              comment: "TODO: figure this out",
            },
          },

          exitActive: {
            transitionDuration: {
              value: "{primitive.duration.500}",
            },

            transitionProperty: {
              value: "opacity",
            },

            transitionTimingFunction: {
              value: "{primitive.timing.linear.100}",
            },

            opacity: {
              value: 0,
              comment: "TODO: figure this out",
            },
          },
        },
      },
    },
  },
};
