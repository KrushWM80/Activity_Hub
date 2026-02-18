import * as React from 'react';
import {View, StyleSheet, Alert, Image} from 'react-native';
import {
  SupportiveText,
  FilledFlag,
  Flag,
  Button,
  colors,
  Icons,
  Link,
  Badge,
  IconButton,
  RollbackFlag,
  Body,
  Divider,
  TextField,
} from '@walmart/gtp-shared-components';

const ss = StyleSheet.create({
  button: {
    margin: 8,
  },
  body: {
    fontStyle: 'normal',
    color: 'blue',
  },
  normal: {
    fontStyle: 'normal',
  },
  bullet: {
    marginTop: 9,
    height: 10,
    width: 10,
    borderRadius: 5,
    backgroundColor: colors.gray['100'],
  },
  badge: {
    marginLeft: 8,
  },
  longBottomSheet: {
    width: '90%',
  },
  LongBottomSheetImageContainer: {
    width: '100%',
    marginTop: 16,
  },
  LongBottomSheetImage: {
    marginRight: 16,
    alignSelf: 'center',
  },
});

const carouselHeader = {
  title: 'Carousel With All Features',
  subtitle: 'Carousel Subtitle',
  link: 'Carousel Link',
  onLinkPress: () => {},
};

const carouselFooter = {
  total: 12.0,
  link: 'Link Text',
  onLinkPress: () => {},
  button: (
    <Button variant="primary" size="small" onPress={() => {}}>
      Button Text
    </Button>
  ),
};

const carouselItems = [
  {
    id: 'Item_1',
    flag: <FilledFlag>Walmart's Pick</FilledFlag>,
    imageSource: 'http://via.placeholder.com/150',
    price: 10,
    wasPrice: 11,
    eachPrice: 1,
    weightLabel: true,
    name: 'Etiam porta sem malesuada magna mollis Etiam porta sem malesuada magna mollis ',
    ratings: {
      value: 3,
      count: 5,
      onPress: () => {},
    },
    outOfStock: true,
    availabilityBadge: 'Today',
    mediaBadge: 'PG-13',
    link: 'Link here',
    onLinkPress: () => {},
  },
  {
    id: 'Item_2',
    flag: (
      <SupportiveText
        color={colors.blue['120']}
        icon={<Icons.CheckIcon size={12} />}>
        Bought Before
      </SupportiveText>
    ),
    imageSource: 'http://via.placeholder.com/100x150',
    price: 100,
    eachPrice: 60,
    name: 'Etiam porta sem malesuada magna mollis Etiam porta sem malesuada magna mollis ',
    ratings: {
      value: 1.5,
      count: 50,
    },
    outOfStock: true,
  },
  {
    id: 'Item_3',
    flag: <RollbackFlag>Rollback</RollbackFlag>,
    imageSource: 'http://via.placeholder.com/150x100',
    price: 10,
    name: 'Etiam porta sem malesuada magna mollis Etiam porta sem malesuada magna mollis ',
    availabilityBadge: 'Tomorrow',
  },
  {
    id: 'Item_4',
    flag: <Flag>Best Seller</Flag>,
    imageSource: 'http://via.placeholder.com/250',
    price: 10,
    name: 'Etiam porta sem malesuada magna mollis Etiam porta sem malesuada magna mollis ',
  },
  {
    id: 'Item_5',
    imageSource: 'http://via.placeholder.com/250',
    price: 10,
    name: 'Etiam porta sem malesuada magna mollis Etiam porta sem malesuada magna mollis ',
  },
];

const LongBottomSheetContent = ({close}: {close: () => void}) => (
  <View style={ss.longBottomSheet}>
    <Body>
      <Body weight="medium">You won’t get NextDay delivery</Body> on this order
      because your cart contains item(s) that aren’t “NextDay eligible.” If you
      want NextDay, we can save the other items for later.
    </Body>
    <Button
      UNSAFE_style={ss.button}
      variant="primary"
      isFullWidth
      onPress={close}>
      Yes—Save my other items for later
    </Button>
    <Button
      UNSAFE_style={ss.button}
      variant="secondary"
      isFullWidth
      onPress={close}>
      No—I want to keep shopping
    </Button>
    <Divider />
    <Body>For example:</Body>
    <Body>
      <Body weight="medium" UNSAFE_style={ss.body}>
        NextDay
      </Body>{' '}
      +
      <Body weight="medium" UNSAFE_style={ss.body}>
        {' '}
        NextDay
      </Body>{' '}
      =
      <Body weight="medium" UNSAFE_style={ss.body}>
        {' '}
        NextDay
      </Body>
      !
    </Body>
    <Body>
      <Body weight="medium" UNSAFE_style={ss.body}>
        NextDay
      </Body>{' '}
      +
      <Body weight="medium" UNSAFE_style={ss.normal}>
        {' '}
        2Day
      </Body>{' '}
      =
      <Body weight="medium">
        <Body UNSAFE_style={ss.normal}> 2Day</Body> on entire order
      </Body>
    </Body>
    <Divider />
    <View style={ss.LongBottomSheetImageContainer}>
      <Image
        source={{
          uri: 'https://gecgithub01.walmart.com/storage/user/67415/files/f9a3519d-45a9-437a-b41c-27d6cd1152b1',
          height: 300,
          width: 300,
        }}
        style={ss.LongBottomSheetImage}
      />
      <Body weight="medium">{loremIpsum(3)}</Body>
    </View>
    <TextField
      label="This is the label"
      placeholder="Placeholder text"
      helperText="Helper text"
      onChangeText={() => {}}
    />
  </View>
);

