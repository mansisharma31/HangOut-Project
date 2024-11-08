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
