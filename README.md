<a id="readme-top"></a>




<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<!--
<br />
<div align="center">
  <a href="https://github.com/evan-thoms/pinyImage">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
  -->

<h3 align="center">PinyImage</h3>

  <p align="center">
    Create meaningful mental images to remember Mandarin characters forever!
    <br />
    
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
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
One of the most important parts of language learning is being able to remember massive amounts of words and phrases, and especially with a system like Mandarin where characters give few clues to their meaning, the ability to recall their sound and function becomes essential.

PinyImage leverages your brain's natural ability to recall visual information to enhance and speed up character memorization. Tying character appearance to its meaning and sound using a mental image with familiar objects and feelings will store a character more strongly in your mind, ultimately leading to a better mastery of the Chinese language!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* React
* Node.js
* Bootstrap
* Masonry layout
* SQLite
* tilt.js
* Cohere AI API

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/evan-thoms/pinyImage.git
   cd pinyImage
   ```

2. Backend Setup
   ```sh
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Environment Configuration
   ```sh
   # Copy the example environment file
   cp env.example .env
   # Edit .env and add your API keys
   # Choose either COHERE_API_KEY or OPENAI_API_KEY
   ```

4. Frontend Setup
   ```sh
   cd ../frontend
   npm install
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Local Development

1. Start the backend server
   ```sh
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python main.py
   ```

2. Start the React frontend (in a new terminal)
   ```sh
   cd frontend
   npm start
   ```

3. Open your browser and navigate to http://localhost:3000

4. Input a Mandarin character and review the AI-generated mnemonic
5. Save desired responses to create study cards
6. Use the search functionality to filter through your saved cards

### Deployment

#### Option 1: Render (Recommended - Free)
1. Fork this repository
2. Connect your fork to [Render](https://render.com/)
3. Create a new Web Service
4. Add environment variables in Render dashboard:
   - `COHERE_API_KEY` or `OPENAI_API_KEY`
   - `FLASK_ENV=production`
5. Deploy automatically

#### Option 2: Heroku
1. Install Heroku CLI
2. Create a new Heroku app
3. Add environment variables:
   ```sh
   heroku config:set COHERE_API_KEY=your_key_here
   heroku config:set FLASK_ENV=production
   ```
4. Deploy:
   ```sh
   git push heroku main
   ```

### Testing

Run the API tests:
```sh
cd backend
python test_api.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Evan Thoms - evanthoms@outlook.com

Project Link: [https://github.com/evan-thoms/pinyImage](https://github.com/evan-thoms/pinyImage)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
