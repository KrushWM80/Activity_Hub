---
to: src/next/components/__tests__/<%= componentName %>.test.tsx
unless_exists: true
---

import * as React from 'react';

import {render, screen} from '@testing-library/react-native';

import {<%= componentName %>} from '../<%= componentName %>';

describe('<%= componentName %>', () => {
  test('renders <%= componentName %> component successfully', () => {
    render(<<%= componentName %> size="small" />);
    const element = screen.getByTestId('<%= componentName %>');
    expect(element).toBeDefined();
  });
});
