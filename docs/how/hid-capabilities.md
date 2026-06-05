# HID capabilities and LED/RGB limitations

The baseline treats the Anticater VK-01 as HID-first. The CLI reports HID
identity metadata and capabilities where HIDAPI exposes them:

- manufacturer and product strings
- vendor ID and product ID
- path
- usage page and usage
- interface number
- transport hints when available

HIDAPI does not reliably expose transport or full descriptor details on every
platform. Missing values are reported as `unknown` or `null` rather than guessed.

Vendor-defined usage pages (`>= 0xff00`) are reported as capabilities. This
baseline does not attempt LED/RGB control. Add a separate research phase only if
real descriptor evidence shows output or feature reports that can be exercised
safely and without reverse engineering vendor software.

