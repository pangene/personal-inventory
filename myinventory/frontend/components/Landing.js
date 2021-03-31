import React from 'react';
import { init } from 'ityped';

const typedWords = [
  'pikachu doll',
  'percy jackson',
  'Titanic DVD',
  'Space heater',
]

class Landing extends React.Component {
  componentDidMount() {
    // Initializing the typing animation
    const typingElement = document.getElementById('typing');
    init(
      typingElement, {
        strings: typedWords,
        showCursor: true,
        typeSpeed: 100,
        backSpeed: 70,
        startDelay: 700,
        backDelay: 500,
      }
    )
  }

  render() {
    return (
      <div className="mx-auto">
        <h1 className="text-center giant pt-100">Do I own</h1>
        <div className="input-group mx-auto mt-4 max-w-small">
          <div className="form-control underline">
            <span id="typing"></span>
          </div>
          <div className="input-group-append">
            <button className="btn btn-primary disabled" type="button">?</button>
          </div>
        </div>
        <div className="pt-5 text-center" id="description">
          <p>
            A personal-inventory management tool based around a simple user experience.
          </p>
          <p>
            <a href="/accounts/login">Sign in</a> or <a href="/accounts/register">Register</a> to get started.
          </p>
        </div>
      </div>
    )
  }
}

export default Landing;
