import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import './App.css';
import Navbar from './components/Navbar';
import CardList from './components/CardList';
import CardForm from './components/CardForm';
import Search from './components/Search';
import $ from 'jquery';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'tilt.js';
import { BrowserRouter as Router } from 'react-router-dom';

const App = () => {
  const [cards, setCards] = useState([]);
  const [result, setResult] = useState('');
  const [connections, setConnections] = useState('');
  const [filteredCards, setFilteredCards] = useState([]);
  const [curCard, setCurCard] = useState({ title: "", pinyin: "", meaning: "", con: "" });
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);
  const [validChar, setValidChar] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  const aboutRef = useRef(null);
  const searchRef = useRef(null);

  useEffect(() => {
    $('[data-tilt]').tilt({
      maxTilt: 15,
      perspective: 1000,
      easing: 'cubic-bezier(.03,.98,.52,.99)',
      scale: 1.03,
      speed: 300,
      transition: true,
      disableAxis: null,
      reset: true,
      glare: false,
      maxGlare: 0.5,
    });
  }, [cards]);

  useEffect(() => {
    fetchCards();
  }, []);

  const searchFiltering = (searchTerm) => {
    const filteredResult = cards.filter(card =>
      card.pinyin.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").includes(searchTerm.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""))
    );
    setFilteredCards(filteredResult);
  };

  const handleScroll = (ref) => {
    ref.current.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchCards = async () => {
    console.log("fetch cards");
    try {
      const response = await axios.get('/api/cards');
      console.log("response of fetchCards: ", response);
      setCards(response.data);
    } catch (error) {
      console.error("error fetching cards: ", error);
    }
  };

  const containsChineseCharacters = (s) => {
    return /[\u4e00-\u9fff]/.test(s);
  };

  const removeDuplicates = (cards) => {
    const uniqueCards = cards.filter((card, index, self) =>
      index === self.findIndex((c) => (
        c.character === card.character && c.pinyin === card.pinyin
      ))
    );
    return uniqueCards;
  };

  const handleSubmit = async (input) => {
    setSubmitted(true);
    setLoading(true);
    setSaved(false);
    const isChinese = containsChineseCharacters(input);
    setValidChar(isChinese);

    if (!isChinese) {
      setLoading(false);
      setResult("");  // Clear the result if the input is not Chinese
      setConnections(""); // Clear connections if the input is not Chinese
      return;
    }

    setResult("");
    try {
      console.log("hit submit button");
      const response = await axios.post('/api/result', { user_input: input });
      console.log("response here, ", response);
      setResult(response.data.result);
      setConnections(response.data.connections);
      setCards(removeDuplicates(response.data.cards));
      setCurCard({
        title: input,
        pinyin: response.data.pinyin,
        meaning: "means " + response.data.meaning,
        con: response.data.connections,
      });
    } catch (error) {
      console.error("Error submitting input: ", error);
    } finally {
      setLoading(false);
    }
  };

  const addToDatabase = async () => {
    try {
      console.log("adding to db");
      const response = await axios.post('/api/post', curCard);
      console.log("response of addtodb: ", response);

      fetchCards();
      setSaved(true);
      // Do not reset validChar or any other states affecting the response display
    } catch (error) {
      console.error("Error adding to db: ", error);
    }
  };

  return (
    <Router>
      <div className="App">
        <Navbar onClick={handleScroll} aboutRef={aboutRef} searchRef={searchRef} />
        <h3 className="intro">Create meaningful mental images to remember Mandarin characters forever!</h3>
        <CardForm className="cardForm" onSubmit={handleSubmit} />

        {submitted ? (
          loading ? (
            <div className='dots'>
              <div></div>
              <div></div>
              <div></div>
            </div>
          ) : validChar ? (
            <div className="output">
              {result ? (
                <div className="response">{result}</div>
              ) : (
                <div></div>
              )}

              {connections && (
                <div>
                  <br />
                  <div className="response">{connections}</div>
                  <div className="save">
                    Save this response?
                    {saved ? (
                      <button className="saveButton">Saved!</button>
                    ) : (
                      <button className="saveButton" onClick={addToDatabase}>Save to Cards</button>
                    )}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="shortly"><p>Response does not contain Chinese characters</p></div>
          )
        ) : (
          <div className="shortly">
            <p>Your response will appear below.</p>
          </div>
        )}

        <div ref={searchRef}>
          <Search cards={cards} handleSearch={searchFiltering}></Search>
        </div>
        <CardList cards={filteredCards.length > 0 ? filteredCards : cards} />
        <div className="line"></div>
        <div className="about" ref={aboutRef}>
          <div className="aboutTitle">What is PinyImage?</div>
          <div className="description">
            One of the most important parts of language learning is being able to remember massive amounts of words and phrases, and especially with a system like Mandarin where characters give few clues to their meaning, the ability to recall their sound and function becomes essential.
            <br /><br />PinyImage leverages your brain's natural ability to recall visual information to enhance and speed up character memorization. Tying character appearance to its meaning and sound using a mental image with familiar objects and feelings will store a character more strongly in your mind, ultimately leading to a better mastery of the Chinese language!
          </div>
        </div>
        <div className="endBlock"></div>
      </div>
    </Router>
  );
}

export default App;