const ShortBottomSheetContent = ({close}: {close: () => void}) => (
  <View>
    <Body>This is a small bit of content.</Body>
    <Button variant="secondary" isFullWidth onPress={close}>
      Close
    </Button>
  </View>
);

const sizes = {
  XS: 'Extra Small',
  S: 'Small',
  M: 'Medium',
  L: 'Large',
  XL: 'Extra Large',
  '2XL': '2XL',
  '3XL': '3XL',
};

const sizesList = Object.values(sizes);

const _sizesObjects = (sizeObj: typeof sizes) => {
  return Object.keys(sizes).map(key => {
    return {label: sizeObj[key as keyof typeof sizeObj], id: key};
  });
};

const sizesObjects = _sizesObjects(sizes);

const itemsForSimpleList = [
  {
    title: 'List Item Title 2',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor',
    leading: <Icons.InfoCircleIcon size={24} />,
    trailing: (
      <Link onPress={() => displayPopupAlert('Action', 'Action Link Pressed')}>
        Action1
      </Link>
    ),
  },
  {
    title: 'List Item Title 3',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor',
    leading: <Icons.InfoCircleIcon size={24} />,
    trailing: (
      <IconButton
        children={<Icons.ChevronRightIcon />}
        size="small"
        onPress={() => displayPopupAlert('Action', 'icon button pressed')}
      />
    ),
  },
];
const displayPopupAlert = (title: string, message: string) => {
  Alert.alert(title, message);
};
const formGroupCheckbox = [
  {
    id: 1,
    label: 'Sourdough',
  },
  {
    id: 2,
    label: 'Wheat',
  },
  {
    id: 3,
    label: 'Rye',
  },
];
const formGroupRadio = [
  {
    id: 1,
    label: 'Banana',
  },
  {
    id: 2,
    label: 'Vanilla',
  },
  {
    id: 3,
    label: 'Mango',
  },
  {
    id: 4,
    label: 'Banana Khajur',
  },
  {
    id: 5,
    label: 'Chocolate ',
  },
  {
    id: 6,
    label: 'Strawberry',
  },
  {
    id: 7,
    label: 'Chocolate-Banana',
  },
  {
    id: 8,
    label: 'Cookies and Cream ',
  },
];
const tabs = {
  withLeadingTrailing: [
    {
      leading: <Icons.CartIcon />,
      trailing: (
        <Badge color="blue" UNSAFE_style={ss.badge}>
          10
        </Badge>
      ),
      label: 'One',
    },
    {
      leading: <Icons.BoxIcon />,
      trailing: (
        <Badge color="gray" UNSAFE_style={ss.badge}>
          20
        </Badge>
      ),
      label: 'Two',
    },
  ],
  withLeading: [
    {
      leading: <Icons.CartIcon />,
      label: 'One',
    },
    {
      leading: <Icons.BoxIcon />,
      label: 'Two',
    },
    {
      leading: <Icons.ReceiptIcon />,
      label: 'Three',
    },
    {
      leading: <Icons.FlagIcon />,
      label: 'Four',
    },
  ],
  withTrailing: [
    {
      trailing: (
        <Badge color="blue" UNSAFE_style={ss.badge}>
          10
        </Badge>
      ),
      label: 'One',
    },
    {
      trailing: (
        <Badge color="gray" UNSAFE_style={ss.badge}>
          20
        </Badge>
      ),
      label: 'Two',
    },
    {
      trailing: (
        <Badge color="green" UNSAFE_style={ss.badge}>
          30
        </Badge>
      ),
      label: 'Three',
    },
  ],
  labelOnly: [
    {
      label: 'One',
    },
    {
      label: 'Two',
    },
    {
      label: 'Three',
    },
    {
      leading: <Icons.BoxIcon />,
      label: 'Four',
    },
    {
      label: 'Five',
    },
    {
      label: 'Six',
    },
    {
      leading: <Icons.ReceiptIcon />,
      trailing: (
        <Badge color="green" UNSAFE_style={ss.badge}>
          30
        </Badge>
      ),
      label: 'Seven',
    },
    {
      label: 'Eight',
    },
    {
      trailing: (
        <Badge color="green" UNSAFE_style={ss.badge}>
          30
        </Badge>
      ),
      label: 'Nine',
    },
    {
      label: 'Ten',
    },
  ],
};

