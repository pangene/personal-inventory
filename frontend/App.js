import React from 'react';
import Search from './components/Search';
import Landing from './components/Landing';

function App() {
  const isLoggedIn = JSON.parse(document.getElementById('isLoggedIn').textContent)
  console.log('Login status: ' + isLoggedIn);

  if (isLoggedIn) {
    return (
      <div>
        <Search />
      </div>
    );
  } else {
    return (
      <div>
        <Landing />
      </div>
    );
  }
}

export default App;
