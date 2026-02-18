### SeeDetails default

```js
import {SeeDetails,Body} from '@walmart/gtp-shared-components';

const [isExpand,setIsExpand] = React.useState(false);

const Spacer = () => <View style={{height: 8}} />;

 <>
 <SeeDetails
    expanded={isExpand}
    onToggle={() => setIsExpand(!isExpand)}>
            <Body>See Details Content appears above the toggle area.</Body>
</SeeDetails>
 </>
```
### SeeDetails with Custom heading and dividers

```js
import {SeeDetails,Body} from '@walmart/gtp-shared-components';

const [isExpand,setIsExpand] = React.useState(false);

const Spacer = () => <View style={{height: 8}} />;

 <>
 <SeeDetails
    showText="Show My Content"
    hideText="Hide My Content"
    dividerTop
    dividerBottom
    expanded={isExpand}
    onToggle={() => setIsExpand(!isExpand)}>
            <Body>See Details Content appears above the toggle area.</Body>
</SeeDetails>
 </>
```