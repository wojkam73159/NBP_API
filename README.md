# NBP_API
## Overview
This project focuses on deepening knowledge and experience with APIs, Test-Driven Development (TDD), and mocking. It aggregates real-time currency exchange rate data from the NBP (National Bank of Poland) API.
## Tech Stack

    Python: Core programming language for implementing the project.
    NBP API: External REST API used for fetching real-time currency exchange rates.
    JSON: format of data
    PyTest: Testing framework used to ensure the correctness of the code.
    Mocking (unittest.mock): Used to simulate API responses during testing, ensuring isolated and reliable test cases.

## Key Features

    NBP API Integration:
        Utilizes Python's requests library to fetch data from multiple endpoints of the NBP API.
        Data is returned in JSON format and processed to extract relevant exchange rate information.

    Test-Driven Development (TDD):
        Follows a TDD approach, with all functionality developed alongside corresponding unit tests.

    PyTest:
        Comprehensive test coverage using the unittest and PyTest frameworks.
        Tests include validating API responses, data correctness, and ensuring the program handles multiple scenarios.

    Mocking:
        Extensively uses mocking to simulate API responses for test cases, enabling testing of functionality without reliance on the live NBP API.
        unittest.mock is used to create mock objects for API calls, ensuring the tests are fast, reliable, and independent of external systems.

    Data Validation:
        Ensures correctness of data structure and content through unit tests that check for expected keys, types, and values in the API responses and processed data.
