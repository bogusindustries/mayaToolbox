<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/bogusindustries/mayaToolbox">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Maya Toolbox</h3>

  <p align="center">
    Useful Maya Tools
    <br />
    <a href="https://github.com/bogusindustries/mayaToolbox"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/bogusindustries/mayaToolbox">View Demo</a>
    ·
    <a href="https://github.com/bogusindustries/mayaToolbox/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/bogusindustries/mayaToolbox/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
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

A toolbox full of various tools including:
* Fix Viewport
  - When viewport 2.0 freaks out
* Custom Control Creation
  - Combine multiple curves into one control
* Selection Tools
  - Select all objects of specified types in the scene
  - Select BlendShape targets on selected
  - Select all animation curves in scene
* Constraint tools
  - Create multiple constraints at once
  - Bake constraints to animation (Great for sending to game engines!)
  - Find constraint parents and children
* And More!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With
PySide2

<!--* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]-->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Download the latest python script and follow the installation instructions

### Prerequisites

Currently only tested in Maya 2022.5

### Installation

1. Download the latest Python file
2. Place the script on your local drive
   Windows : C:\Users\<YourUserName>\Documents\maya\scripts
   macOS : /Users/<YourUserName>/Documents/maya/scripts
3. Create a shelf button
   Right-click on the shelf and choose New Shelf Button
4. Edit the shelf button command
   ```py
   import hybrid_toolbox
   from imp import reload
   reload(hybrid_toolbox)
   hybrid_toolbox.openWindow()
   ```
5. Name and Icon:
   Give uour button a name and set an icon if you wish

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Add the toolbox to a shelf for easy access

<!--_For more examples, please refer to the [Documentation](https://example.com)_ -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Search for animation within selected group

See the [open issues](https://github.com/bogusindustries/mayaToolbox/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/bogusindustries/mayaToolbox/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=bogusindustries/mayaToolbox" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

License pending

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

John Zilka - [@twitter_handle](https://x.com/bogusindustries) 

Project Link: [https://github.com/bogusindustries/mayaToolbox](https://github.com/bogusindustries/mayaToolbox)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/bogusindustries/mayaToolbox.svg?style=for-the-badge
[contributors-url]: https://github.com/bogusindustries/mayaToolbox/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/bogusindustries/mayaToolbox.svg?style=for-the-badge
[forks-url]: https://github.com/bogusindustries/mayaToolbox/network/members
[stars-shield]: https://img.shields.io/github/stars/bogusindustries/mayaToolbox.svg?style=for-the-badge
[stars-url]: https://github.com/bogusindustries/mayaToolbox/stargazers
[issues-shield]: https://img.shields.io/github/issues/bogusindustries/mayaToolbox.svg?style=for-the-badge
[issues-url]: https://github.com/bogusindustries/mayaToolbox/issues
[license-shield]: https://img.shields.io/github/license/bogusindustries/mayaToolbox.svg?style=for-the-badge
[license-url]: https://github.com/bogusindustries/mayaToolbox/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/therealjz
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
