# ui.xml documentation
The ```ui.xml``` file defines the user interface that is integrated into iRC / CPRog.

The user interface currently consists of three parts:
* Ribbon - the tool bar above the 3D view
* Main - the section that can be shown instead of or next to the 3D view
* App functions in program editor - these are defined in [rcapp.xml](rcapp.xml.md)

You do not need to define a user interface. If you define a user interface you must define a ribbon (can be empty), the main section is optional.

This example shows the structure and most element types. Notethe ribbon definition at the top and the main definition below.
```xml
<?xml version="1.0"?>
<ui>
	<!-- app ribbon at the top of iRC -->
	<ribbon label="Sample App"> <!-- Enter the app name here -->
		<group label="Buttons">
			<button name="buttonFoo" label="Foo" />
			<button name="buttonBar" label="Bar" />
			<toggle name="checkboxBaz" label="Baz" />
		</group>
	</ribbon>
	<!-- main app ui section in iRC -->
	<main>
		<group name="group1" label="Some UI elements">
			<text name="textSample" label="This is a text" />
			<textbox name="textboxSample" value="Enter something" label="Text Box" />
			<numberbox name="numberboxSample" value="123.456" label="Number Box" />
			<combobox name="comboboxSample" value="Choose something" label="Algorithm">
				<item>Apple</item>
				<item>Banana</item>
				<item>Berry</item>
			</combobox>
			<horizontal>
				<button name="buttonMinus" label="minus" />
				<text name="textLeftRight" label="0" />
				<button name="buttonPlus" label="plus" />
			</horizontal>
			<checkbox name="checkboxSample" label="Check this" />
		</group>
	</main>
</ui>
```

# Ribbon definition
The ribbon definition is wrapped in ```<ribbon label="App Name">...</ribbon>```. The label is the human readable name that is shown at the ribbon tab.

The ribbon may contain elements of the following types:
* button - a normal button
* dropdown - a drop down menu, can contain nested elements
* toggle - a toggle button

The dropdown element may contain the following elements:
* button
* toggle

Note that each element is defined by a line like ```<button name="buttonID" label="Click this" />```. The name is sent to your app when an UI event occurs. The label is shown to the user.

# Main definition
The main definition consists of layout elements and normal elements. Layout elements can contain other elements, including other layout elements.

## Element types
Normal elements:
* button - a normal button
* checkbox - a checkbox
* combobox - a drop down selection
* image - an image
* numberbox - a number entry
* separator - a separator line
* text - a text
* textbox - a text entry

Layout elements:
* group - draws a box with a title around elements. Behaves like a vertical.
* horizontal - elements are stacked horizontally
* vertical - elements are stacked vertically

## Attributes
Each element has the following attributes, each of them is optional:
* name - identifier for events and UI updates
* label - text label, drawn in column to the left of the object
* value - default value

Note: for text elements you can give the text as ```label``` or ```value```. Consider setting static informational texts as ```value```: If no label is given the text is spread over both left and right columns.

Additional attributes:
* numberbox - ```min``` and ```max``` define the allowed value range
* image - ```width``` and ```height``` define the image width within the UI (not the pixels of the image data). If undefined or <= 0 the size is automatic

Comboboxes may contain child elements of type ```item```, these are used as the selectable items.
```xml
<item>My Item Text</item>
```

## Events
Elements can send events depending on their type, your app receives them as calls of UiUpdateHandler() if you use AppClient, or via the RecieveActions stream if you use plain gRPC.

Elements send the following event data:
* Buttons - ButtonState - CLICKED (NOT_CLICKED might be sent in future)
* Checkboxes - CheckboxState - CHECKED, UNCHECKED
* Comboboxes - DropdownState - the selected value as string
* Images - ImageState - the position that was clicked at in percent (0.0 .. 1.0) of width/height
* Numberboxes - NumberfieldState - the number value
* Textboxes - TextfieldState - the text string

If your app contains multiple binaries changes by one binary will also be sent to all others.

## Visibility
Elements can be hidden by a command from the app or by adding the attribute ```visible="false"``` to a UI element:
```xml
<numberbox name="numberboxSample" value="123.456" label="Number Box" visible="false" />
```

# Handling UI events in your app
When a user clicks a button or enters a value the ```UiUpdateHandler()``` is called. You app should override this function and handle the UI updates it contains. See sample apps ```MinimalApp```, ```MonitorApp``` or ```ControlApp``` for examples. Note that if your app uses more than one binary each binary will also receive the updates triggered by the other binaries.

# Changing the UI via your app
While the UI structure can not be changed class ```AppClient``` contains several methods for changing the state of the UI elements:
* ```SetUIVisibility()``` - sets an object visible or hidden
* ```SetCheckboxState()``` - sets the state of a checkbox
* ```SetDropDownState()``` - sets the selection and/or selectable items of a drop down box
* ```SetText()``` - sets the text of a text element or text box
* ```SetNumber()``` - sets the number value of a number box. This can also be used to assign a number value to a text element or text box.
* ```SetImage()``` - sets an image

Note the ```Queue...``` method calls. These queue multiple UI updates to be sent in a single message via ```SendQueuedUIUpdates()```. This improves UI performance when updating multiple UI elements at once.

If you are using images note that all images combined must not be larger than 290kB. Due to a limitation in the CRI interface larger images are not received by the igus Robot Control PC software (iRC). On reconnect of the iRC the entire ```ui.xml``` including images is sent to iRC, everything combined must be less than 400kB (images are base64 encoded, therefore 290kB). If you exceed this limit images may not be updated and the UI may not load on reconnect.