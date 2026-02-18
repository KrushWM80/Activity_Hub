### StyledText

```js
import {StyledText, Icons} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;

<>
  <StyledText size="small" color="blue" leading={<Icons.CheckIcon />}>
    Blue small StyledText with Check Icon
  </StyledText>
  <StyledText size="small" color="green" leading={<Icons.CheckIcon />}>
    Green small StyledText with Check Icon
  </StyledText>
  <StyledText size="small" color="gray" leading={<Icons.CheckIcon />}>
    Gray small StyledText with Check Icon
  </StyledText>
  <Spacer />
  <StyledText size="large" color="blue" leading={<Icons.CheckIcon />}>
    Blue large StyledText with Check Icon
  </StyledText>
  <StyledText size="large" color="green" leading={<Icons.CheckIcon />}>
    Green large StyledText with Check Icon
  </StyledText>
  <StyledText size="large" color="gray" leading={<Icons.CheckIcon />}>
    Gray large StyledText with Check Icon
  </StyledText>
</>
```
