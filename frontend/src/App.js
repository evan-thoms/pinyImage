import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import Navbar from './components/Navbar';
import CardList from './components/CardList';
import CardForm from './components/CardForm';
import Search from './components/Search';
import $ from 'jquery';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'tilt.js';



const App = () => {
  const  [cards, setCards] = useState([]);
  const [result, setResult] = useState('');
  const [connections, setConnections] = useState('');
  const [filteredCards, setFilteredCards] = useState([]);
  const [curCard, setCurCard] = useState({ title:"", pinyin:"", meaning:"", con:""});

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
      card.pinyin.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").includes(searchTerm.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "")));
      setFilteredCards(filteredResult);
  };
  
  const fetchCards = async () => {
    console.log("fetch cards")
    try {
      const response = await axios.get('/api/cards');
      console.log("response of fetchCards: ", response);
      setCards(response.data);
      console.log(response.data);

    } catch (error) {
      console.error("error fetching cards: ", error);
    }
  };
  
  const removeDuplicates = (cards) => {
    const uniqueCards = cards.filter((card, index, self) => 
      index === self.findIndex((c) => (
        c.character === card.character && c.pinyin === card.pinyin
        )
      ));

    return uniqueCards;
  };


  const handleSubmit = async (input) => {
    try {
    console.log("hit submit button")
    const response = await axios.post('/api/result', { user_input: input });
    console.log("response here, ", response)
    setResult(response.data.result);
    setConnections(response.data.connections);
    setCards(removeDuplicates(response.data.cards));
    setCurCard({
      title: input, 
      pinyin: response.data.pinyin,
      meaning: response.data.meaning,
      con: response.data.connections,
    })
  } catch (error) {
    console.error("Error submitting input: ", error);
  }
  };

  const addToDatabase = async (card) => {
    try {
      console.log("adding to db");
      const response = await axios.post('/api/post', curCard);
      console.log("response of addtodb: ", response);

      fetchCards();

    } catch (error) {
      console.error("Error adding to db: ", error);
    }
  };

  return (
    <div className="App">
    
      <Navbar />
      <h3>Create meaningful mental images to help remember Mandarin characters!</h3>
      
      < CardForm onSubmit={handleSubmit} />

      {result ? <div>{result}</div>: <div><p>Your response will appear below shortly</p></div>}
      {connections && <div>
        {connections}
        <p>Save this response?</p>
        <button onClick={addToDatabase}>Save</button>
        </div>}
      <Search cards={cards} handleSearch={searchFiltering}></Search>
      <CardList cards={filteredCards.length > 0 ? filteredCards : cards} />
    </div>
  );
}
export default App;
