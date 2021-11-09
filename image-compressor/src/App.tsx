import "./App.css";
import { BrowserRouter as Router, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <body>
        <header className="App-header">
          <h1>Image Compression</h1>
          <p>
            You can compress jpg/png file and with some quality precision. To
            get started click the button.
          </p>
          <button className="btn">Upload an image</button>
        </header>
      </body>
      <footer>
        <p>Image Compressor &copy; CitraBodyLotion</p>
      </footer>
    </div>
  );
}

export default App;
