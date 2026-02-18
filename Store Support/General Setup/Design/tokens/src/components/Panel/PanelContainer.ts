module.exports = {
  component: {
    panel: {
      container: {
        backgroundColor: {
          value: "{semantic.color.surface.overlay}",
        },

        elevation: {
          value: "{semantic.elevation.300}",
        },

        position: {
          left: {
            state: {
              enter: {
                translateX: {
                  value: "-100%",
                },
              },

              enterActive: {
                translateX: {
                  value: "none",
                },
              },

              exit: {
                translateX: {
                  value: "none",
                },
              },

              exitActive: {
                translateX: {
                  value: "-100%",
                },
              },
            },
          },

          right: {
            state: {
              enter: {
                translateX: {
                  value: "100%",
                },
              },

              enterActive: {
                translateX: {
                  value: "none",
                },
              },

              exit: {
                translateX: {
                  value: "none",
                },
              },

              exitActive: {
                translateX: {
                  value: "100%",
                },
              },
            },
          },
        },

        size: {
          small: {
            maxWidth: {
              value: "320px",
            },
          },

          medium: {
            maxWidth: {
              value: "420px",
            },
          },

          large: {
            maxWidth: {
              value: "600px",
            },
          },
        },

        state: {
          enterActive: {
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

          exitActive: {
            transitionDuration: {
              value: "{primitive.duration.300}",
            },

            transitionProperty: {
              value: "transform",
            },

            transitionTimingFunction: {
              value: "{primitive.timing.easeOut.100}",
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
