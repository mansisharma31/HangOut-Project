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




import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const RecommendationForm = ({ onSubmit }) => {
    const [location, setLocation] = useState('');
    const [budget, setBudget] = useState('');
    const [duration, setDuration] = useState('');
    const [ageGroups, setAgeGroups] = useState([]);
    const [category, setCategory] = useState('');



    const navigate = useNavigate();

    // Age group options
    const ageGroupOptions = ['18-25', '26-40', '41-65', '65 and above'];

    // Handle age group checkboxes
    const handleAgeGroupChange = (ageGroup) => {
        setAgeGroups(prev => 
            prev.includes(ageGroup)
                ? prev.filter(item => item !== ageGroup)
                : [...prev, ageGroup]
        );
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ location, budget, duration, ageGroups, category });
        navigate('/recommendations');
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Location:</label>
                <input type="text" value={location} onChange={(e) => setLocation(e.target.value)} required />
            </div>
            <div>
                <label>Budget:</label>
                <input type="number" value={budget} onChange={(e) => setBudget(e.target.value)} required />
            </div>
            <div>
                <label>Duration (hours):</label>
                <input type="number" value={duration} onChange={(e) => setDuration(e.target.value)} required />
            </div>
            <div>
                <label>Age Groups:</label>
                {ageGroupOptions.map((group) => (
                    <label key={group}>
                        <input
                            type="checkbox"
                            value={group}
                            onChange={() => handleAgeGroupChange(group)}
                            checked={ageGroups.includes(group)}
                        />
                        {group}
                    </label>
                ))}
            </div>
            <div>
                <label>Category (optional):</label>
                <input type="text" value={category} onChange={(e) => setCategory(e.target.value)} />
            </div>
            <button type="submit">Get Recommendations</button>
        </form>
    );
};

export default RecommendationForm;




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
