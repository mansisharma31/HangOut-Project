import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const RecommendationForm = () => {
    const [formData, setFormData] = useState({
        location: '',
        budget: '',
        duration: '',
        ageGroup: '',
        categories: []
    });

    const navigate = useNavigate();

    // Update form data as the user types
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    // Handle checkbox selection for categories
    const handleCheckboxChange = (e) => {
        const { value, checked } = e.target;
        setFormData((prevState) => {
            const newCategories = checked
                ? [...prevState.categories, value]
                : prevState.categories.filter((category) => category !== value);
            return { ...prevState, categories: newCategories };
        });
    };

    // Submit form data to the backend
    // const handleSubmit = async (e) => {
    //     e.preventDefault();
    //     try {
    //         const response = await axios.post('http://localhost:3000/api/getRecommendations', formData);
    //         console.log(response);
    //         navigate('/recommendations', { state: { recommendations: response.data } });
    //     } catch (error) {
    //         console.error("Error fetching recommendations:", error);
    //     }
    // };
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:3000/api/getRecommendations', formData);
            navigate('/recommendations', { state: { recommendations: response.data } });
        } catch (error) {
            console.error("Error fetching recommendations:", error.response || error.message);
        }
    };

    return (
        <div className="recommendation-form-container">
            <h2>Plan Your Day</h2>
            <form onSubmit={handleSubmit} className="recommendation-form">
                <label>
                    Location:
                    <input
                        type="text"
                        name="location"
                        value={formData.location}
                        onChange={handleChange}
                        required
                    />
                </label>

                <label>
                    Budget:
                    <input
                        type="number"
                        name="budget"
                        value={formData.budget}
                        onChange={handleChange}
                        required
                    />
                </label>

                <label>
                    Duration (hours):
                    <input
                        type="number"
                        name="duration"
                        value={formData.duration}
                        onChange={handleChange}
                        required
                    />
                </label>

                <label>
                    Age Group:
                    <select name="ageGroup" value={formData.ageGroup} onChange={handleChange} required>
                        <option value="">Select Age Group</option>
                        <option value="18-25">18-25</option>
                        <option value="26-35">26-35</option>
                        <option value="36-50">36-50</option>
                        <option value="50+">50+</option>
                    </select>
                </label>

                <fieldset>
                    <legend>Categories:</legend>
                    <label>
                        <input
                            type="checkbox"
                            value="dining"
                            checked={formData.categories.includes("dining")}
                            onChange={handleCheckboxChange}
                        />
                        Dining
                    </label>
                    <label>
                        <input
                            type="checkbox"
                            value="adventure"
                            checked={formData.categories.includes("adventure")}
                            onChange={handleCheckboxChange}
                        />
                        Adventure
                    </label>
                    <label>
                        <input
                            type="checkbox"
                            value="entertainment"
                            checked={formData.categories.includes("entertainment")}
                            onChange={handleCheckboxChange}
                        />
                        Entertainment
                    </label>
                    <label>
                        <input
                            type="checkbox"
                            value="culture"
                            checked={formData.categories.includes("culture")}
                            onChange={handleCheckboxChange}
                        />
                        Culture
                    </label>
                    {/* Add more categories as needed */}
                </fieldset>

                <button type="submit" className="submit-button">
                    Get Recommendations
                </button>
            </form>
        </div>
    );
};

export default RecommendationForm;



// // RecommendationForm.js
// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';

// const ageGroupOptions = ['18-25', '26-40', '41-65', '65 and above'];

// const RecommendationForm = ({ onSubmit }) => {
//     const [formData, setFormData] = useState({
//         location: '',
//         budget: '',
//         duration: '',
//         age_groups: ageGroupOptions[0],  // Set default to first option
//         category: ''
//     });

//     const navigate = useNavigate();

//     // Handler to update form data based on input field changes
//     const handleChange = (e) => {
//         const { name, value } = e.target;
//         setFormData((prevData) => ({
//             ...prevData,
//             [name]: value
//         }));
//     };

