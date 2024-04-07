// import React, { useState } from 'react';
// import './styles.css';

// // Importing the local JSON file directly
// const toFrontendData = require('./to_frontend.json');

// export default function App() {
//   // Extracting values from the local JSON file
//   const assignments = Object.values(toFrontendData);

//   const [selectedAssignment, setSelectedAssignment] = useState(null);

//   const handleClick = (index) => {
//     setSelectedAssignment(selectedAssignment === index ? null : index);
//   };

//   return (
//     <div className="container">
//       <div className="header">
//         <h1><span id="userName">User's</span> Assignments</h1>
//       </div>
//       <div className="assignments-container">
//         <div className="assignments-list">
//           {assignments.map((assignment, index) => (
//             <button key={index} className="assignment-button" onClick={() => handleClick(index)}>
//               <div className='display'>
//                 <div className="name">{assignment.assignment_name}</div>
//                 <div className="due-date">Due: {assignment.due_date}</div>
//               </div>
//               <div className='display'>
//                 <div className="course">{assignment.course_name}</div>
//                 <div className="time-estimate">Est. Time: {assignment.time_estimate}</div>
//               </div>
//             </button>
//           ))}
//         </div>
//         <div className="selected-assignment">
//           {selectedAssignment !== null && (
//             <div className="dropdown-menu">
//               <p>
//                 <p>We suggest the following outline to help finish this assignment:</p>
//                 <ol>
//                   {assignments[selectedAssignment].steps.map((step, index) => (
//                     <li key={index}>{step}</li>
//                   ))}
//                 </ol>
//               </p>
//               <p>
//                 <p>Here's some resources to help get you started:</p>
//                 <ul>
//                   {Object.entries(assignments[selectedAssignment].links).map(([name, link]) => (
//                     <li key={name}>
//                       <a href={link} target="_blank" rel="noopener noreferrer">{name}</a>
//                     </li>
//                   ))}
//                 </ul>
//               </p>
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }


// import React, { useState } from 'react';
// import './styles.css';

// // Importing the local JSON file directly
// const toFrontendData = require('./to_frontend.json');

// export default function App() {
//   // Extracting values from the local JSON file
//   const assignments = Object.values(toFrontendData);

//   const [selectedAssignment, setSelectedAssignment] = useState(null);
//   const [completedAssignments, setCompletedAssignments] = useState({}); // State to track completed assignments

//   const handleClick = (index) => {
//     setSelectedAssignment(selectedAssignment === index ? null : index);
//   };

//   const toggleCompletion = (index) => {
//     setCompletedAssignments({
//       ...completedAssignments,
//       [index]: !completedAssignments[index]
//     });
//   };

//   return (
//     <div className="container">
//       <div className="header">
//         <h1><span id="userName">User's</span> Assignments</h1>
//       </div>
//       <div className="assignments-container">
//         <div className="assignments-list">
//           {assignments.map((assignment, index) => (
//             <div key={index} className="assignment-item">
//               <button className={`assignment-button ${completedAssignments[index] ? 'completed' : ''}`} onClick={() => handleClick(index)}>
//                 <div className='display'>
//                   <div className="name">{assignment.assignment_name}</div>
//                   <div className="due-date">Due: {assignment.due_date}</div>
//                 </div>
//                 <div className='display'>
//                   <div className="course">{assignment.course_name}</div>
//                   <div className="time-estimate">Est. Time: {assignment.time_estimate}</div>
//                 </div>
//               </button>
//               <input
//                 type="checkbox"
//                 checked={completedAssignments[index] || false}
//                 onChange={() => toggleCompletion(index)}
//               />
//             </div>
//           ))}
//         </div>
//         <div className="selected-assignment">
//           {selectedAssignment !== null && (
//             <div className="dropdown-menu">
//               <p>
//                 <p>We suggest the following outline to help finish this assignment:</p>
//                 <ol>
//                   {assignments[selectedAssignment].steps.map((step, index) => (
//                     <li key={index}>{step}</li>
//                   ))}
//                 </ol>
//               </p>
//               <p>
//                 <p>Here's some resources to help get you started:</p>
//                 <ul>
//                   {Object.entries(assignments[selectedAssignment].links).map(([name, link]) => (
//                     <li key={name}>
//                       <a href={link} target="_blank" rel="noopener noreferrer">{name}</a>
//                     </li>
//                   ))}
//                 </ul>
//               </p>
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }

