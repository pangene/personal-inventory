import React, { useState } from 'react'

function Search() {
  const [searchVal, setSearchVal] = useState("");
  const [result, setResult] = useState([]);

  const handleItemLoadSuccess = (result) => {
    console.log(result);
    setResult(result);
  }

  const handleItemLoadFail = (error) => {
    console.log(error);
    setResult({name: "There was an error."})
  }

  const handleSubmit = (e) => {
    e.preventDefault();
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
          placeholder="search" 
          value={searchVal} 
          onChange={(e) => setSearchVal(e.target.value)}
        />
        <input type="submit" value="Submit" onClick={(e) => handleSubmit(e)}/>
      </form>
      <p>Found:</p>
      <ResultsDisplay result={result}/>
    </div>
  )
}

function ResultsDisplay(props) {
  const result = props.result;
  const resultItems = result.map((item) =>
    <li key={item.name}>{item.name} - {item.upc}</li>
  )
  return (
    <ul>{resultItems}</ul>
  )
}

export default Search;