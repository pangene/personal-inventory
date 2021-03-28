import React, { useState, useEffect } from 'react'

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].toString().replace(/^([\s]*)|([\s]*)$/g, "");
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function Search() {
  const [searchVal, setSearchVal] = useState("");
  const [result, setResult] = useState([]);
  // Item is only considered in the inventory if it is an exact match.
  const [matchExact, setMatchExact] = useState(false);
  // Used for displaying the AddItem component. Enabled as soon as non-empty item is searched.
  const [canAdd, setCanAdd] = useState(false);

  const handleItemLoadSuccess = (result) => {
    console.log(result);
    setResult(result);

    // Checks for exact match
    let match = result.some((e) => e.name === searchVal);
    setMatchExact(match);
  }

  const handleItemLoadFail = (error) => {
    console.log(error);
    setResult({name: "There was an error."})
  }

  const handleSubmit = (e) => {
    if (searchVal === "") return;  // 
    e.preventDefault();  // Necessary for logging to persist
    setCanAdd(true);
    fetch('/api/items/?search=' + searchVal)
      .then(res => res.json())
      .then(
        (result) => {
          handleItemLoadSuccess(result);
        },
        (error) => {
          handleItemLoadFail(error);
        }
      );
  }

  return (
    <div>
      <form>
        <input 
          type="text" 
          placeholder="Search" 
          value={searchVal} 
          onChange={(e) => setSearchVal(e.target.value)}
        />
        <input type="submit" value="Submit" onClick={(e) => handleSubmit(e)}/>
      </form>
      {matchExact && "yep its there"}
      {result.length > 0 && <ResultsDisplay result={result}/>}
      {canAdd && <AddItem name={searchVal} upc=""/>}
    </div>
  )
}

function ResultsDisplay(props) {
  const result = props.result;
  const resultItems = result.map((item) =>
    <li key={item.name}>{item.name} - {item.upc}</li>
  )
  return (
    <div>
      <p>Found: </p>
      <ul>{resultItems}</ul>
    </div>
  )
}

function AddItem(props) {
  const [name, setName] = useState(props.name);
  const [upc, setUpc] = useState(props.upc);

  useEffect(() => {
    // Update the name and upc after initial mount.
    setName(props.name);
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Adding item to database.");

    let newItem = {name: name, upc: upc};
    console.log(newItem);

    fetch('/api/items/', {
      method: 'POST',
      credentials: "same-origin",
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newItem)
    })
      .then(res => res.json())
      .then(data => {
        console.log('Success:', data);
      })
      .catch(error => {
        console.error('Error:', error);
      })
  }

  return (
    <div>
      <p>Would you like to add this item?</p>
      <form>
        <input 
          type="text" 
          value={name} 
          onChange={(e) => setName(e.target.value)}
        />
        <input 
          type="text" 
          value={upc} 
          onChange={(e) => setUpc(e.target.value)}
        />
        <input type="submit" value="Submit" onClick={(e) => handleSubmit(e)}/>
      </form>
    </div>
  )
}

export default Search;