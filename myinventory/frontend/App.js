import React from 'react';
import Search from './components/Search'

function App() {
  const isLoggedIn = JSON.parse(document.getElementById('isLoggedIn').textContent)
  if (isLoggedIn) {
    return (
      <div>
        <Search />
      </div>
    )
  } else {
    return (
      <div>
        Landing Page
      </div>
    )
  }
}

export default App;
