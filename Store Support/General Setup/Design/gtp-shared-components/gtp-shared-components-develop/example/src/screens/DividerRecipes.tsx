import * as React from 'react';
import {Header, Page, Section, VariantText} from '../components';
import {Divider} from '@walmart/gtp-shared-components';
import {Text} from 'react-native';

export const DividerRecipes: React.FC = () => {
  const dividerColor = ['#b36a16', '#590b0e', '#004f9a', '#1d5f02'];
  // ---------------
  // Rendering
  // ---------------
  return (
    <Page>
      <Header>
        Divider Recipes
        <VariantText>{` (default)`}</VariantText>
      </Header>
      <Section space={10}>
        {[1, 2, 3, 4].map((val, i) => (
          <React.Fragment key={i}>
            <Text key={val}>{`item-${val}`}</Text>
            <Divider key={`${val}-`} />
          </React.Fragment>
        ))}
      </Section>

      <Header>
        Divider Recipes
        <VariantText>{` (with UNSAFE_style)`}</VariantText>
      </Header>
      <Section space={10}>
        {[1, 2, 3, 4].map((val, i) => (
          <React.Fragment key={i}>
            <Text key={i}>{`item-${val}`}</Text>
            {
              <Divider
                key={val}
                UNSAFE_style={{backgroundColor: dividerColor[i], height: val}}
              />
            }
          </React.Fragment>
        ))}
      </Section>
    </Page>
  );
};
