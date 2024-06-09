import {
  createBrowserRouter, 
  RouterProvider 
} from 'react-router-dom';

import ConnectPage from './pages/ConnectPage/ConnectPage'

import './App.scss'
import DatabaseInspectorPage from './pages/DatabaseInspectorPage/DatabaseInspector';

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element:  <ConnectPage/>
    },
    {
      path: "/test",
      element: <h1>This is a test page</h1>
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
