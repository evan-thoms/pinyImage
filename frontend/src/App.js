import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import Navbar from './components/Navbar';
import CardList from './components/CardList';
import CardForm from './components/CardForm';
import Search from './components/Search';

import 'bootstrap/dist/css/bootstrap.min.css';


const App = () => {
  const  [cards, setCards] = useState([]);
  const [result, setResult] = useState('');
  const [connections, setConnections] = useState('');
  const [filteredCards, setFilteredCards] = useState([])

  
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
    } catch (error) {
      console.error("error fetching cards: ", error);
    }
  };

  const handleSubmit = async (input) => {
    try {
    console.log("hit submit button")
    const response = await axios.post('/api/result', { user_input: input });
    console.log("response here: ",response);
    setResult(response.data.result);
    setConnections(response.data.connections);
    setCards(response.data.cards);
  } catch (error) {
    console.error("Error submitting input: ", error);
  }
  };
  return (
    <div className="App">
      <Navbar />
      
      <h3>Create meaningful mental images to help remember Mandarin characters!</h3>
      
      <CardForm onSubmit={handleSubmit} />
      {result && <div>{result}</div>}
      {connections && <div>{connections}</div>}
      <Search cards={cards} handleSearch={searchFiltering}></Search>
      <CardList cards={filteredCards.length > 0 ? filteredCards : cards} />
    </div>
  );
}
export default App;