//     // Submit handler
//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         if (typeof onSubmit === 'function') {
//             await onSubmit(formData);  // Call onSubmit with formData
//             navigate('/recommendations');  // Redirect to recommendations page
//         } else {
//             console.error("onSubmit is not a function");
//         }
//     };

//     return (
//         <form onSubmit={handleSubmit}>
//             <div>
//                 <label>
//                     Location:
//                     <input
//                         type="text"
//                         name="location"
//                         value={formData.location}
//                         onChange={handleChange}
//                         required
//                     />
//                 </label>
//             </div>

//             <div>
//                 <label>
//                     Budget:
//                     <input
//                         type="number"
//                         name="budget"
//                         value={formData.budget}
//                         onChange={handleChange}
//                         required
//                     />
//                 </label>
//             </div>

//             <div>
//                 <label>
//                     Duration (hours):
//                     <input
//                         type="number"
//                         name="duration"
//                         value={formData.duration}
//                         onChange={handleChange}
//                         required
//                     />
//                 </label>
//             </div>

//             <div>
//                 <label>
//                     Age Groups:
//                     <select
//                         name="age_groups"
//                         value={formData.age_groups}
//                         onChange={handleChange}
//                         required
//                     >
//                         {ageGroupOptions.map((ageGroup, index) => (
//                             <option key={index} value={ageGroup}>
//                                 {ageGroup}
//                             </option>
//                         ))}
//                     </select>
//                 </label>
//             </div>

//             <div>
//                 <label>
//                     Category:
//                     <input
//                         type="text"
//                         name="category"
//                         value={formData.category}
//                         onChange={handleChange}
//                     />
//                 </label>
//             </div>

//             <button type="submit">Get Recommendations</button>
//         </form>
//     );
// };

// export default RecommendationForm;




// // RecommendationForm.js
// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';

// const RecommendationForm = ({ onSubmit }) => { // Accept onSubmit as a prop
//     const [formData, setFormData] = useState({
//         location: '',
//         budget: '',
//         duration: '',
//         age_groups: '',
//         category: ''
//     });

//     const navigate = useNavigate();

//     // Handler to update form data based on input field changes
//     const handleChange = (e) => {
//         const { name, value } = e.target;
//         setFormData((prevData) => ({
//             ...prevData,
//             [name]: value
//         }));
//     };

//     // Submit handler
//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         if (typeof onSubmit === 'function') { // Check if onSubmit is a function
//             await onSubmit(formData);  // Call onSubmit with formData
//             navigate('/recommendations');  // Redirect to recommendations page
//         } else {
//             console.error("onSubmit is not a function");
//         }
//     };

//     return (
//         <form onSubmit={handleSubmit}>
//             <div>
//                 <label>
//                     Location:
//                     <input
//                         type="text"
//                         name="location"
//                         value={formData.location}
//                         onChange={handleChange}
//                         required
//                     />
//                 </label>
//             </div>

//             <div>
//                 <label>
//                     Budget:
//                     <input
//                         type="number"
//                         name="budget"
//                         value={formData.budget}
//                         onChange={handleChange}
//                         required
//                     />
//                 </label>
//             </div>

//             <div>
//                 <label>
//                     Duration (hours):
//                     <input
//                         type="number"
//                         name="duration"
//                         value={formData.duration}
//                         onChange={handleChange}
//                         required
//                     />
//                 </label>
//             </div>

//             <div>
//                 <label>
//                     Age Groups:
//                     <input
//                         type="text"
//                         name="age_groups"
//                         value={formData.age_groups}
//                         onChange={handleChange}
//                         placeholder="e.g., adults, teens"
//                         required
//                     />
//                 </label>
//             </div>

//             <div>
//                 <label>
//                     Category:
//                     <input
//                         type="text"
//                         name="category"
//                         value={formData.category}
//                         onChange={handleChange}
//                     />
//                 </label>
//             </div>

//             <button type="submit">Get Recommendations</button>
//         </form>
//     );
// };

// export default RecommendationForm;




// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import axios from 'axios';

