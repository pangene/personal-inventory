import React, { useState } from 'react';
import AnimateHeight from 'react-animate-height';

import PresentDisplay from './PresentDisplay';
import ResultsDisplay from './ResultsDisplay';
import AddItem from './AddItem';
import { searchItems } from '../ItemsApi';

function Search() {
  // Mount animation setup
  const [height, setHeight] = useState(0);

  // searchVal always associated w/ name
  const [searchVal, setSearchVal] = useState("");
  // upc for now is unsearchable, but planned to implement soon
  const [upc, setUpc] = useState("");
  // tags for searched item
  const [tags, setTags] = useState([]);
  // array of searched item
  const [result, setResult] = useState([]);
  // Item is only considered in the inventory if it is an exact match.
  const [matchExact, setMatchExact] = useState(false);
  // Used for displaying additional components after first search
  const [canDisplay, setCanDisplay] = useState(false);

  const handleItemLoadSuccess = (result) => {
    console.log("Results:", result);
    setResult(result);

    // Checks for exact match
    let matchingItem = result.find((e) => e.name === searchVal);
    let match = matchingItem !== undefined;
    setMatchExact(match);

    // Updates upc and tags if it exists.
    if (match) {
      setUpc(matchingItem.upc);
      setTags(matchingItem.tags);
    }
  }

  const handleItemLoadFail = (error) => {
    console.log(error);
    setResult({name: "There was an error."});
  }

  const handleSubmit = (e) => {
    if (searchVal === "") return;  // Empty searchVal probably an accident.
    e.preventDefault();
    setCanDisplay(false);
    setHeight(0);
    // Get all items that match search params (name or upc)
    searchItems(searchVal)
      .then(
        (result) => {
          handleItemLoadSuccess(result);
          setCanDisplay(true);
          setTimeout(() => setHeight('auto'), 100);
        },
        (error) => {
          handleItemLoadFail(error);
        }
      );
  }

  const searchThisItem = (item) => {
    setSearchVal(item.name);
    setUpc(item.upc);
    setTags(item.tags);
  }

  return (
    <div className="mx-auto max-w-large">
      <div className="mx-auto">
        <h1 className="text-center giant pt-5">Do I own</h1>
      </div>
      <form>
        <div className="mx-auto max-w-medium input-group mb-3">
          <input 
            className="form-control underline"
            type="text" 
            placeholder="Enter the name of an item to see if you own it" 
            value={searchVal} 
            onChange={(e) => setSearchVal(e.target.value)}
          />
          <div className="input-group-append">
            <input
              className="btn btn-primary px-3"
              type="submit" 
              value="?" 
              onClick={(e) => handleSubmit(e)}
            />
          </div>
        </div>
      </form>
      <AnimateHeight 
        height={height} 
        delay={150}
        duration={300}
      >
        {canDisplay && 
          (<div>
            <PresentDisplay 
              present={matchExact} 
              foundSomething={result.length} 
            />
            <ResultsDisplay 
              className="float-end" 
              name={searchVal} 
              result={result} 
              search={searchThisItem}
            />
            <div className="clr"></div>
            <AddItem 
              present={matchExact} 
              name={searchVal} 
              upc={upc} 
              tags={tags} 
              />
          </div>)}
      </AnimateHeight>
    </div>
  )
}

export default Search;