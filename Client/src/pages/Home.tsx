import React from 'react'
import api from '../api'
import { useNavigate } from 'react-router-dom'




export default function Home() {
  interface Asset {
    name: string
    ticker: string
    price: number
  }
  const [assets, setAssets] = React.useState<Asset[]>([])
  const [ticker,setTicker] = React.useState("")
  const [qty,setQty] = React.useState(0)
  const [indicatorcols,setIndicatorcols] = React.useState([])
  const navigate = useNavigate()


  return (
    <div className='flex justify-center items-center flex-col' >
      <button onClick={async () => {
          const res = await api.post('/getcurrprice', {ticker: "AAPL"})
          console.log(res)
          alert(res.data)
      }}>
        Getstockdata
      </button>
      <button onClick={async () => {
          const res = await api.get('/getindicators')
          console.log(res)
          alert(res.data)
      }}>
        Gettickers
      </button>
      <button onClick={async () => {
          const res = await api.post('/addasset', {ticker: "GOOG", qty: 10})
          console.log(res)
          alert(res.data)
      }}>
        addAsset
      </button>
      <button onClick={async () => {
          const res = await api.get('/getassets')
          console.log(res)
          alert(res.data)
      }}>
        getAssets
      </button>
    </div>
  )
}