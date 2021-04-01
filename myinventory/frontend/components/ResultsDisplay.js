import React from 'react';

function ResultsDisplay(props) {
  const result = props.result;

  const resultItems = result.map((item) =>
    <a 
      href="#"
      onClick={() => props.search(item)}
      className={"list-group-item list-group-item-action" 
        + (item.name === props.name ? " active" : "")}
      key={item.name}
      >
      {item.name} - Qty: {item.quantity}
    </a>
  )

  return (
    <div className="right mb-3 float-end">
      <div className="list-group">
        <a href="#" className="list-group-item disabled">
          This is what we found:
        </a>
        <div className="scrollable max-h-medium">
          {resultItems}
        </div>
      </div>
    </div>
  )
}

export default ResultsDisplay;