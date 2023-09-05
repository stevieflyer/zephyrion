# Zephyrion - Deprecated

**Note: This repository is deprecated and no longer maintained. For an active and maintained browser automation library, we recommend using [Quokka](https://github.com/stevieflyer/quokka).**

Zephyrion is a powerful Python library built on top of Pyppeteer, designed to simplify browser automation and manipulation tasks. It provides a convenient way to interact with web pages, extract data, and automate browser actions.

## Deprecation Notice

This repository is no longer actively maintained. We encourage you to consider using [Quokka](https://github.com/stevieflyer/quokka), a modern and actively developed browser automation library that offers a rich set of features and improved performance.

## Key Features

- Easy Browser Management: Zephyrion provides a simple interface for managing browser instances, starting, stopping, and navigating web pages.
- Data Extraction: With the data extraction module, you can easily extract data from web pages using customizable selectors and patterns.
- Page Interaction: The page interaction module enables you to interact with web page elements, such as clicking, typing, and scrolling.
- Extensible: Zephyrion's architecture allows for extension and customization to suit your specific needs.
    
## Installation

```bash
pip install zephyrion
```

## Getting Started

Zephyrion's intuitive API makes browser automation straightforward. Here's a simple example:

```python
from zephyrion import Browser

async def main():
    browser = await Browser.launch(headless=True)
    page = await browser.new_page()
    await page.goto("https://example.com")
    
    # Your automation code here

    await browser.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Documentation
For detailed usage instructions, examples, and customization options, please refer to the Documentation.

## Examples
Check out the Examples folder for more usage scenarios and demonstrations of Zephyrion's capabilities.

## Contributing
Contributions to Zephyrion are welcome! Please read our Contribution Guidelines for more information on how to contribute to the project.

## License
This project is licensed under the MIT License.