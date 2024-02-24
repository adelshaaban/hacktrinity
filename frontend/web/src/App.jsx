import ppLogo from './assets/logo.svg'
import './App.css'
import ImageUpload from './components/ImageUpload'

function App() {
  return (
    <>
      <div>
        <a href="" target="_blank">
          <img src={ppLogo} className="logo" alt="Power Pulse logo" />
        </a>
      </div>
      <ImageUpload />  
    </>
  )
}

export default App