const segments = [
  {
    index: 0,
    label: 'First',
  },
  {
    index: 1,
    label: 'Second',
  },
  {
    index: 2,
    label: 'Third',
  },
];

const loremIpsum = (repeat: number) => {
  const lIpsum =
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.';
  const result = [...Array(repeat).keys()].map(() => {
    return lIpsum;
  });
  return result.join('');
};
const dataTable = {
  rightAlignLabel: ['Count', 'Actions', 'Quantity (lb)', 'Quantity'],
  sortLabel: ['Name', 'Quantity (lb)'],
  autoHorizontalHeader: ['ID', 'Name', 'itemName', 'Count', 'Quantity', 'Date'],
  autoHorizontalData: [
    {
      id: 1,
      name: 'Banana',
      itemName: 'Organic Bananas, Bunch',
      count: 15,
      quantity: '3kg',
      date: '19/10/2022',
    },
    {
      id: 2,
      name: 'Peach',
      itemName: 'Organic Tomato, Bunch',
      count: 12,
      quantity: '3kg',
      date: '19/10/2022',
    },
    {
      id: 3,
      name: 'Strawberry',
      itemName: 'Organic Apple, Bunch',
      count: 9,
      quantity: '3kg',
      date: '19/10/2022',
    },
    {
      id: 4,
      name: 'Peach',
      itemName: 'Fresh Strawberries, 1 lb',
      count: 12,
      quantity: '3kg',
      date: '19/10/2022',
    },
    {
      id: 5,
      name: 'Strawberry',
      itemName: 'Market side Caesar Salad Kit, 11.55 oz',
      count: 9,
      quantity: '3kg',
      date: '19/10/2022',
    },
    {
      id: 6,
      name: 'Peach',
      itemName: 'Fresh Pear, 2 lb',
      count: 12,
      quantity: '3kg',
      date: '19/10/2022',
    },
    {
      id: 7,
      name: 'Strawberry',
      itemName: 'Market side Caesar Salad Kit, 11.55 oz',
      count: 9,
      quantity: '3kg',
      date: '19/10/2022',
    },
  ],
  simpleHeader: ['ID', 'Name', 'Count'],
  simpleData: [
    {id: 1, name: 'Banana', count: '75'},
    {id: 2, name: 'Peach', count: '0'},
    {id: 3, name: 'Strawberry', count: '9'},
  ],
  selectHeader: ['ID', 'Name'],
  selectData: [
    {id: 1, name: 'Banana'},
    {id: 2, name: 'Peach'},
    {id: 3, name: 'Strawberry'},
  ],
  actionHeader: ['ID', 'Name', 'Actions'],
  actionData: [
    {id: 1, name: 'Banana', isEdit: false},
    {id: 2, name: 'Peach', isEdit: false},
    {id: 3, name: 'Strawberry', isEdit: false},
  ],
  menuHeader: ['ID', 'Name', 'Actions'],
  menuData: [
    {id: 1, name: 'Banana', isEdit: false},
    {id: 2, name: 'Peach', isEdit: false},
    {id: 3, name: 'Strawberry', isEdit: false},
    {id: 4, name: 'Pineapple', isEdit: false},
    {id: 5, name: 'Avocado', isEdit: false},
    {id: 6, name: 'Melon', isEdit: false},
    {id: 7, name: 'Lemon', isEdit: false},
    {id: 8, name: 'Orange', isEdit: false},
    {id: 9, name: 'Kiwi', isEdit: false},
    {id: 10, name: 'Nectarine', isEdit: false},
  ],
  statusHeader: ['Name', 'Status'],
  statusData: [
    {id: 1, name: 'Freyja Atli', status: 'Healthy'},
    {id: 2, name: 'Borghildr Sigurdr', status: 'Upset stomach'},
    {id: 3, name: 'Brynhild Idun', status: 'Unamused'},
  ],
  scrollHeader: ['Item number', 'Item name', 'Quantity (lb)', 'Delivery date'],
  scrollData: [
    {
      itemNumber: 51259338,
      itemName: 'Organic Bananas, Bunch',
      quantity: '24,500',
      dDate: 'Oct 5, 2022',
    },
    {
      itemNumber: 51259339,
      itemName: 'Organic Tomato, Bunch',
      quantity: '2,300',
      dDate: 'Oct 5, 2022',
    },
    {
      itemNumber: 51259349,
      itemName: 'Organic Apple, Bunch',
      quantity: '2,000',
      dDate: 'Oct 5, 2022',
    },
    {
      itemNumber: 44391605,
      itemName: 'Fresh Strawberries, 1 lb',
      quantity: '13,758',
      dDate: 'Oct 10, 2022',
    },
    {
      itemNumber: 44391615,
      itemName: 'Fresh Pear, 2 lb',
      quantity: '3,758',
      dDate: 'Oct 14, 2022',
    },
    {
      itemNumber: 16935784,
      itemName: 'Market side Caesar Salad Kit, 11.55 oz',
      quantity: '4,893',
      dDate: 'Oct 7, 2022',
    },
    {
      itemNumber: 16935786,
      itemName: 'Market side Caesar Salad Kit, 15.55 oz',
      quantity: '5,893',
      dDate: 'Oct 7, 2022',
    },
    {
      itemNumber: 16935787,
      itemName: 'Market side Caesar Salad Kit, 11.55 oz',
      quantity: '4,893',
      dDate: 'Oct 19, 2022',
    },
    {
      itemNumber: 16935788,
      itemName: 'Market side Caesar Salad Kit, 15.55 oz',
      quantity: '5,893',
      dDate: 'Oct 19, 2022',
    },
  ],
};

