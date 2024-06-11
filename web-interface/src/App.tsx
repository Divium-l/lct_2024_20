import {
  createBrowserRouter, 
  RouterProvider 
} from 'react-router-dom';

import './API/axios.ts'

import DatabaseInspectorPage from './pages/DatabaseInspectorPage/DatabaseInspector';
import ConnectPage from './pages/ConnectPage/ConnectPage'

import './App.scss'

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element:  <ConnectPage/>
    },
    {
      path: "/database-inspector",
      element: <DatabaseInspectorPage/>
    },
  ]);
  
  return (
    <RouterProvider router={router} />
  )
}

export default App
