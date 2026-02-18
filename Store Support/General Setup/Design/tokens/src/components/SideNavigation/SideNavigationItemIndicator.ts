module.exports = {
  component: {
    sideNavigation: {
      itemIndicator: {
        backgroundColor: {
          value: "{semantic.color.pageNav.indicator.activated._}",
        },

        borderRadiusBottomEnd: {
          value: "{primitive.scale.border.radius.round}",
        },

        borderRadiusTopEnd: {
          value: "{primitive.scale.border.radius.round}",
        },

        height: {
          value: "100%",
        },

        offsetBottom: {
          value: "{primitive.scale.space.50}",
        },

        offsetTop: {
          value: "{primitive.scale.space.50}",
        },

        opacity: {
          value: 0,
          comment: "TODO: figure this out",
        },

        state: {
          activated: {
            opacity: {
              value: 1,
              comment: "TODO: figure this out",
            },
          },
        },

        width: {
          value: "{primitive.scale.space.50}",
        },
      },
    },
  },
};
