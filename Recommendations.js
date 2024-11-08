// Recommendations.js
import React from 'react';
import { Link } from 'react-router-dom';

const Recommendations = ({ recommendations }) => {
    return (
        <div>
            <h2>Top Recommendations</h2>
            <Link to="/">Back to Home</Link>

            {recommendations.length > 0 ? (
                recommendations.map((itinerary, idx) => (
                    <div key={idx}>
                        <h3>Itinerary {idx + 1} (Score: {itinerary.score})</h3>
                        <ul>
                            {itinerary.places.map((place, i) => (
                                <li key={i}>
                                    <strong>{place.name}</strong> - {place.category} <br />
                                    Duration: {place.duration} hours, Price: {place.price}
                                </li>
                            ))}
                        </ul>
                    </div>
                ))
            ) : (
                <p>No recommendations found. Please go back and submit the form.</p>
            )}
        </div>
    );
};

export default Recommendations;



// import React from 'react';
// import { useLocation } from 'react-router-dom';

// const Recommendations = () => {
//   const location = useLocation();
//   const recommendations = location.state?.recommendations || [];

//   return (
//     <div>
//       {recommendations.length > 0 ? (
//         recommendations.map((itinerary, index) => (
//           <div key={index}>
//             <h3>Itinerary {index + 1} (Score: {itinerary.score})</h3>
//             <ul>
//               {itinerary.itinerary.map((place, idx) => (
//                 <li key={idx}>
//                   {place.name} - {place.category} - {place.duration} hours - ₹{place.price}
//                 </li>
//               ))}
//             </ul>
//             <p>Total Duration: {itinerary.total_duration} hours</p>
//             <p>Total Price: ₹{itinerary.total_price}</p>
//           </div>
//         ))
//       ) : (
//         <p>No recommendations found</p>
//       )}
//     </div>
//   );
// };

// export default Recommendations;




// // import React, { useState, useEffect } from 'react';
// // import axios from 'axios';
// // import Navbar from '../Components/Navbar';

// // const Recommendations = ({ userInput }) => {
// //   const [recommendations, setRecommendations] = useState([]);
// //   const [loading, setLoading] = useState(true);

// //   useEffect(() => {
// //     // Fetch recommendations from the backend
// //     const fetchRecommendations = async () => {
// //       try {
// //         const response = await axios.post('http://localhost:3000/api/recommend', userInput);
// //         setRecommendations(response.data.recommendations);
// //       } catch (error) {
// //         console.error("Error fetching recommendations:", error);
// //       } finally {
// //         setLoading(false);
// //       }
// //     };

// //     if (userInput) fetchRecommendations();
// //   }, [userInput]);

// //   return (
// //     <div className="min-h-screen bg-[#FAF7F0] pl-8 pr-8">
// //       <Navbar />
// //       <h1 className="text-3xl font-bold text-[#4A4947] text-center mb-6">
// //         Your Recommended Plan
// //       </h1>
      
// //       {loading ? (
// //         <p className="text-center text-gray-600 text-lg">Loading recommendations...</p>
// //       ) : (
// //         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
// //           {recommendations.length > 0 ? (
// //             recommendations.map((place) => (
// //               <div
// //                 key={place.id}
// //                 className="bg-white rounded-lg shadow-lg p-6 transition-transform transform hover:scale-105 hover:shadow-2xl"
// //               >
// //                 <img
// //                   src={place.image}
// //                   alt={place.title}
// //                   className="w-full h-48 object-cover rounded-lg mb-4"
// //                 />
// //                 <h3 className="text-xl font-semibold text-[#4A4947] mb-2">{place.title}</h3>
// //                 <p className="text-gray-600 mb-2">{place.description}</p>
// //                 <p className="text-sm text-gray-500">
// //                   Price: <span className="font-bold">₹{place.price}</span> | Duration: {place.duration} hrs
// //                 </p>
// //               </div>
// //             ))
// //           ) : (
// //             <p className="text-center text-gray-600 text-lg">
// //               No recommendations available.
// //             </p>
// //           )}
// //         </div>
// //       )}
// //     </div>
// //   );
// // };

// // export default Recommendations;





// // import { useLocation } from "react-router-dom";
// // import Navbar from '../Components/Navbar'; 

// // const Recommendations = () => {
// //   const { state } = useLocation();
// //   const { recommendations } = state || { recommendations: [] };

// //   return (
// //     <div className="min-h-screen bg-[#FAF7F0] pl-8 pr-8">
// //       <Navbar/>
// //             <h1 className="text-3xl font-bold text-[#4A4947] text-center mb-6">
// //         Your Recommended Plan
// //       </h1>
// //       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
// //         {recommendations.length > 0 ? (
// //           recommendations.map((place) => (
// //             <div
// //               key={place.id}
// //               className="bg-white rounded-lg shadow-lg p-6 transition-transform transform hover:scale-105 hover:shadow-2xl"
// //             >
// //               <img
// //                 src={place.image}
// //                 alt={place.title}
// //                 className="w-full h-48 object-cover rounded-lg mb-4"
// //               />
// //               <h3 className="text-xl font-semibold text-[#4A4947] mb-2">{place.title}</h3>
// //               <p className="text-gray-600 mb-2">{place.description}</p>
// //               <p className="text-sm text-gray-500">
// //                 Price: <span className="font-bold">₹{place.price}</span> | Duration: {place.duration} hrs
// //               </p>
// //             </div>
// //           ))
// //         ) : (
// //           <p className="text-center text-gray-600 text-lg">
// //             No recommendations available.
// //           </p>
// //         )}
// //       </div>
// //     </div>
// //   );
// // };

// // export default Recommendations;