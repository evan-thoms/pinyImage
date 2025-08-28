import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { ClerkProvider, SignIn, useUser, useAuth, useSession } from '@clerk/clerk-react';
import './App.css';
import Navbar from './components/Navbar';
import CardList from './components/CardList';
import CardForm from './components/CardForm';
import Search from './components/Search';
import $ from 'jquery';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'tilt.js';
import { BrowserRouter as Router } from 'react-router-dom';
// Environment test removed

const AppContent = () => {
  const { user, isSignedIn } = useUser();
  const { signOut } = useAuth();
  const { session } = useSession();
  
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
    if (isSignedIn && user && session) {
      // Set up axios default headers with Clerk token and user info
      session.getToken()
        .then(token => {
          console.log('Clerk token obtained successfully');
          console.log('User info:', user);
          
          // Set up headers with token and user info
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          axios.defaults.headers.common['X-User-Email'] = user.emailAddresses[0]?.emailAddress || user.primaryEmailAddress?.emailAddress;
          axios.defaults.headers.common['X-User-ID'] = user.id;
          
          // Fetch cards immediately after getting token
          fetchCards();
        })
        .catch(error => {
          console.error('Error getting Clerk token:', error);
          // Still try to fetch cards without token for now
          fetchCards();
        });
    } else {
      // Clear cards when user logs out
      setCards([]);
      setFilteredCards([]);
      setResult("");
      setConnections("");
      setCurCard(null);
      // Clear headers
      delete axios.defaults.headers.common['Authorization'];
      delete axios.defaults.headers.common['X-User-Email'];
      delete axios.defaults.headers.common['X-User-ID'];
    }
  }, [isSignedIn, user, session]);

  const searchFiltering = (searchTerm) => {
    const filteredResult = cards.filter(card =>
      card.pinyin.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").includes(searchTerm.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""))
    );
    setFilteredCards(filteredResult);
  };

  const handleScroll = (ref) => {
    ref.current.scrollIntoView({ behavior: 'smooth' });
  };

  const handleLogout = () => {
    signOut();
    delete axios.defaults.headers.common['Authorization'];
    delete axios.defaults.headers.common['X-User-Email'];
    delete axios.defaults.headers.common['X-User-ID'];
    setCards([]);
    setFilteredCards([]);
    setResult("");
    setConnections("");
    setCurCard(null);
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
      // DON'T overwrite database cards with AI response cards
      // setCards(removeDuplicates(response.data.cards));
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

      if (response.status === 200) {
        console.log("Card saved successfully");
        // Refresh cards immediately after saving
        await fetchCards();
        setSaved(true);
      }
      // Do not reset validChar or any other states affecting the response display
    } catch (error) {
      console.error("Error adding to db: ", error);
      // Show error to user
      alert("Failed to save card. Please try again.");
    }
  };

  return (
    <Router>
      <div className="App">
        {!isSignedIn ? (
          <div className="auth-container">
            <div className="auth-card">
              <div className="auth-header">
                <h2>Welcome to PinyImage</h2>
                <p>Sign in to start learning Chinese characters</p>
              </div>
              <div className="clerk-wrapper">
                <SignIn />
              </div>
            </div>
          </div>
        ) : (
          <>
            <Navbar onClick={handleScroll} aboutRef={aboutRef} searchRef={searchRef} user={user} onLogout={handleLogout} />
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
          </>
        )}
      </div>
    </Router>
  );
}

const App = () => {
  const clerkPubKey = process.env.REACT_APP_CLERK_PUBLISHABLE_KEY;
  
  console.log('Clerk key:', clerkPubKey ? 'Found' : 'Missing');
  
  if (!clerkPubKey) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        backgroundColor: '#e8e7e3',
        color: '#333',
        fontSize: '16px',
        fontFamily: '"Sawarabi Mincho", serif'
      }}>
        <div style={{ 
          textAlign: 'center',
          backgroundColor: '#7a8aa0',
          padding: '30px',
          borderRadius: '12px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)'
        }}>
          <h2>Configuration Error</h2>
          <p>Missing Clerk Publishable Key</p>
          <p>Please add REACT_APP_CLERK_PUBLISHABLE_KEY to your .env file</p>
          <p>Current key: {clerkPubKey || 'Not found'}</p>
        </div>
      </div>
    );
  }
  
  return (
    <ClerkProvider publishableKey={clerkPubKey}>
      <AppContent />
    </ClerkProvider>
  );
};

export default App;
