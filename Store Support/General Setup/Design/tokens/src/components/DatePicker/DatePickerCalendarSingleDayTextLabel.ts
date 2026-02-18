module.exports = {
  component: {
    datePicker: {
      calendarSingleDayTextLabel: {
        aliasName: {
          value: "text.body",
        },

        aliasOptions: {
          size: {
            value: "small",
          },
        },

        state: {
          isSelected: {
            textColor: {
              _: {
                value: "{semantic.color.text.onFill.activated._}",
              },

              disabled: {
                value: "{semantic.color.text.onFill.activated.disabled}",
              },
            },
          },
        },

        textColor: {
          _: {
            value: "{semantic.color.text.onFill.activated.subtle._}",
          },

          disabled: {
            value: "{semantic.color.text.onFill.activated.subtle.disabled}",
          },
        },
      },
    },
  },
};
