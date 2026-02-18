import * as React from 'react';

class SimpleState {
  [key: string]: string | boolean | number | undefined | null;
}

const genericReducer = <S extends SimpleState>(
  state: S,
  action: {
    type: string;
    payload: S[string];
  },
) => {
  switch (action.type) {
    case action.type:
      return {
        ...state,
        [action.type]: action.payload,
      };
    default:
      return {...state};
  }
};

const useSimpleReducer = <S extends SimpleState>(
  initialState: S,
): [
  state: SimpleState,
  setState: (type: string, payload: S[keyof S]) => void,
] => {
  const [state, dispatch] = React.useReducer(genericReducer, initialState);

  const setState = React.useCallback(
    (type: string, payload: S[keyof S]) =>
      dispatch({
        type,
        payload,
      }),
    [],
  );

  return [state, setState];
};

export {useSimpleReducer};
