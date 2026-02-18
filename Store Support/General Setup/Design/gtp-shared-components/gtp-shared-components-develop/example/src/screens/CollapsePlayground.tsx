import * as React from 'react';
import {
  StyleSheet,
  SafeAreaView,
  ImageStyle,
  TextStyle,
  View,
} from 'react-native';
import {
  Icons,
  Checkbox,
  colors,
  Body,
  getFont,
  Collapse,
} from '@walmart/gtp-shared-components';
import {Header, Page, Section} from '../components';
const Spacer = () => <View style={ss.spacer} />;
type IconSize = 'small' | 16 | 'medium' | 24 | 'large' | 32;
const CollapsePlayground: React.FC = () => {
  type Traits = {
    title: string;
    subtitle?: string | undefined;
    icon?: boolean;
    dividerTop?: boolean;
    dividerBottom?: boolean;
    size?: IconSize;
    allow_icon_style?: boolean;
    allow_title_style?: boolean;
    allow_subTitle_style?: boolean;
  };
  const [traits, setTraits] = React.useState<Traits>({
    title: 'Collapse',
    subtitle: undefined,
    icon: false,
    dividerTop: false,
    dividerBottom: false,
    size: 24,
    allow_icon_style: false,
    allow_title_style: false,
    allow_subTitle_style: false,
  });
  const [isExpanded, setIsExpanded] = React.useState(false);
  const onToggle = () => {
    setIsExpanded(!isExpanded);
  };
  const getTitle = () => {
    const title = traits.title;
    if (traits.subtitle && traits.icon) {
      return `${title} with Subtitle & Icon`;
    } else if (traits.subtitle) {
      return `${title} with Subtitle`;
    } else if (traits.icon) {
      return `${title} with icon`;
    }
    return `${title}`;
  };
  return (
    <SafeAreaView style={ss.container}>
      <Page>
        <View key={'Template'}>
          <Header>Collapse</Header>
          <View style={ss.innerContainer}>
            <Collapse
              title={getTitle()}
              subtitle={traits.subtitle}
              expanded={isExpanded}
              icon={
                traits.icon ? <Icons.InfoCircleIcon size={24} /> : undefined
              }
              dividerTop={traits.dividerTop}
              dividerBottom={traits.dividerBottom}
              size={traits.size}
              icon_style={traits.allow_icon_style ? ss.icon_Style : {}}
              title_style={traits.allow_title_style ? ss.title_Style : {}}
              subTitle_style={
                traits.allow_subTitle_style ? ss.subtitle_Style : {}
              }
              onToggle={() => {
                onToggle();
              }}>
              <Body>Collapse content appears underneath the toggle area.</Body>
            </Collapse>
          </View>
        </View>

        <Section>
          <View style={ss.innerContainer}>
            <Checkbox
              label="With Subtitle"
              checked={!!traits.subtitle}
              onPress={() =>
                setTraits({
                  ...traits,
                  subtitle: traits.subtitle ? undefined : 'subTitle',
                })
              }
            />
            <Spacer />
            <Checkbox
              label="With icon"
              checked={traits.icon}
              onPress={() =>
                setTraits({
                  ...traits,
                  icon: !traits.icon,
                })
              }
            />
            <Spacer />
            <Checkbox
              label="with dividerTop"
              checked={traits.dividerTop}
              onPress={() =>
                setTraits({
                  ...traits,
                  dividerTop: !traits.dividerTop,
                })
              }
            />
            <Spacer />
            <Checkbox
              label="With dividerBottom"
              checked={traits.dividerBottom}
              onPress={() =>
                setTraits({
                  ...traits,
                  dividerBottom: !traits.dividerBottom,
                })
              }
            />
            <Spacer />
            <Checkbox
              label="With title_style"
              checked={!!traits.allow_title_style}
              onPress={() =>
                setTraits({
                  ...traits,
                  allow_title_style: !traits.allow_title_style,
                })
              }
            />
            <Spacer />
            <Checkbox
              label="With subtitle_style"
              checked={!!traits.allow_subTitle_style}
              onPress={() =>
                setTraits({
                  ...traits,
                  allow_subTitle_style: !traits.allow_subTitle_style,
                })
              }
            />
            <Spacer />
            <Checkbox
              label="With icon_style"
              checked={!!traits.allow_icon_style}
              onPress={() =>
                setTraits({
                  ...traits,
                  allow_icon_style: !traits.allow_icon_style,
                })
              }
            />
            <Spacer />
          </View>
        </Section>
      </Page>
    </SafeAreaView>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.gray['100'],
    height: '15%',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
    borderTopColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingRight: 16,
    paddingVertical: 8,
    marginTop: 20,
  },
  headerText: {
    fontSize: 20,
    fontWeight: '500',
    color: colors.blue['90'],
    textAlign: 'left',
    paddingVertical: 10,
    marginLeft: 12,
  },
  imageContainer: {
    backgroundColor: colors.gray['100'],
    borderRadius: 16,
    marginHorizontal: 16,
    paddingVertical: 16,
    marginTop: 8,
  },
  image: {
    width: '100%',
    resizeMode: 'contain',
  },
  innerContainer: {
    marginLeft: 16,
    padding: 8,
    justifyContent: 'flex-start',
  },
  spacer: {
    height: 8,
  },
  radioHeaderText: {
    color: colors.blue['90'],
  } as TextStyle,
  rbGroup: {
    marginLeft: 16,
  },
  icon_Style: {
    width: 36,
    height: 36,
  } as ImageStyle,
  title_Style: {
    ...getFont('bold'),
    fontSize: 16,
    lineHeight: 24,
    color: 'green',
  } as TextStyle,
  subtitle_Style: {
    ...getFont('bold'),
    fontSize: 16,
    lineHeight: 24,
    color: 'red',
  } as TextStyle,
});

export {CollapsePlayground};
