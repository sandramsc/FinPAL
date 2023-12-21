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

const BarChartt = ({ barChartData, label }) => {
console.log("🚀 ~ file: BarChartt.js:20 ~ BarChartt ~ label:", label)
console.log("🚀 ~ file: BarChartt.js:20 ~ BarChartt ~ barChartData:", barChartData)

  const data = {
    labels: barChartData.labels,
    datasets: [{
      // label: ,
      data: barChartData.expenseDataset,
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
    <div className='w-full'>
      <Bar
      className='w-full'
        data={data}
        height={400}
        options={options}
      />
    </div>
  )
}

export default BarChartt