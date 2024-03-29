<a name="readme-top"></a>

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
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Link to the project][product-screenshot]](https://sen-codex.dev)

The Digital Economy Unit of the French Competition Agency (“FCA”) has developed a tool that identifies citations of the FCA’s publications in other Autorité’s publications and represents the interconnections in a graph. The creation of such a tool breaks new ground in computational antitrust research. The present open source code is designed to be publicly accessible—anyone can see, modify, and distribute the code as they see fit. Open source software is developed in a decentralized and collaborative way, relying on peer review and community production.

### Built With

This section list major frameworks/libraries used to bootstrap the project.

* ![Python](https://img.shields.io/badge/PYTHON-007396.svg?&style=flat&logo=python&logoColor=white)&nbsp;
* ![Dash](https://img.shields.io/badge/DASH-007396.svg?&style=flat&logo=plotly&logoColor=white)&nbsp;
* ![Dash cytoscape](https://img.shields.io/badge/DASH-CYTOSCPAE-007396.svg?&style=flat&logo=plotly&logoColor=white)&nbsp;

Dash is an open-source framework for Python written on top of Flask, Plotly.js, and React.js

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This repository hosts the open source code written in Python. They can serve as a starting point for your own Dash app, as a learning tool to better understand how Dash works, as a reusable templates, and much more.
To get a local copy up and running follow these simple example steps.

### Prerequisites

You need to have python (https://www.python.org/downloads/) and pip installed (https://pip.pypa.io/en/stable/installation/), do not forget to add environment variables for python and pip.

### Installation

To clone this repository, run:
```
git clone https://github.com/AutoriteDeLaConcurrence/publication_sen-codex_networkgraph
```

To create an isolated Python virtual environment.
```bash
python -m venv venv
source venv/bin/activate  # Windows: \venv\scripts\activate
pip install -r requirements.txt
```

then you can run the app:
```bash
python front_end_app.py
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

We would like to thank :

* Autorité de la concurrence (France) : Yann Guthmann, Adrien Frumence and Camille Hoogterp
* The Stanford University CodeX Center
* Stanford Computational Antitrust Project Director: Dr. Thibault Schrepel // Editor-in-Chief: Teodora Groza
* Editors: Thaiane Abreu, Juan Sebastian Gomez, Mariah Mumbi Kirubi, Kyrill Ryabtsev, Anna Starkova, Björn ten Seldam, Glen Williams
* Academic Outreach Chair: Aleksandra Wierzbicka // Executive Operations Chair: Alex Sotropa


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.png


