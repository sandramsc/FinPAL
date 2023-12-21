import React, { useState, useEffect } from 'react'
import {
  Chart as ChartJS,

  BarElement,
  CategoryScale,
  LinearScale,

} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { useParams } from 'react-router-dom';

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
);

const baseUrl = "https://finpal-alpha.23.94.26.231.sslip.io";
const apiKey = "coinrankinga0d622c9c87f41f10b19b797ba4f932fa68aef3daff45766";
const LABELS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];


const BarChartt = () => {
  const {user_id: userId, start_date: startDate, end_date: endDate} = useParams()
  console.log("🚀 ~ file: BarChartt.js:26 ~ BarChartt ~ endDate:", endDate)
  console.log("🚀 ~ file: BarChartt.js:26 ~ BarChartt ~ startDate:", startDate)
  console.log("🚀 ~ file: BarChartt.js:26 ~ BarChartt ~ userId:", userId)
  const [chart, setChart] = useState({})

  // var proxyUrl = "https://cors-anywhere.herokuapp.com/";
  // var apiKey = "coinrankinga0d622c9c87f41f10b19b797ba4f932fa68aef3daff45766";

  useEffect(() => {
    const fetchTransactions = async ({ startDate, endDate, userId }) => {

      const response = await fetch(`${baseUrl}/transactions/?user_id=${userId}&start_date=${startDate}&end_date=${endDate}`);
      const data = await response.json();
      console.log("🚀 ~ file: BarChartt.js:35 ~ fetchTransactions ~ data:", data)

      let expenseDataset = new Array(12).fill(0)
      let incomeDataset = new Array(12).fill(0)
      for (const transaction of data.transactions) {
        const amountIn = Number(transaction.amountIn)
        const amountOut = Number(transaction.amountOut)
        const category = transaction.category
        const createdAt = transaction.createdAt
        const currency = transaction.currency
        const description = transaction.description
        const id = transaction.id
        const sourceOrPayee = transaction.sourceOrPayee
        const transactionDate = transaction.transactionDate
        const updatedAt = transaction.updatedAt
        const userId = transaction.userId

        // remove 0 at the left
        const labelIndex = Number(transactionDate.slice(4, 6)).toString()

        incomeDataset[labelIndex] += amountIn
        expenseDataset[labelIndex] += amountOut
        setChart({
          labels: LABELS,
          incomeDataset: incomeDataset,
          expenseDataset: expenseDataset
        })
      }
    }
    fetchTransactions({ startDate: startDate, endDate: endDate, userId: userId });
  },[])

  // useEffect(() => {
  //   const fetchCoins = async () => {
  //     await fetch(`${proxyUrl}${baseUrl}`, {
  //       method: 'GET',
  //       headers: {
  //         'Content-Type': 'application/json',
  //         'x-access-token': `${apiKey}`,
  //         'Access-Control-Allow-Origin': "*"
  //       }
  //     })
  //       .then((response) => {
  //         if (response.ok) {
  //           response.json().then((json) => {
  //             console.log(json.data);
  //             setChart(json.data)
  //           });
  //         }
  //       }).catch((error) => {
  //         console.log(error);
  //       });
  //   };
  //   fetchCoins()
  // }, [baseUrl, proxyUrl, apiKey])

  const data = {
    labels: LABELS,
    datasets: [{
      label: chart.labels,
      data: chart.incomeDataset,
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 1
    },{
      label: chart.labels,
      data: chart.expenseDataset,
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 1
    }]
  };

  const options = {
    maintainAspectRatio: false,
    scales: {
    },
    legend: {
      labels: {
        fontSize: 25,
      },
    },
  }

  return (
    <div>
      <Bar
        data={data}
        height={400}
        options={options}
      />
    </div>
  )
}

export default BarChartt