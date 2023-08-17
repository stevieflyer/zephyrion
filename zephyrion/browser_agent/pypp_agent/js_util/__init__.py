"""
# Introduction

`js_utils` provides a set of javascript code generators and javascript code handlers.

Including the following modules:

- `js_generator`: javascript code generators, which can generate common javascript code

- `js_handler`: javascript code handlers, which can execute javascript code in specific usage case

# Limitation

`js_generator` can run independently without any dependency.

However, `js_handler` highly depends on  `pyppeteer.page.Page` class, which provide the js execution environment.
Some interaction function is purely based on `pyppeteer.page.Page` class methods for efficiency.
"""