module.exports = {
  component: {
    datePicker: {
      calendarContainer: {
        backgroundColor: {
          value: "{semantic.color.surface.overlay}",
        },

        borderRadius: {
          value: "{primitive.scale.border.radius.100}",
        },

        elevation: {
          value: "{semantic.elevation.200}",
        },

        minWidth: {
          value: "352px",
        },

        state: {
          enter: {
            opacity: {
              value: 0,
            },

            translateY: {
              value: ".8px",
            },
          },

          enterActive: {
            opacity: {
              value: 1,
            },

            translateY: {
              value: "0px",
            },

            opacityTransition: {
              transitionDuration: {
                value: "{primitive.duration.100}",
              },

              transitionProperty: {
                value: "opacity",
              },

              transitionTimingFunction: {
                value: "{primitive.timing.easeInOut.100}",
              },
            },

            transformTransition: {
              transitionDuration: {
                value: "{primitive.duration.100}",
              },

              transitionProperty: {
                value: "transform",
              },

              transitionTimingFunction: {
                value: "{primitive.timing.easeInOut.100}",
              },
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

            translateY: {
              value: ".8px",
            },

            opacityTransition: {
              transitionDuration: {
                value: "{primitive.duration.100}",
              },

              transitionProperty: {
                value: "opacity",
              },

              transitionTimingFunction: {
                value: "{primitive.timing.easeInOut.100}",
              },
            },

            transformTransition: {
              transitionDuration: {
                value: "{primitive.duration.100}",
              },

              transitionProperty: {
                value: "transform",
              },

              transitionTimingFunction: {
                value: "{primitive.timing.easeInOut.100}",
              },
            },
          },
        },
      },
    },
  },
};
