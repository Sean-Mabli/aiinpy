import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { db } from './firebase'
import './index.css';
import { collection, getDocs } from 'firebase/firestore';

function Navbar() {
  const [version, setVersion] = useState(window.currentversion);
  
  function getversion(val) {
    setVersion(val.target.value);
    if (window.versions.includes(val.target.value) === true) {
      window.currentversion = val.target.value;
    }
  }

  const [content, setContent] = useState([]);
  const contentRef = collection(db, 'documentation')
  useEffect(() => {
    const getContent = async () => {
      const data = await getDocs(contentRef);
      setContent(data.docs.map((doc) => ({ ...doc.data(), id: doc.id})))
    };
    getContent();
  }, [])  

  const contentfilteredbyversion = content.filter(content => content.version === window.currentversion);

  return (
    <div>
      <div className="box">
        <Link to='/' className="p notext-decoration">aiinpy</Link> <br/>
      </div>
      <div class="inlinebox">
        <label className="h1" >version:&nbsp;</label>
        <input type="text" value={version} onChange={getversion} className="h1 lighter version"/>
      </div>

      {contentfilteredbyversion.map((item) => {
        return (
          <div>
            <Link to={item.url} className="h1 lighter link"> {item.title} </Link> <br />
          </div>
        )
      })}
      <div className="box">
        <a href="https://github.com/seanmabli/aiinpy" className="h1 lighter link">github</a> 
        <a href="https://pypi.org/project/aiinpy/" className="h1 lighter link">&nbsp;pypi</a> 
      </div>
    </div>
  );
}

export default Navbar;