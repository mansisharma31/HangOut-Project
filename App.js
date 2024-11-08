//import './App.css';
import React, { useState, useEffect } from 'react';
//import PreferenceForm from './Components/PreferenceForm';
//import RecommendationList from './Components/RecommendationList';
//import data from './data.json';
import Home from "./Screens/Home/Home.js";
import Product from "./Screens/Products/Product.js";
// import Recommendations from "./Components/Recommendations.js";
import Recommendations from "./Components/Recommendations.js";
import Delhi from "./Components/Delhi.js";
import Mumbai from "./Components/Mumbai.js";
import Bangalore from "./Components/Banglore.js";
import RecommendationForm from './Components/RecommendationForm';
// import 'swiper/swiper-bundle.min.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useNavigate
  // Navigate
} from "react-router-dom";

function App() {
  const [recommendations, setRecommendations] = useState([]);

//   const fetchRecommendations = async (formData) => {
//     try {
//         const response = await fetch('http://localhost:3000/api/getRecommendations', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(formData)
//         });
//         const data = await response.json();
//         setRecommendations(data); // Set recommendations from backend response
//     } catch (error) {
//         console.error('Error fetching recommendations:', error);
//     }
// };


    
  return (
    <Router> 
    <div className="App">
    
      <Routes>
      {/* <h1>HangOut Activity Recommender</h1> */}
      {/* <Route exact path="/" element={<Home recommendActivities={recommendActivities}/>} /> */}
      {/* <Route exact path="/recommendations" element={<RecommendationList recommendations={recommendations}/>} /> */}
      <Route exact path="/" element={<Home/>} />
        <Route exact path="/product/:id" element={<Product/>} />
        {/* <Route exact path="/recommendations" element={<Recommendations/>} /> */}
        {/* <Route exact path="/api/recommend" element={<Recommendations/>} /> */}
        <Route 
                        path="/form" 
                        element={<RecommendationForm/>} 
                    />
                    <Route 
                        path="/recommendations" 
                        element={<Recommendations />} 
                    />
        <Route path="/delhi" element={<Delhi />} />
        <Route path="/mumbai" element={<Mumbai />} />
        <Route path="/bangalore" element={<Bangalore />} />
      </Routes>

    </div>
    </Router>
  );
}


export default App;
