import React from 'react';

function PresentDisplay(props) {
  const present = props.present;
  const foundSomething = props.foundSomething;
  
  let classModifier = "danger";
  let icon = <i className="far fa-times-circle"></i>;
  let title = "Item is not present!";
  let body = "It doesn't seem like you own this item...";

  if (foundSomething) {
    body += " But, you may own something similar. Check what we found -->";
  }

  if (present) {
    classModifier = "success"; 
    icon = <i className="far fa-check-circle"></i>;
    title = "Item is present!";
    body = "You already own this!";
  }

  return (
    <div className={"max-h-large left float-start mb-3 card border-" + classModifier}>
      <div className={"card-body text-" + classModifier}>
        <div className="giant">{icon}</div>
        <h5 className="card-title">{title}</h5>
        <p className="card-text">{body}</p>
      </div>
    </div>
  )
}

export default PresentDisplay;