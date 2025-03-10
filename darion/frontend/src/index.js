import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';

// Font Awesome setup
import { library } from '@fortawesome/fontawesome-svg-core';
import { 
  faPaperPlane, 
  faSync, 
  faTimes,
  faEnvelope,
  faCalendar,
  faFile,
  faCog,
  faRobot,
  faSpinner
} from '@fortawesome/free-solid-svg-icons';

// Add icons to the library
library.add(
  faPaperPlane,
  faSync,
  faTimes,
  faEnvelope,
  faCalendar,
  faFile,
  faCog,
  faRobot,
  faSpinner
);

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