const menus = {
  bottomLeft: [
    {
      id: 1,
      leading: <Icons.GlobeIcon />,
      label: 'Activate transporter',
    },
    {
      id: 2,
      leading: <Icons.SearchIcon />,
      label: 'Engage tractor beam',
    },
    {
      id: 3,
      leading: <Icons.PhoneIcon />,
      label: 'Open a channel',
    },
  ],
  bottomRight: [
    {
      id: 1,
      leading: <Icons.PencilIcon />,
      label: 'Edit',
    },
    {
      id: 2,
      leading: <Icons.CloudDownloadIcon />,
      label: 'Download',
    },
    {
      id: 3,
      leading: <Icons.TrashCanIcon />,
      label: 'Delete',
    },
  ],
  topLeft: [
    {
      id: 1,
      leading: <Icons.PhoneIcon />,
      label: 'Call back',
    },
    {
      id: 2,
      leading: <Icons.StarIcon />,
      label: 'Save',
    },
    {
      id: 3,
      leading: <Icons.TrashCanIcon />,
      label: 'Delete',
    },
  ],
  topRight: [
    {
      id: 1,
      leading: <Icons.PencilIcon />,
      label: 'Edit',
    },
    {
      id: 2,
      leading: <Icons.RefreshIcon />,
      label: 'Refresh',
    },
    {
      id: 3,
      leading: <Icons.TrashCanIcon />,
      label: 'Delete',
    },
  ],
};
const miniAppListData = [
  {
    id: 1,
    isReturnable: true,
    isSelected: true,
    productName: '2PK 60L SURG',
    displayUpc: '681131311809',
    isReturned: false,
    currencyAmount: '$10.88',
  },
  {
    id: 2,
    isReturnable: true,
    isSelected: false,
    productName: 'GV SC CT CHS',
    displayUpc: '8809609924821',
    isReturned: false,
    currencyAmount: '$1.76',
  },
  {
    id: 3,
    isReturnable: false,
    isSelected: false,
    productName: '2PK 60L SURG',
    displayUpc: '681131311908',
    isReturned: false,
    currencyAmount: '$10.88',
  },
  {
    id: 4,
    isReturnable: true,
    isSelected: false,
    productName: '2PK CLR BULB',
    displayUpc: '844702085985',
    isReturned: true,
    currencyAmount: '$9.00',
  },
  {
    id: 5,
    isReturnable: true,
    isSelected: false,
    productName: 'SOUR CREAM',
    displayUpc: '0734200161142',
    isReturned: true,
    currencyAmount: '$9.00',
  },
  {
    id: 6,
    isReturnable: true,
    isSelected: false,
    productName: 'MILK',
    displayUpc: '0734200161143',
    isReturned: false,
    currencyAmount: '$5.00',
  },
  {
    id: 7,
    isReturnable: true,
    isSelected: false,
    productName: 'HONEY',
    displayUpc: '0734200161144',
    isReturned: false,
    currencyAmount: '$6.00',
  },
];
const alertRecipeData = [
  {TaskName: 'PAYMENT'},
  {
    TaskName: 'I-9',
    alertContent:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
  },
  {TaskName: 'GEAR'},
  {TaskName: 'BENEFITS_CONSENT', alertContent: 'Activate Benefits Consent'},
];
export {
  carouselHeader,
  carouselFooter,
  carouselItems,
  LongBottomSheetContent,
  ShortBottomSheetContent,
  loremIpsum,
  sizes,
  sizesList,
  sizesObjects,
  itemsForSimpleList,
  displayPopupAlert,
  formGroupCheckbox,
  formGroupRadio,
  tabs,
  segments,
  menus,
  dataTable,
  miniAppListData,
  alertRecipeData,
};
