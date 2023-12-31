/*!

=========================================================
* Vision UI Free React - v1.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/vision-ui-free-react
* Copyright 2021 Creative Tim (https://www.creative-tim.com/)
* Licensed under MIT (https://github.com/creativetimofficial/vision-ui-free-react/blob/master LICENSE.md)

* Design and Coded by Simmmple & Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/

// @mui material components
import Grid from "@mui/material/Grid";
import { Card, Stack } from "@mui/material";
import '../../App.css'

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiProgress from "components/VuiProgress";

// Vision UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import MiniStatisticsCard from "examples/Cards/StatisticsCards/MiniStatisticsCard";
import linearGradient from "assets/theme/functions/linearGradient";

// Vision UI Dashboard React base styles
import typography from "assets/theme/base/typography";
import colors from "assets/theme/base/colors";

// Dashboard layout components
import WelcomeMark from "layouts/dashboard/components/WelcomeMark";
import SatisfactionRate from "layouts/dashboard/components/SatisfactionRate";

// React icons
import { IoIosRocket } from "react-icons/io";
import { IoGlobe } from "react-icons/io5";
import { IoBuild } from "react-icons/io5";
import { IoWallet } from "react-icons/io5";
import { IoDocumentText } from "react-icons/io5";
import { FaShoppingCart } from "react-icons/fa";

// Data
import LineChart from "examples/Charts/LineCharts/LineChart";
import BarChartt from "examples/Charts/BarCharts/BarChartt";
import { lineChartDataDashboard } from "layouts/dashboard/data/lineChartData";
import { lineChartOptionsDashboard } from "layouts/dashboard/data/lineChartOptions";
import { useParams } from "react-router-dom";

// react hook
import { useState, useEffect } from "react";

const SERVER_BASE_URL = "https://finpal-alpha.23.94.26.231.sslip.io";

function Dashboard() {
  const { gradients } = colors;
  const { cardContent } = gradients;
  const { user_id: userId, start_date: startDate, end_date: endDate } = useParams()
  const [lineChartData, setLineChartData] = useState()
  const [barChartData, setBarChartData] = useState()
  useEffect(() => {
    const fetchTransactions = async ({ startDate, endDate, userId }) => {

      const response = await fetch(`${SERVER_BASE_URL}/transactions/?user_id=${userId}&start_date=${startDate}&end_date=${endDate}`);
      const data = await response.json();
      let expenseDataset = new Array(12).fill(0)
      console.log("🚀 ~ file: index.js:76 ~ fetchTransactions ~ expenseDataset:", expenseDataset)
      let incomeDataset = new Array(12).fill(0)
      console.log("🚀 ~ file: index.js:78 ~ fetchTransactions ~ incomeDataset:", incomeDataset)
      
      // key as categories, value as total expense
      let barChartData = {}

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

        if (category in barChartData) {
          barChartData[category] += amountOut
        } else {
          barChartData[category] = amountOut
        }

        // remove 0 at the left
        const labelIndex = Number(transactionDate.slice(4, 6) - 1).toString()

        incomeDataset[labelIndex] += amountIn
        expenseDataset[labelIndex] += amountOut
      }

      setLineChartData([
        {
          name: "Income",
          data: incomeDataset
        },
        {
          name: "Expense",
          data: expenseDataset
        }
      ])

      setBarChartData({
        labels: Object.keys(barChartData),
        expenseDataset: Object.values(barChartData)
      })
    }
    fetchTransactions({ startDate: startDate, endDate: endDate, userId: userId });
  }, [])
  return (
    <DashboardLayout>
      <DashboardNavbar />
      <VuiBox py={3}>
        <VuiBox mb={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "total income", fontWeight: "regular" }}
                count="$53,000"
                percentage={{ color: "success", text: "+55%" }}
                icon={{ color: "info", component: <IoWallet size="22px" color="white" /> }}
              />
            </Grid>
            <Grid item xs={18} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "total expenses" }}
                count="2,300"
                percentage={{ color: "success", text: "+3%" }}
                icon={{ color: "info", component: <IoGlobe size="22px" color="white" /> }}
              />
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "investments" }}
                count="+3,462"
                percentage={{ color: "error", text: "-2%" }}
                icon={{ color: "info", component: <IoDocumentText size="22px" color="white" /> }}
              />
            </Grid>
            <Grid item xs={12} md={6} xl={3}>
              <MiniStatisticsCard
                title={{ text: "total savings" }}
                count="$103,430"
                percentage={{ color: "success", text: "+5%" }}
                icon={{ color: "info", component: <FaShoppingCart size="20px" color="white" /> }}
              />
            </Grid>
          </Grid>
        </VuiBox>
        <VuiBox mb={3}>
          <Grid container spacing="18px">
            <Grid item xs={12} lg={12} xl={8}>
              <WelcomeMark />
            </Grid>
            <Grid item xs={12} lg={6} xl={4}>
              <SatisfactionRate />
            </Grid>
          </Grid>
        </VuiBox>
        <VuiBox mb={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} lg={6} xl={12}>
              <Card>
                <VuiBox sx={{ height: "100%" }}>
                  <VuiTypography variant="lg" color="white" fontWeight="bold" mb="5px">
                    My Activity
                  </VuiTypography>
                  <VuiBox sx={{ height: "310px" }}>
                    {lineChartData && (
                      <LineChart
                        lineChartData={lineChartData}
                        lineChartOptions={lineChartOptionsDashboard}
                      />
                    )}
                  </VuiBox>
                </VuiBox>
              </Card>
            </Grid>
          </Grid>
        </VuiBox>

        <Grid container spacing={3} direction="row" justifyContent="center" alignItems="stretch">
          <Grid item xs={12} md={6} lg={22}>
            <Card>
            <VuiTypography variant="lg" color="white" fontWeight="bold" mb="25px">
                  Expense Distribution
                </VuiTypography>
              <VuiBox>
                <VuiBox
                  className="App"
                  mb="24px"
                  height="420px"
                  sx={{
                    background: linearGradient(
                      cardContent.main,
                      cardContent.state,
                      cardContent.deg
                    ),
                    borderRadius: "20px",
                  }}
                >
                  {barChartData && (
                    <BarChartt
                      barChartData={barChartData}
                      label="Spending Categories"
                    />
                  )}
                </VuiBox>
              </VuiBox>
            </Card>
          </Grid>
        </Grid>
      </VuiBox>
      <Footer />
    </DashboardLayout>
  );
}

export default Dashboard;
