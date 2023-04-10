<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/abiatarfestus/quote-invoice">
    <img src="quote_invoice/assets/main_logo.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">Quote & Invoice App</h3>

  <p align="center">
    A desktop application to keep track of your customers and generate quotes and invoices
    <br />
    <a href="https://github.com/abiatarfestus/quote-invoice"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/abiatarfestus/quote-invoice">View Demo</a>
    ·
    <a href="https://github.com/abiatarfestus/quote-invoice/issues">Report Bug</a>
    ·
    <a href="https://github.com/abiatarfestus/quote-invoice/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This project was adapted from a Microsoft Access application I made for my colleague's business. As part of my Python learning journe, i decided to convert the Access application to a desktop application using Python and its Tkinter module. The application has a number of features, which include storing and retrieving customer information, products and services, quotations and orders, as well as generating quotes and invoces based on quotations and orders saved in the database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This project was built with, among others, the following frameworks/libraries.

* [![Python][Python]][Python-url]
* [![Sqlite][Sqlite]][Sqlite-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get this project up and running on your local machine follow these steps.

### Prerequisites

* Pipenv
  ```sh
  pip install pipenv --user
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/abiatarfestus/quote-invoice.git
   ```
3. Install dependencies
   ```sh
   pipenv install
   ```
4. Lauch project
   ```sh
   pipenv shell
   python -m quote_invoice
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Add unique constrations to quotations
- [ ] Add clumn attributes (unique, nullable, auto_add_date)
- [ ] Review the update methods
- [ ] Wrap data display/insertion on the treeview into a function for reuse by search function
- [ ] Wrap clear treeview into a method for access by all search methods
- [ ] Limit number of list items diplayed in the list views
- [ ] Add option for adding items not in the product table (de-link foreignkey)
- [ ] Quote/OrderItem description defaults to associated product description, but can be modified
- [ ] Change if quote_id and product_id: to if not quote_id or not product_id: and return error message
- [ ] Show info message on print("THE SELECTED PRODUCT IS ALREADY ON THE QUOTATION") but continue with next item
- [ ] Check if product is in stock 
- [ ] Change money/prices representation in the db and elsewhere from float to strings
- [ ] Verify/validate customer field when submitting quotation
- [ ] Enforce or validate a particular date format
- [ ] Reduce items.append(self.quote_items_tree.item(item)) to values instead of the whole dictionaries
- [ ] Verify if get_connection() has to appear twice
- [ ] Change self.notebook.select(6) to self.notebook.select(tab name)
- [ ] Add specific exceptions
- [ ] change print("THIS ORDER IS CLOSED") to error message
- [ ] Refactor update_order in order details to connect to db's method
- [ ] Disable order_date when in editing mode
- [ ] Reset variables on open_new blank form and open record
- [x] Check if !disabled is necessary before modifying the widget
- [ ] Fix customer selction: ID vs display name
- [ ] Prevent settings window from disappearing when dialog box pops up
- [ ] Managing session in the app
- [ ] Check data entry formatting e.g., .lower() etc
- [ ] Add on_delete restrictions
- [ ] Where to calculate Tax?/ Add VAT to Product table
- [ ] Prefix for invoice/quote number (add it to settings)
- [ ] Change some if statements to asserts 

See the [open issues](https://github.com/abiatarfestus/quote-invoice/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing
I welcome any and all contributions! Here are some ways you can get started:
1. Report bugs: If you encounter any bugs, please let me know. Open up an issue and let me know the problem.
2. Contribute code: If you are a developer and want to contribute, follow the instructions below to get started!
3. Suggestions: If you don't want to code but have some awesome ideas, open up an issue explaining some updates or imporvements you would like to see!
4. Documentation: If you see the need for some additional documentation, feel free to add some!

## Instructions
1. Fork this repository
2. Clone the forked repository
3. Add your contributions (code or documentation)
4. Commit and push
5. Wait for pull request to be merged

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Your Name - [@abiatarfestus](https://twitter.com/abiatarfestus)

Project Link: [https://github.com/abiatarfestus/quote-invoice](https://github.com/abiatarfestus/quote-invoice)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://dev.to/envoy_/150-badges-for-github-pnk)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/abiatarfestus/quote-invoice.svg?style=for-the-badge
[contributors-url]: https://github.com/abiatarfestus/quote-invoice/contributors
[forks-shield]: https://img.shields.io/github/forks/abiatarfestus/quote-invoice.svg?style=for-the-badge
[forks-url]: https://github.com/abiatarfestus/quote-invoice/network/members
[stars-shield]: https://img.shields.io/github/stars/abiatarfestus/quote-invoice.svg?style=for-the-badge
[stars-url]: https://github.com/abiatarfestus/quote-invoice/stargazers
[issues-shield]: https://img.shields.io/github/issues/abiatarfestus/quote-invoice.svg?style=for-the-badge
[issues-url]: https://github.com/abiatarfestus/quote-invoice/issues
[license-shield]: https://img.shields.io/github/license/abiatarfestus/quote-invoice.svg?style=for-the-badge
[license-url]: https://github.com/abiatarfestus/quote-invoice/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/festus-abiatar-35b33b215/
[product-screenshot]: quote_invoice/assets/screenshot.png
[Python]: https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[Sqlite]: https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white
[Sqlite-url]: https://sqlite.org/