// // const RecommendationForm = ({ onSubmit }) => {
//     // const [location, setLocation] = useState('');
//     // const [budget, setBudget] = useState('');
//     // const [duration, setDuration] = useState('');
//     // const [ageGroups, setAgeGroups] = useState([]);
//     // const [category, setCategory] = useState('');
//     const RecommendationForm = () => {
//         const [formData, setFormData] = useState({
//             location: '',
//             budget: '',
//             duration: '',
//             ageGroup: '',
//             categories: [],
//         });
        



//     const navigate = useNavigate();

//     // Age group options
//     const ageGroupOptions = ['18-25', '26-40', '41-65', '65 and above'];

//     // Handle age group checkboxes
//     const handleAgeGroupChange = (ageGroup) => {
//         setAgeGroups(prev => 
//             prev.includes(ageGroup)
//                 ? prev.filter(item => item !== ageGroup)
//                 : [...prev, ageGroup]
//         );
//     };

//     const handleSubmit = async(e) => {
//         e.preventDefault();
//         //onSubmit({ location, budget, duration, ageGroups, category });
//         try {
//             const response = await axios.post('http://localhost:5000/api/recommend', formData);
//             navigate('/api/getRecommendations', { state: { recommendations: response.data } });
//         } catch (error) {
//             console.error("Error fetching recommendations:", error);
//         }
//         // navigate('/api/getRecommendations');
//     };

//     return (
//         <form onSubmit={handleSubmit}>
//             <div>
//                 <label>Location:</label>
//                 <input type="text" value={location} onChange={(e) => setLocation(e.target.value)} required />
//             </div>
//             <div>
//                 <label>Budget:</label>
//                 <input type="number" value={budget} onChange={(e) => setBudget(e.target.value)} required />
//             </div>
//             <div>
//                 <label>Duration (hours):</label>
//                 <input type="number" value={duration} onChange={(e) => setDuration(e.target.value)} required />
//             </div>
//             <div>
//                 <label>Age Groups:</label>
//                 {ageGroupOptions.map((group) => (
//                     <label key={group}>
//                         <input
//                             type="checkbox"
//                             value={group}
//                             onChange={() => handleAgeGroupChange(group)}
//                             checked={ageGroups.includes(group)}
//                         />
//                         {group}
//                     </label>
//                 ))}
//             </div>
//             <div>
//                 <label>Category (optional):</label>
//                 <input type="text" value={category} onChange={(e) => setCategory(e.target.value)} />
//             </div>
//             <button type="submit">Get Recommendations</button>
//         </form>
//     );
// };

// export default RecommendationForm;




// import React, { useState } from 'react';
// import { useHistory } from 'react-router-dom';

// const RecommendationForm = () => {
//   const [location, setLocation] = useState('');
//   const [budget, setBudget] = useState('');
//   const [ageGroup, setAgeGroup] = useState('');
//   const [duration, setDuration] = useState('');
  
//   const history = useHistory();

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     // Prepare data to send to the backend
//     const formData = {
//       location,
//       budget,
//       ageGroup,
//       duration,
//     };

//     // Send data to the backend
//     const response = await fetch('/api/recommendations', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify(formData),
//     });

//     const data = await response.json();
//     if (response.ok) {
//       // Redirect to the recommendations page
//       history.push('/recommendations', { recommendations: data });
//     } else {
//       console.log('Error:', data);
//     }
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <input
//         type="text"
//         placeholder="Location"
//         value={location}
//         onChange={(e) => setLocation(e.target.value)}
//       />
//       <input
//         type="number"
//         placeholder="Budget"
//         value={budget}
//         onChange={(e) => setBudget(e.target.value)}
//       />
//       <input
//         type="text"
//         placeholder="Age Group"
//         value={ageGroup}
//         onChange={(e) => setAgeGroup(e.target.value)}
//       />
//       <input
//         type="number"
//         placeholder="Duration (hours)"
//         value={duration}
//         onChange={(e) => setDuration(e.target.value)}
//       />
//       <button type="submit">Submit</button>
//     </form>
//   );
// };

// export default RecommendationForm;