import React, { useState } from 'react';
import './styles.css';

// Importing the local JSON file directly
const toFrontendData = require('./to_frontend.json');

export default function App() {
  // Extracting values from the local JSON file
  const [assignments, setAssignments] = useState(Object.values(toFrontendData));

  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [completedAssignments, setCompletedAssignments] = useState({}); // State to track completed assignments
  const [newEstimateHours, setNewEstimateHours] = useState('');
  const [newEstimateMinutes, setNewEstimateMinutes] = useState('');

  const handleClick = (index) => {
    setSelectedAssignment(selectedAssignment === index ? null : index);
  };

  const toggleCompletion = (index) => {
    setCompletedAssignments({
      ...completedAssignments,
      [index]: !completedAssignments[index]
    });
  };

  const handleEstimateHoursChange = (event) => {
    setNewEstimateHours(event.target.value);
  };

  const handleEstimateMinutesChange = (event) => {
    setNewEstimateMinutes(event.target.value);
  };

  const handleUpdateEstimate = () => {
    // Update the estimate for the selected assignment
    if (selectedAssignment !== null && (newEstimateHours !== '' || newEstimateMinutes !== '')) {
      const hours = parseInt(newEstimateHours) || 0;
      const minutes = parseInt(newEstimateMinutes) || 0;
      const timeEstimateString = hours.toString() + 'hrs ' + minutes.toString() + 'mins';
      const updatedAssignments = [...assignments]; // Create a copy of assignments array
      updatedAssignments[selectedAssignment].time_estimate = timeEstimateString;
      setAssignments(updatedAssignments); // Update the state to trigger re-render
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1><span id="userName">User's</span> Canvassist</h1>
      </div>
      <div className="assignments-container">
        <div className="assignments-list">
          {assignments.map((assignment, index) => (
            <div key={index} className="assignment-item">
              <input
                type="checkbox"
                className="assignment-checkbox"
                checked={completedAssignments[index] || false}
                onChange={() => toggleCompletion(index)}
              />
              <button className={`assignment-button ${completedAssignments[index] ? 'completed' : ''}`} onClick={() => handleClick(index)}>
              <div className="left-section">
                <div className="name">{assignment.assignment_name}</div>
                <div className="course">{assignment.course_name}</div>
              </div>
              <div className="right-section">
                <div className="due-date">Due: {assignment.due_date}</div>
                <div className="time-estimate">Est. Time: {assignment.time_estimate}</div>
              </div>
            </button>
            </div>
          ))}
        </div>
        <div className="selected-assignment">
          {selectedAssignment !== null && (
            <div className="dropdown-menu">
              <p>
                <p>We suggest the following outline to help finish this assignment:</p>
                <ol>
                  {assignments[selectedAssignment].steps.map((step, index) => (
                    <li key={index}>{step}</li>
                  ))}
                </ol>
              </p>
              <p>
                <p>Here's some resources to help get you started:</p>
                <ul>
                  {Object.entries(assignments[selectedAssignment].links).map(([name, link]) => (
                    <li key={name}>
                      <a href={link} target="_blank" rel="noopener noreferrer">{name}</a>
                    </li>
                  ))}
                </ul>
              </p>
              <div>
                <input
                  type="number"
                  placeholder="Hours"
                  value={newEstimateHours}
                  onChange={handleEstimateHoursChange}
                />
                <span>hrs</span>
                <input
                  type="number"
                  placeholder="Minutes"
                  value={newEstimateMinutes}
                  onChange={handleEstimateMinutesChange}
                />
                <span>min</span>
                <button onClick={handleUpdateEstimate}>Update Estimate</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
