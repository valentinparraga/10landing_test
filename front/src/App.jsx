import './App.css'
import Navbar from './components/Navbar.jsx' //no lleva el .jsx por la exportacion en el archivo
import Hero from './components/Hero.jsx'
import Main from './components/Main.jsx'
import FindUs from './components/FindUs.jsx'
import Footer from './components/Footer.jsx'

function App() {

  return (
    <>
      <Navbar/>
      <Hero/>
      <Main/>
      <FindUs/>
      <Footer/>
    </>
  )
}

export default App
