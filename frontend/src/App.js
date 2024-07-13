import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import Navbar from './Navbar';
import CardList from './CardList';
import CardForm from './CardForm';

const App = () => {
  const  [cards, setCards] = useState([]);
  const [result, setResult] = useState('');
  const [connections, setConnections] = useState('');


  useEffect(() => {
    fetchCards();
  }, []);

  const fetchCards = async () => {
    try {
      const response = await axios.get('/api/cards');
    console.log("response of fetchCards: "+response);
    setCards(response.data)
    } catch (error){
      console.error("error fecthing cards: ", error)
    }
    
  };

  const handleSubmit = async (input) => {
    try {
    const response = await axios.post('/api/result', { user_input: input });
    setResult(response.data.result);
    setConnections(response.data.result);
    setCards(response.data.cards);
  } catch (error) {
    console.error("Error submitting input: ", error);
  }
  };
  return (
    <div className="App">
      <Navbar />
      <h1>PinyImage</h1>
      <h3>Create meaningful mental images to help remember Mandarin characters!</h3>
      <CardList cards={cards} />
      <CardForm onSubmit={handleSubmit} />
      {result && <div>{result}</div>}
      {connections && <div>{connections}</div>}
    </div>
  );
}
export default App;
