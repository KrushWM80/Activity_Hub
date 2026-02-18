module.exports = {
  component: {
    callout: {
      container: {
        backgroundColor: {
          value: "{semantic.color.fill.inverse}",
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.50}",
        },

        elevation: {
          value: "{semantic.elevation.200}",
        },

        paddingVertical: {
          value: "{primitive.scale.space.200}",
        },

        state: {
          enter: {
            opacity: {
              value: 0,
            },

            position: {
              bottom: {
                translateY: {
                  value: "100px",
                },
              },

              left: {
                translateX: {
                  value: "-100px",
                },
              },

              right: {
                translateX: {
                  value: "100px",
                },
              },

              top: {
                translateY: {
                  value: "-100px",
                },
              },
            },
          },

          enterActive: {
            opacity: {
              value: 1,
            },

            opacityTransition: {
              transitionDuration: {
                value: "{primitive.duration.200}",
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
                value: "{primitive.duration.200}",
              },

              transitionProperty: {
                value: "transform",
              },

              transitionTimingFunction: {
                value: "{primitive.timing.easeOut.100}",
              },
            },
          },

          exit: {
            opacity: {
              value: 1,
            },
          },

          exitActive: {
            opacity: {
              value: 0,
            },

            transitionDuration: {
              value: "{primitive.duration.200}",
            },

            transitionProperty: {
              value: "opacity",
            },

            transitionTimingFunction: {
              value: "{primitive.timing.easeIn.100}",
            },
          },
        },

        width: {
          value: "213px",
        },
      },
    },
  },
};
